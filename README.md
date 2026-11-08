# Self-Evaluating Lesson Generator: "Introduction to RAG"

A **Generate → Evaluate → Regenerate** loop that writes a beginner lesson on RAG for a
12th-grade Indian learner with limited English, and refuses to ship it until it passes review.

```
 spec ──► GENERATOR ──► draft ──► EVALUATOR ──pass──► final_lesson.md
              ▲                       │
              └──── fix-list ◄──fail──┘   (max 3 attempts)
```

## Evaluator (two layers)
1. **Deterministic checks (always on):** known false claims (e.g. "RAG retrains the model",
   "removes all hallucinations"), required sections, readability (avg ≤ 14 words/sentence),
   India-relevant example, glossary terms, analogy, quiz with answers (≥ 4).
2. **LLM judge (real providers):** scores accuracy, language, pedagogy, cultural fit (1–5) and
   lists issues. Accuracy < 4 is a hard fail. Final score = 50% checks + 50% judge; pass ≥ 0.85
   with no critical failure.

Failures are sent back to the generator as a bullet list of fixes.

## Run
```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=...           # or OPENAI_API_KEY
python main.py --provider anthropic --inject-error   # demo: evaluator catches a planted error
python main.py --provider anthropic                  # normal run
python main.py --provider mock --inject-error        # offline test of the loop (no API key)
```
`--inject-error` tells the generator to put two false claims in draft 1, so you can show the
evaluator catching them and draft 2 fixing them.

Outputs go to `output/`: `draft_N.md`, `final_lesson.md`, `run_log.json` (scores + issues per attempt).

> Note: `--provider mock` replays a fixed lesson from `fixtures/` to test the loop offline.
> Run once with a real model before submitting and keep that `output/` folder.

## Design choices
- Plain Python (no framework): easy to read and debug; the loop is ~30 lines in `src/pipeline.py`.
- Rules catch things LLM judges miss (sentence length, missing quiz); the LLM judge catches what rules cannot (tone, subtle errors).
- Accuracy is a hard gate: a fluent but wrong lesson never passes.
