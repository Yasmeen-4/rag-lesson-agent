import json, time
from pathlib import Path
from .generator import generate
from .evaluator import evaluate


def run(llm, max_iters=3, inject_error=False, out_dir="output"):
    out = Path(out_dir); out.mkdir(exist_ok=True)
    feedback, log, draft = None, [], ""
    for i in range(1, max_iters + 1):
        print(f"\n=== Attempt {i}: GENERATE ===")
        draft = generate(llm, i, feedback, inject_error and i == 1)
        (out / f"draft_{i}.md").write_text(draft)
        print("=== EVALUATE ===")
        rep = evaluate(llm, draft)
        print(f"score={rep['score']}  passed={rep['passed']}")
        for iss in rep["issues"]:
            print("  ✗", iss)
        log.append({"attempt": i, "time": time.strftime("%H:%M:%S"), "report": rep})
        if rep["passed"]:
            print("✓ Evaluator approved the lesson.")
            break
        feedback = rep["issues"]
        print("→ REGENERATE with feedback")
    (out / "final_lesson.md").write_text(draft)
    (out / "run_log.json").write_text(json.dumps(log, indent=2, ensure_ascii=False))
    return draft, log
