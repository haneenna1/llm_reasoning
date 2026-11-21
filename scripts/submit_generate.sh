#!/bin/bash
# Submit scripts/slurm_generate.sbatch on the fastest GPU type that is free right now.
# Preference: nlp partition (account nlp, high priority) first, then public (account cs);
# within each, the fastest bf16 card first. If nothing is free, queue on nlp for any bf16 card.
#
#   scripts/submit_generate.sh [--dry-run] [-J NAME] [SBATCH_FLAGS... --] <run_generation.py args...>
#   scripts/submit_generate.sh -J mimo_rl configs/runs/mimo_rl_{direct,think}.yaml
#   scripts/submit_generate.sh -J smoke_rl --limit 50 --out_dir results/smoke configs/runs/mimo_rl_*.yaml
#   scripts/submit_generate.sh -J mimo_rl --time=12:00:00 -- configs/runs/mimo_rl_*.yaml
# Extra sbatch flags go before a `--`; everything after it goes to run_generation.py.
# Without `--`, everything after --dry-run/-J goes to run_generation.py.
set -euo pipefail
cd "$(dirname "$0")/.."
SBATCH_FILE=scripts/slurm_generate.sbatch

# Fastest first for 1x 7B bf16 inference. Cards without bf16 (2080ti, 1080ti, titanxp) are never listed.
PREF=(H200 PRO6000 A100 6000ADA L40 A40 A6000)

# Excluded nodes and per-job resources are read from the sbatch header: it is the
# single source of truth (edit `#SBATCH --exclude=` there to add a bad node).
header() { sed -n "s/^#SBATCH --$1=//p" "$SBATCH_FILE" | head -1; }
EXCLUDE=$(header exclude)
NEED_CPUS=$(header cpus-per-task)
mem=$(header mem)
case "$mem" in *G) NEED_MEM_MB=$(( ${mem%G} * 1024 )) ;; *M) NEED_MEM_MB=${mem%M} ;; *) NEED_MEM_MB=$mem ;; esac
[ -n "$EXCLUDE" ] && [ -n "$NEED_CPUS" ] && [ -n "$NEED_MEM_MB" ] ||
  { echo "could not read --exclude/--cpus-per-task/--mem from $SBATCH_FILE" >&2; exit 1; }

dry=0; name=gen
while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run) dry=1; shift ;;
    -J) name="$2"; shift 2 ;;
    *) break ;;
  esac
done
extra=()
if printf '%s\n' "$@" | grep -qx -- '--'; then
  while [ "$1" != "--" ]; do extra+=("$1"); shift; done
  shift
fi
[ $# -gt 0 ] || { echo "usage: $0 [--dry-run] [-J NAME] [SBATCH_FLAGS... --] <run_generation.py args...>" >&2; exit 1; }

# Print the GPU types in partition $1 that have >=1 free GPU on a node with enough free CPUs/mem.
free_types() {
  sinfo -h -N -p "$1" -t idle,mix \
      -O "NodeList:40,Gres:80,GresUsed:100,CPUsState:30,Memory:15,AllocMem:15" |
  awk -v bad=",$EXCLUDE," -v cpus="$NEED_CPUS" -v mem="$NEED_MEM_MB" '
    index(bad, "," $1 ",") { next }
    {
      split($4, c, "/"); if (c[2] < cpus) next          # A/I/O/T -> idle CPUs
      if ($5 - $6 < mem) next
      n = split($2, g, ","); if (n != 1) next           # skip mixed-GRES nodes (old cards)
      split(g[1], t, ":"); type = t[2]; total = t[3]; sub(/\(.*/, "", total)
      split($3, u, ":"); used = u[3]; sub(/\(.*/, "", used)
      if (total - used > 0) print type
    }' | sort -u
}

pick() {  # $1 partition -> fastest free preferred type, or nothing
  local avail; avail=$(free_types "$1")
  for t in "${PREF[@]}"; do grep -qx "$t" <<<"$avail" && { echo "$t"; return; }; done
}

# --exclude is left to the sbatch header (CLI flags would replace it, not extend it).
if t=$(pick nlp) && [ -n "$t" ]; then
  opts=(--account=nlp --partition=nlp --gres="gpu:$t:1")
elif t=$(pick public) && [ -n "$t" ]; then
  opts=(--account=cs --partition=public --gres="gpu:$t:1")
else
  t="any (queued)"
  opts=(--account=nlp --partition=nlp --gres=gpu:1)
fi

cmd=(sbatch -J "$name" "${opts[@]}" "${extra[@]}" "$SBATCH_FILE" "$@")
echo "GPU choice: $t -> ${cmd[*]}"
[ "$dry" = 1 ] || "${cmd[@]}"
