"""Discovery statistics (Phase 1a, project.md "Statistics").

    python scripts/discovery_stats.py [--graded results/analysis/discovery_graded.parquet]
        -> results/analysis/stats/{contrasts,flips,dose_response,size_interaction}.csv, summary.md

Unit of analysis = item (qid); resampling unit = item group (a question with its control
variants), so variants of one question are never treated as independent.

1. Paired contrasts per (model, benchmark[, subgroup]):
     Qwen3:  think vs nothink (primary), think_b{256,1024,4096} vs nothink, think vs think_b{1024,4096}
             ("overthinking": does the full trace do worse than a shorter budget?)
     gpt-oss: effort_high vs effort_low (primary)
   effect = mean over items of p_hi - p_lo (p = share of correct samples; greedy excluded);
   95% CI by group bootstrap (B=5000); two-sided p by group sign-flip permutation (10000).
   Benjamini-Hochberg FDR within each family (primary / budget / overthinking / subgroup).
2. Robust flips: hurt = p_lo >= .75 and p_hi <= .25 (helped: reverse). Noise floor = the same
   rule applied to the two disjoint 8-sample halves of no-think (Qwen3 only), per direction.
   Exact one-sided binomial test of hurt vs helped among robust flips.
3. Dose-response (Qwen3): GEE logistic, correct ~ level + level^2, level = 0..4
   (nothink, b256, b1024, b4096, full), exchangeable within group.
4. Size x mode (Qwen3-4B vs 8B): GEE logistic correct ~ think * size on {nothink, think}.
5. Sensitivity: primary contrast excluding items whose think trace hit the 16k cap in any sample.
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd

OUT = Path("results/analysis/stats")
RNG = np.random.default_rng(20261122)
QWEN_LEVELS = ["nothink", "think_b256", "think_b1024", "think_b4096", "think"]


def bh(p: pd.Series) -> pd.Series:
    """Benjamini-Hochberg adjusted p-values (NaN-safe)."""
    q = pd.Series(np.nan, index=p.index)
    ok = p.dropna()
    if ok.empty:
        return q
    order = ok.sort_values()
    m = len(order)
    adj = (order * m / np.arange(1, m + 1))[::-1].cummin()[::-1].clip(upper=1)
    q[adj.index] = adj
    return q


def item_rates(d: pd.DataFrame) -> pd.DataFrame:
    """Per item and condition: share correct over sampled (non-greedy) samples."""
    d = d[(d.sample_id >= 0) & d.correct.notna()]
    p = d.groupby(["qid", "condition"]).correct.mean().unstack()
    g = d.groupby("qid").group.first()
    return p.join(g)


def paired(p: pd.DataFrame, lo: str, hi: str, n_boot=5000, n_perm=10000) -> dict:
    x = p[[lo, hi, "group"]].dropna()
    if len(x) < 10:
        return {}
    diff = x[hi] - x[lo]
    s = diff.groupby(x.group).sum().to_numpy()
    n = diff.groupby(x.group).size().to_numpy()
    G, N = len(s), n.sum()
    eff = s.sum() / N
    idx = RNG.integers(0, G, size=(n_boot, G))
    boot = s[idx].sum(1) / n[idx].sum(1)
    signs = RNG.choice([-1.0, 1.0], size=(n_perm, G))
    perm = (signs * s).sum(1) / N
    pval = (np.sum(np.abs(perm) >= abs(eff) - 1e-12) + 1) / (n_perm + 1)
    return {"n_items": len(x), "n_groups": G, "acc_lo": x[lo].mean(), "acc_hi": x[hi].mean(), "effect": eff,
            "ci_lo": np.quantile(boot, .025), "ci_hi": np.quantile(boot, .975), "p": pval}


def flips(d: pd.DataFrame, p: pd.DataFrame, lo: str, hi: str) -> dict:
    from scipy.stats import binomtest
    x = p[[lo, hi]].dropna()
    hurt = int(((x[lo] >= .75) & (x[hi] <= .25)).sum())
    helped = int(((x[lo] <= .25) & (x[hi] >= .75)).sum())
    noise = np.nan
    if lo == "nothink":
        h = d[(d.condition == "nothink") & (d.sample_id >= 0) & d.correct.notna()].copy()
        h["half"] = np.where(h.sample_id < 8, "A", "B")
        hh = h.groupby(["qid", "half"]).correct.mean().unstack().dropna()
        noise = (((hh.A >= .75) & (hh.B <= .25)).sum() + ((hh.A <= .25) & (hh.B >= .75)).sum()) / 2
    pt = binomtest(hurt, hurt + helped, 0.5, alternative="greater").pvalue if hurt + helped else np.nan
    return {"hurt": hurt, "helped": helped, "noise_per_dir": noise, "p_hurt_gt_helped": pt}


def gee(df: pd.DataFrame, formula: str):
    import statsmodels.api as sm
    import statsmodels.formula.api as smf
    m = smf.gee(formula, groups="group", data=df, family=sm.families.Binomial(),
                cov_struct=sm.cov_struct.Exchangeable())
    return m.fit()


def subgroups(d: pd.DataFrame):
    """Subgroups where a think-induced failure could hide inside an overall gain."""
    yield "all", d
    if d.variant.notna().any():
        # items without a variant are the complement (e.g. XSTest safe prompts, answerable FalseQA/KUQ)
        v = d.variant.fillna("other")
        if v.nunique() < 2:
            return
        for v, dv in d.groupby(v):
            yield f"variant={v}", dv


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--graded", default="results/analysis/discovery_graded.parquet")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    df = pd.read_parquet(a.graded)
    df = df[df.correct.notna()]
    rows, frows, drows, irows = [], [], [], []
    for (m, b), d in df.groupby(["model", "benchmark"]):
        is_q = m.startswith("qwen3")
        prim = ("nothink", "think") if is_q else ("effort_low", "effort_high")
        for sg, ds in subgroups(d):
            p = item_rates(ds)
            fam_prim = "primary" if sg == "all" else "subgroup"
            contrasts = [(fam_prim, *prim)]
            if is_q and sg == "all":
                contrasts += [("budget", "nothink", c) for c in QWEN_LEVELS[1:4]]
                contrasts += [("overthinking", c, "think") for c in ("think_b1024", "think_b4096")]
            for fam, lo, hi in contrasts:
                if lo not in p or hi not in p:
                    continue
                r = paired(p, lo, hi)
                if not r:
                    continue
                r.update(model=m, benchmark=b, category=d.category.iloc[0], subgroup=sg, family=fam, lo=lo, hi=hi)
                if fam in ("primary", "subgroup"):
                    r.update(flips(ds, p, lo, hi))
                rows.append(r)
            if sg == "all":
                # sensitivity: drop items whose high-mode trace hit the cap in any sample
                capped = ds[(ds.condition == prim[1]) & (ds.forced_close == True)].qid.unique()  # noqa: E712
                pc = p.drop(index=[q for q in capped if q in p.index])
                r = paired(pc, *prim)
                if r:
                    r.update(model=m, benchmark=b, category=d.category.iloc[0], subgroup="no_capped_items",
                             family="sensitivity", lo=prim[0], hi=prim[1], n_capped=len(capped))
                    rows.append(r)
        # dose-response
        if is_q:
            x = d[d.condition.isin(QWEN_LEVELS) & (d.sample_id >= 0)].copy()
            x["level"] = x.condition.map({c: i for i, c in enumerate(QWEN_LEVELS)})
            x["level2"] = x.level ** 2
            x["y"] = x.correct
            try:
                f = gee(x, "y ~ level + level2")
                drows.append({"model": m, "benchmark": b, "b_level": f.params["level"], "p_level": f.pvalues["level"],
                              "b_level2": f.params["level2"], "p_level2": f.pvalues["level2"],
                              **{f"acc_{c}": x[x.condition == c].correct.mean() for c in QWEN_LEVELS}})
            except Exception as e:      # perfect separation etc.
                drows.append({"model": m, "benchmark": b, "error": str(e)[:100]})
    # size x mode interaction (Qwen3-4B vs 8B)
    q = df[df.model.isin(["qwen3_4b", "qwen3_8b"]) & df.condition.isin(["nothink", "think"]) & (df.sample_id >= 0)]
    for b, d in q.groupby("benchmark"):
        d = d.assign(think=(d.condition == "think").astype(int), big=(d.model == "qwen3_8b").astype(int), y=d.correct)
        try:
            f = gee(d, "y ~ think * big")
            irows.append({"benchmark": b, "b_think": f.params["think"], "b_think_x_8b": f.params["think:big"],
                          "p_interaction": f.pvalues["think:big"]})
        except Exception as e:
            irows.append({"benchmark": b, "error": str(e)[:100]})

    C = pd.DataFrame(rows)
    C["q"] = np.nan
    for fam, idx in C.groupby("family").groups.items():
        C.loc[idx, "q"] = bh(C.loc[idx, "p"])
    C = C.sort_values(["family", "q", "effect"])
    C.to_csv(OUT / "contrasts.csv", index=False)
    D = pd.DataFrame(drows)
    if "p_level2" in D:
        D["q_level2"] = bh(D.p_level2)
    D.to_csv(OUT / "dose_response.csv", index=False)
    I = pd.DataFrame(irows)
    if "p_interaction" in I:
        I["q_interaction"] = bh(I.p_interaction)
    I.to_csv(OUT / "size_interaction.csv", index=False)

    # ---- summary
    pd.set_option("display.width", 250, "display.max_rows", 300, "display.max_colwidth", 40)
    cols = ["model", "benchmark", "subgroup", "lo", "hi", "n_items", "acc_lo", "acc_hi", "effect", "ci_lo", "ci_hi",
            "q", "hurt", "helped", "noise_per_dir"]
    neg = C[(C.q < 0.05) & (C.effect < 0)]
    with open(OUT / "summary.md", "w") as f:
        f.write("# Discovery statistics\n\nSignificant (BH q < .05) contrasts where the higher-thinking condition is "
                "WORSE:\n\n" + neg[[c for c in cols + ["family"] if c in neg]].round(4).to_markdown(index=False) + "\n\n")
        for fam in ["primary", "subgroup", "budget", "overthinking", "sensitivity"]:
            t = C[C.family == fam]
            f.write(f"## {fam}\n\n" + t[[c for c in cols if c in t]].round(4).to_markdown(index=False) + "\n\n")
        f.write("## dose-response (GEE, level 0..4)\n\n" + D.round(4).to_markdown(index=False) + "\n\n")
        f.write("## size x mode (Qwen3-4B vs 8B)\n\n" + I.round(4).to_markdown(index=False) + "\n")
    print(open(OUT / "summary.md").read()[:6000])


if __name__ == "__main__":
    main()
