"""Step-1 feasibility check: can vLLM serve a 7B MiMo/OLMo checkpoint in fp16
on 2x RTX 2080 Ti, do the outputs look sane (no fp16 overflow garbage), and
what throughput do we get for direct vs. thinking generation?

Usage (inside a SLURM job with 2 GPUs):
    python scripts/env_check_vllm.py --model XiaomiMiMo/MiMo-7B-RL --mode mimo
"""
import argparse
import json
import time

from transformers import AutoTokenizer
from vllm import LLM, SamplingParams

QUESTIONS = [
    "Who wrote the novel 'Nineteen Eighty-Four'?",
    "What is the capital city of Australia?",
    "Which element has the chemical symbol Fe?",
    "In which year did the Berlin Wall fall?",
    "Who painted the ceiling of the Sistine Chapel?",
    "What is the largest planet in the Solar System?",
    "Which country hosted the 2016 Summer Olympics?",
    "Who was the first person to walk on the Moon?",
]
INSTR = "Answer the following question with a short answer.\nQuestion: {q}"


def build(tok, q, mode, think):
    if mode == "mimo":
        msgs = [{"role": "system", "content": ""}, {"role": "user", "content": INSTR.format(q=q)}]
        p = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
        return p if think else p + "<think>\n\n</think>\n\n"
    if mode == "olmo":  # template already ends with "<think>"
        msgs = [{"role": "user", "content": INSTR.format(q=q)}]
        p = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
        return p if think else p + "</think>\n\n"
    raise ValueError(mode)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--mode", choices=["mimo", "olmo"], required=True)
    ap.add_argument("--tp", type=int, default=2)
    ap.add_argument("--max_model_len", type=int, default=5120)
    ap.add_argument("--gpu_mem", type=float, default=0.85)
    ap.add_argument("--out", default="logs/env_check.jsonl")
    a = ap.parse_args()

    tok = AutoTokenizer.from_pretrained(a.model, trust_remote_code=True)
    llm = LLM(model=a.model, trust_remote_code=True, dtype="float16",
              tensor_parallel_size=a.tp, max_model_len=a.max_model_len,
              gpu_memory_utilization=a.gpu_mem, seed=0)
    with open(a.out, "a") as f:
        for think, max_tok in [(False, 64), (True, 4096)]:
            prompts = [build(tok, q, a.mode, think) for q in QUESTIONS]
            sp = SamplingParams(temperature=0.6, top_p=0.95, max_tokens=max_tok, n=4, seed=0)
            t0 = time.time()
            outs = llm.generate(prompts, sp)
            dt = time.time() - t0
            ntok = sum(len(c.token_ids) for o in outs for c in o.outputs)
            trunc = sum(c.finish_reason == "length" for o in outs for c in o.outputs)
            print(f"\n### think={think}: {ntok} tokens in {dt:.1f}s = {ntok/dt:.0f} tok/s; truncated {trunc}/{4*len(QUESTIONS)}")
            for q, o in zip(QUESTIONS[:3], outs[:3]):
                print(f"--- Q: {q}\n{o.outputs[0].text[-600:]!r}")
            for q, p, o in zip(QUESTIONS, prompts, outs):
                f.write(json.dumps({"model": a.model, "think": think, "prompt": p,
                                    "outputs": [c.text for c in o.outputs]}) + "\n")


if __name__ == "__main__":
    main()
