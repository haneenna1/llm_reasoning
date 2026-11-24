"""Figures for the discovery screen (static PNG + SVG, light theme, for the thesis).

    python scripts/discovery_figures.py   -> results/analysis/figures/*.png|svg

Reads results/analysis/stats/contrasts.csv and results/analysis/discovery_graded.parquet.
Colours: reference dataviz palette (validated). Categorical slots in fixed order, one per
model; diverging blue (thinking helps) <-> red (thinking hurts) with a gray midpoint.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm  # noqa: E402

FIG = Path("results/analysis/figures")
STATS = Path("results/analysis/stats")
MODELS = {"qwen3_4b": ("Qwen3-4B", "#2a78d6"), "qwen3_8b": ("Qwen3-8B", "#eb6834"),
          "gpt_oss_20b": ("gpt-oss-20b", "#1baf7a")}
INK, INK2, MUTED, GRID, BASE, SURF = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7", "#fcfcfb"
HELP, HURT = "#2a78d6", "#e34948"
DIVERGE = LinearSegmentedColormap.from_list("div", ["#a42c2c", HURT, "#f0efec", HELP, "#184f95"])
LEVELS = ["nothink", "think_b256", "think_b1024", "think_b4096", "think"]
LEVEL_LABELS = ["no-think", "256", "1k", "4k", "full"]
NAMES = {"triviaqa": "TriviaQA", "popqa": "PopQA", "falseqa": "FalseQA", "kuq": "KUQ", "umwp": "UMWP",
         "ifeval": "IFEval", "gsm_ic": "GSM-IC", "ist_misleading_math": "Misleading math",
         "ist_misleading_python": "Misleading python", "ist_paradoxes": "Paradoxes", "ist_zebra": "Zebra",
         "syco_answer": "Sycophancy", "nq_swap": "NQ-Swap", "xstest": "XSTest", "strongreject": "StrongREJECT",
         "gsm8k": "GSM8K", "math500": "MATH-500"}
CAT_ORDER = ["factual", "abstention", "instruction_following", "distractor", "sycophancy",
             "context_faithfulness", "safety", "control"]

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": BASE, "axes.labelcolor": INK2,
    "xtick.color": MUTED, "ytick.color": INK2, "axes.titlecolor": INK, "axes.titlesize": 10,
    "axes.titleweight": "bold", "axes.grid": False, "figure.facecolor": SURF, "axes.facecolor": SURF,
    "savefig.facecolor": SURF, "legend.frameon": False, "axes.spines.top": False, "axes.spines.right": False,
})


def save(fig, name):
    FIG.mkdir(parents=True, exist_ok=True)
    for ext in ("png", "svg"):
        fig.savefig(FIG / f"{name}.{ext}", dpi=200, bbox_inches="tight")
    plt.close(fig)
    print("wrote", FIG / f"{name}.png")


def bench_order(C):
    cats = C.drop_duplicates("benchmark").set_index("benchmark").category
    return sorted(cats.index, key=lambda b: (CAT_ORDER.index(cats[b]) if cats[b] in CAT_ORDER else 99, NAMES.get(b, b)))


def fig_effect_heatmap(C):
    """Primary contrast (think - no-think; gpt-oss high - low effort) per benchmark x model."""
    P = C[(C.family == "primary")]
    order = bench_order(P)
    models = [m for m in MODELS if m in set(P.model)]
    E = P.pivot(index="benchmark", columns="model", values="effect").reindex(order)[models] * 100
    Q = P.pivot(index="benchmark", columns="model", values="q").reindex(order)[models]
    lim = np.nanmax(np.abs(E.values))
    fig, ax = plt.subplots(figsize=(4.6, 0.32 * len(order) + 1.2))
    ax.imshow(E.values, cmap=DIVERGE, norm=TwoSlopeNorm(0, -lim, lim), aspect="auto")
    for i in range(E.shape[0]):
        for j in range(E.shape[1]):
            v, q = E.values[i, j], Q.values[i, j]
            if np.isnan(v):
                ax.text(j, i, "–", ha="center", va="center", color=MUTED)
                continue
            strong = abs(v) > 0.55 * lim
            ax.text(j, i, f"{v:+.1f}{'*' if q < .05 else ''}", ha="center", va="center", fontsize=8,
                    color="#ffffff" if strong else INK, fontweight="bold" if q < .05 else "normal")
    ax.set_xticks(range(len(models)), [MODELS[m][0] for m in models])
    ax.set_yticks(range(len(order)), [NAMES.get(b, b) for b in order])
    ax.xaxis.tick_top()
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title("Accuracy change from thinking (percentage points)\n"
                 "Qwen3: think − no-think · gpt-oss: high − low effort", loc="left", pad=28)
    ax.annotate("* BH-FDR q < .05 (group sign-flip permutation). Red = thinking worse, blue = better.",
                xy=(0, 0), xycoords="axes fraction", xytext=(-90, -8), textcoords="offset points",
                va="top", color=INK2, fontsize=7.5)
    save(fig, "f1_effect_heatmap")


def fig_dose_response(G):
    """Accuracy vs thinking budget, Qwen3-4B vs 8B, one panel per benchmark."""
    d = G[G.model.isin(["qwen3_4b", "qwen3_8b"]) & G.condition.isin(LEVELS) & (G.sample_id >= 0)]
    acc = d.groupby(["benchmark", "model", "condition"]).correct.mean().unstack("condition")[LEVELS]
    C = pd.read_csv(STATS / "contrasts.csv")
    order = [b for b in bench_order(C) if b in acc.index.get_level_values(0)]
    n = len(order)
    cols = 6
    rows = int(np.ceil(n / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(cols * 2.0, rows * 1.9), sharex=True)
    for ax, b in zip(axes.flat, order):
        for m in ["qwen3_4b", "qwen3_8b"]:
            if (b, m) not in acc.index:
                continue
            y = acc.loc[(b, m)].values * 100
            ax.plot(range(5), y, color=MODELS[m][1], lw=2, marker="o", ms=4, mec=SURF, mew=1)
        g = G[(G.benchmark == b) & (G.model == "gpt_oss_20b") & (G.sample_id >= 0)]
        for c, x in (("effort_low", 0), ("effort_high", 4)):
            v = g[g.condition == c].correct.mean() * 100
            if not np.isnan(v):
                ax.plot([x], [v], marker="D", ms=4.5, color=MODELS["gpt_oss_20b"][1], mec=SURF, mew=1, ls="none")
        ax.set_title(NAMES.get(b, b), fontsize=9, loc="left")
        ax.grid(axis="y", color=GRID, lw=0.6)
        ax.set_xticks(range(5), LEVEL_LABELS, fontsize=7)
        ax.tick_params(axis="y", labelsize=7, length=0)
        ax.tick_params(axis="x", length=0)
    for ax in list(axes.flat)[n:]:
        ax.axis("off")
    handles = [plt.Line2D([], [], color=MODELS[m][1], lw=2, marker="o", ms=4, label=MODELS[m][0])
               for m in ["qwen3_4b", "qwen3_8b"]]
    handles.append(plt.Line2D([], [], color=MODELS["gpt_oss_20b"][1], marker="D", ls="none", ms=4.5,
                              label="gpt-oss-20b (low effort at left, high at right)"))
    fig.legend(handles=handles, loc="upper left", ncol=3, bbox_to_anchor=(0.0, 1.04), fontsize=8)
    fig.suptitle("Accuracy (%) vs thinking budget (reasoning tokens before the forced answer)",
                 x=0.0, y=1.08, ha="left", fontsize=11, fontweight="bold", color=INK)
    fig.tight_layout()
    save(fig, "f2_dose_response")


def fig_flips(C):
    """Robust flips per benchmark: hurt (left) vs helped (right), with the no-think noise floor."""
    P = C[C.family == "primary"]
    order = bench_order(P)[::-1]
    models = [m for m in MODELS if m in set(P.model)]
    fig, axes = plt.subplots(1, len(models), figsize=(3.0 * len(models), 0.3 * len(order) + 1.3), sharey=True)
    lim = np.nanmax(P[["hurt", "helped"]].values) * 1.15
    for ax, m in zip(np.atleast_1d(axes), models):
        t = P[P.model == m].set_index("benchmark").reindex(order)
        y = np.arange(len(order))
        ax.barh(y, -t.hurt, color=HURT, height=0.62, label="hurt (right → wrong)")
        ax.barh(y, t.helped, color=HELP, height=0.62, label="helped (wrong → right)")
        if t.noise_per_dir.notna().any():
            for yi, nf in zip(y, t.noise_per_dir):
                if not np.isnan(nf) and nf > 0:
                    ax.plot([-nf, -nf], [yi - .38, yi + .38], color=INK, lw=1.2)
                    ax.plot([nf, nf], [yi - .38, yi + .38], color=INK, lw=1.2)
        for yi, (h, hp) in enumerate(zip(t.hurt, t.helped)):
            if not np.isnan(h) and h > 0:
                ax.text(-h - lim * .02, yi, f"{int(h)}", ha="right", va="center", fontsize=7, color=INK2)
            if not np.isnan(hp) and hp > 0:
                ax.text(hp + lim * .02, yi, f"{int(hp)}", ha="left", va="center", fontsize=7, color=INK2)
        ax.axvline(0, color=BASE, lw=0.8)
        ax.set_xlim(-lim, lim)
        ax.set_title(MODELS[m][0], loc="left")
        ax.tick_params(length=0)
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{abs(int(v))}"))
        ax.grid(axis="x", color=GRID, lw=0.6)
    np.atleast_1d(axes)[0].set_yticks(range(len(order)), [NAMES.get(b, b) for b in order])
    h, l = np.atleast_1d(axes)[0].get_legend_handles_labels()
    h.append(plt.Line2D([], [], color=INK, lw=1.2))
    l.append("no-think noise floor (two disjoint 8-sample halves)")
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.legend(h, l, loc="lower left", ncol=3, bbox_to_anchor=(0.0, 0.945), fontsize=8)
    fig.suptitle("Robust per-item flips (≥75% correct in one mode, ≤25% in the other)", x=0.01, y=1.0,
                 ha="left", va="bottom", fontsize=11, fontweight="bold", color=INK)
    save(fig, "f3_robust_flips")


PREREG = {("strongreject", "all", "nothink", "think"): "P1", ("xstest", "variant=refuse", "nothink", "think"): "P2",
          ("umwp", "variant=unanswerable", "nothink", "think"): "P3",
          ("ist_misleading_math", "all", "nothink", "think"): "P4", ("umwp", "all", "think_b1024", "think"): "P5",
          ("ist_paradoxes", "all", "think_b4096", "think"): "P6",
          ("ist_misleading_python", "all", "think_b1024", "think"): "P7"}


def fig_forest(C):
    """Every contrast where more thinking is significantly worse (BH q < .05), with 95% group-bootstrap CI.
    Rows that enter a pre-registered Phase 1b test are tagged P1-P7."""
    t = C[(C.q < .05) & (C.effect < 0) & C.family.isin(["primary", "budget", "overthinking", "subgroup"])].copy()
    t["tag"] = [PREREG.get((r.benchmark, r.subgroup, r.lo, r.hi), "") for r in t.itertuples()]
    t["label"] = t.apply(lambda r: f"{MODELS.get(r.model, (r.model,))[0]} · {NAMES.get(r.benchmark, r.benchmark)}"
                         f"{'' if r.subgroup == 'all' else ' [' + r.subgroup.split('=')[-1] + ']'}"
                         f" · {r.hi.replace('think_b', 'b')} vs {r.lo.replace('think_b', 'b')}", axis=1)
    t = t.sort_values("effect", ascending=False)
    fig, ax = plt.subplots(figsize=(6.4, 0.24 * len(t) + 1.0))
    y = np.arange(len(t))
    col = [HURT if tag else "#f0a3a2" for tag in t.tag]
    ax.hlines(y, t.ci_lo * 100, t.ci_hi * 100, color=col, lw=2)
    ax.scatter(t.effect * 100, y, color=col, s=24, zorder=3, edgecolor=SURF, linewidth=1)
    for yi, tag in zip(y, t.tag):
        if tag:
            ax.text(0.6, yi, tag, va="center", fontsize=7, color=INK, fontweight="bold")
    ax.axvline(0, color=BASE, lw=0.8)
    ax.set_yticks(y, t.label, fontsize=7.5)
    ax.set_ylim(-0.7, len(t) - 0.3)
    ax.tick_params(length=0)
    ax.grid(axis="x", color=GRID, lw=0.6)
    ax.set_xlabel("change in share correct (percentage points), 95% CI")
    ax.set_title(f"Where more thinking is worse: all {len(t)} contrasts with BH q < .05\n"
                 "dark = enters a pre-registered confirmation test (P1–P7)", loc="left")
    save(fig, "f4_forest")


def fig_trace_lengths(G):
    """Reasoning length per benchmark (think / effort_high), with the share cut at the cap."""
    d = G[G.condition.isin(["think", "effort_high"]) & (G.sample_id >= 0)]
    C = pd.read_csv(STATS / "contrasts.csv")
    order = bench_order(C)[::-1]
    models = [m for m in MODELS if m in set(d.model)]
    fig, ax = plt.subplots(figsize=(6.4, 0.36 * len(order) + 1.2))
    w = 0.26
    for k, m in enumerate(models):
        t = d[d.model == m].groupby("benchmark").n_reasoning_tokens.median().reindex(order)
        cut = d[d.model == m].groupby("benchmark").forced_close.mean().reindex(order)
        y = np.arange(len(order)) + (k - 1) * w
        ax.barh(y, t, height=w * 0.9, color=MODELS[m][1], label=MODELS[m][0])
        for yi, v, c in zip(y, t, cut):
            if not np.isnan(c) and c >= .10:
                ax.text(v + 150, yi, f"{c:.0%} cut", va="center", fontsize=6.5, color=INK2)
    ax.axvline(16384, color=INK2, lw=1, ls="--")
    ax.text(16384, len(order) - 0.3, "16k cap", ha="right", va="bottom", fontsize=7, color=INK2)
    ax.set_yticks(range(len(order)), [NAMES.get(b, b) for b in order])
    ax.tick_params(length=0)
    ax.grid(axis="x", color=GRID, lw=0.6)
    ax.set_xlabel("median reasoning tokens (full think / high effort)")
    ax.legend(loc="lower right", fontsize=8)
    ax.set_title("How long the models think, and how often the 16k cap cuts them", loc="left")
    save(fig, "f5_trace_lengths")


def fig_candidates(G):
    """The behaviours behind the candidates, per thinking level: unsafe-prompt refusal (XSTest),
    harmfulness score (StrongREJECT), abstention on unanswerable problems (UMWP)."""
    d = G[(G.sample_id >= 0)]
    panels = [("xstest", "variant", "refuse", lambda x: (x.xstest_class == "full_refusal").mean(),
               "XSTest unsafe prompts:\nfull refusals (%)"),
              ("strongreject", None, None, lambda x: x.sr_score.mean(),
               "StrongREJECT: mean harmfulness\n(judge score ×100, lower = safer)"),
              ("umwp", "variant", "unanswerable", lambda x: (x.abstained == True).mean(),  # noqa: E712
               "UMWP unanswerable problems:\nabstentions (%)")]
    fig, axes = plt.subplots(1, 3, figsize=(9.6, 2.9))
    for ax, (b, col, val, f, title) in zip(axes, panels):
        x = d[d.benchmark == b]
        if col:
            x = x[x[col] == val]
        for m in ["qwen3_4b", "qwen3_8b"]:
            xm = x[x.model == m]
            y = [f(xm[xm.condition == c]) * 100 for c in LEVELS]
            ax.plot(range(5), y, color=MODELS[m][1], lw=2, marker="o", ms=4, mec=SURF, mew=1)
        xg = x[x.model == "gpt_oss_20b"]
        for c, xx in (("effort_low", 0), ("effort_high", 4)):
            ax.plot([xx], [f(xg[xg.condition == c]) * 100], marker="D", ms=4.5, ls="none",
                    color=MODELS["gpt_oss_20b"][1], mec=SURF, mew=1)
        ax.set_title(title, loc="left", fontsize=9)
        ax.set_xticks(range(5), LEVEL_LABELS, fontsize=7.5)
        ax.tick_params(length=0, labelsize=7.5)
        ax.grid(axis="y", color=GRID, lw=0.6)
        ax.set_ylim(bottom=0)
    handles = [plt.Line2D([], [], color=MODELS[m][1], lw=2, marker="o", ms=4, label=MODELS[m][0])
               for m in ["qwen3_4b", "qwen3_8b"]]
    handles.append(plt.Line2D([], [], color=MODELS["gpt_oss_20b"][1], marker="D", ls="none", ms=4.5,
                              label="gpt-oss-20b (low effort at left, high at right)"))
    fig.tight_layout(rect=(0, 0, 1, 0.86))
    fig.legend(handles=handles, loc="lower left", ncol=3, bbox_to_anchor=(0.0, 0.86), fontsize=8)
    fig.suptitle("What changes with thinking on the safety and abstention candidates (x: thinking budget)",
                 x=0.01, y=0.97, ha="left", va="bottom", fontsize=11, fontweight="bold", color=INK)
    save(fig, "f6_candidate_behaviour")


def tables(C, G):
    """t1: the pre-registered candidates with their discovery statistics; t2: accuracy per benchmark."""
    out = Path("results/analysis/tables")
    out.mkdir(parents=True, exist_ok=True)
    t = C[[(r.benchmark, r.subgroup, r.lo, r.hi) in PREREG for r in C.itertuples()]].copy()
    t["test"] = [PREREG[(r.benchmark, r.subgroup, r.lo, r.hi)] for r in t.itertuples()]
    t = t[t.model != "gpt_oss_20b"].sort_values(["test", "model"])
    t1 = pd.DataFrame({"test": t.test, "model": t.model.map(lambda m: MODELS[m][0]),
                       "benchmark": t.benchmark.map(NAMES) + t.subgroup.map(lambda s: "" if s == "all" else f" ({s.split('=')[1]})"),
                       "contrast": t.hi + " − " + t.lo, "items": t.n_items,
                       "lo %": (t.acc_lo * 100).round(1), "hi %": (t.acc_hi * 100).round(1),
                       "effect pp [95% CI]": [f"{e*100:+.1f} [{a*100:+.1f}, {b*100:+.1f}]" for e, a, b in zip(t.effect, t.ci_lo, t.ci_hi)],
                       "BH q": t.q.map(lambda q: f"{q:.1g}" if q >= .001 else "<.001"),
                       "flips hurt/helped": [f"{int(h)}/{int(hp)}" if not np.isnan(h) else "–" for h, hp in zip(t.hurt, t.helped)],
                       # P4/P6 test Qwen3-8B only, P7 Qwen3-4B only; the other model is shown for context
                       "in test": ["context" if (r.test in ("P4", "P6") and r.model != "qwen3_8b") or
                                   (r.test == "P7" and r.model != "qwen3_4b") else "yes" for r in t.itertuples()]})
    t1.to_csv(out / "t1_candidates.csv", index=False)
    (out / "t1_candidates.md").write_text(t1.to_markdown(index=False) + "\n")
    d = G[G.sample_id >= 0]
    a = d.groupby(["benchmark", "model", "condition"]).correct.mean().unstack(["model", "condition"]) * 100
    cols = [(m, c) for m in MODELS for c in (LEVELS if m != "gpt_oss_20b" else ["effort_low", "effort_high"]) if (m, c) in a]
    a = a[cols].reindex(bench_order(C)).round(1)
    a.index = [NAMES.get(b, b) for b in a.index]
    a.columns = [f"{MODELS[m][0]} {c.replace('think_b', 'b').replace('effort_', '')}" for m, c in a.columns]
    a.to_csv(out / "t2_accuracy.csv")
    (out / "t2_accuracy.md").write_text(a.to_markdown() + "\n")
    print("wrote", out)


def main():
    C = pd.read_csv(STATS / "contrasts.csv")
    G = pd.read_parquet("results/analysis/discovery_graded.parquet")
    G = G[G.correct.notna()]
    fig_effect_heatmap(C)
    fig_dose_response(G)
    fig_flips(C)
    fig_forest(C)
    fig_trace_lengths(pd.read_parquet("results/analysis/discovery_graded.parquet"))
    fig_candidates(pd.read_parquet("results/analysis/discovery_graded.parquet"))
    tables(C, G)


if __name__ == "__main__":
    main()
