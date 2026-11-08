import argparse
from src.llm import LLM
from src.pipeline import run

p = argparse.ArgumentParser(description="Generate → Evaluate → Regenerate lesson agent")
p.add_argument("--provider", default=None, choices=["anthropic", "openai", "mock"])
p.add_argument("--model", default=None)
p.add_argument("--max-iters", type=int, default=3)
p.add_argument("--inject-error", action="store_true", help="Make the first draft contain deliberate factual errors")
a = p.parse_args()
run(LLM(a.provider, a.model), a.max_iters, a.inject_error)
