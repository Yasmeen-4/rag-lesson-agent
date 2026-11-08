"""Evaluator = deterministic checks (always on) + optional LLM judge (real providers)."""
import json, re
from .rubric import JUDGE_RUBRIC

REQUIRED = ["What you will learn", "What is RAG", "How RAG works", "Why RAG is useful",
            "Limits of RAG", "Key words", "Check yourself", "Summary"]
INDIA_WORDS = ["India", "NCERT", "CBSE", "Hyderabad", "₹", "rupee", "Indian"]
TERMS = ["LLM", "Hallucination", "Chunk", "Embedding", "Vector database"]
FALSE_CLAIMS = [
    (r"retrains? the (model|AI)", "False: RAG does not retrain the model; it only looks up documents."),
    (r"(removes?|eliminates?) all (wrong answers|hallucinations|mistakes)", "False: RAG reduces wrong answers but cannot remove them all."),
    (r"never makes? mistakes", "False: an AI using RAG can still make mistakes."),
    (r"invented by (Google|OpenAI)", "False: RAG was introduced by Facebook AI Research (Lewis et al., 2020)."),
    (r"changes? the (model's )?weights", "False: RAG does not change model weights."),
]


def _sentences(md: str):
    prose = [l for l in md.splitlines() if l.strip() and not l.startswith(("#", "|"))]
    text = " ".join(re.sub(r"[*_`>-]", " ", l) for l in prose)
    return [s.strip() for s in re.split(r"(?<=[.?!:])\s+", text) if len(s.split()) > 1]


def deterministic_checks(md: str):
    checks = []
    def add(name, ok, detail, critical=False):
        checks.append({"name": name, "passed": bool(ok), "critical": critical, "detail": detail})

    bad = []
    for pat, msg in FALSE_CLAIMS:
        m = re.search(pat, md, re.I)
        if m:
            bad.append(f'{msg} Found: "{m.group(0)}"')
    if bad:
        for b in bad:
            add("factual_accuracy", False, b, critical=True)
    else:
        add("factual_accuracy", True, "No known false claims found", True)

    missing = [h for h in REQUIRED if h.lower() not in md.lower()]
    add("required_sections", not missing, f"Missing sections: {missing}" if missing else "All sections present", True)

    sents = _sentences(md)
    avg = sum(len(s.split()) for s in sents) / max(len(sents), 1)
    longest = max((len(s.split()) for s in sents), default=0)
    add("readability", avg <= 14 and longest <= 30,
        f"avg sentence = {avg:.1f} words (max 14), longest = {longest} (max 30). Use shorter sentences.")

    add("india_context", any(w.lower() in md.lower() for w in INDIA_WORDS), "Add an India-relevant example")
    add("glossary", all(t.lower() in md.lower() for t in TERMS), "Key-words table must define: " + ", ".join(TERMS))
    nq = len(re.findall(r"\*\*Q\d", md)); na = len(re.findall(r"\*\*Answer", md))
    add("quiz", nq >= 4 and na >= nq, f"{nq} questions, {na} answers (need >=4 with answers)", True)
    add("analogy", re.search(r"open-book|library|analogy", md, re.I), "Add an everyday analogy")
    return checks


def llm_judge(llm, md: str):
    raw = llm.complete("You are a strict curriculum reviewer.", JUDGE_RUBRIC + "\n\nLESSON:\n" + md)
    return json.loads(re.search(r"\{.*\}", raw, re.S).group(0))


def evaluate(llm, md: str, threshold: float = 0.85):
    checks = deterministic_checks(md)
    issues = [f"[{c['name']}] {c['detail']}" for c in checks if not c["passed"]]
    score = sum(c["passed"] for c in checks) / len(checks)
    judge = None
    if not llm.is_mock:
        judge = llm_judge(llm, md)
        issues += [f"[judge] {i}" for i in judge.get("issues", [])]
        dims = [judge[k] for k in ("accuracy", "language", "pedagogy", "cultural_fit")]
        score = 0.5 * score + 0.5 * (sum(dims) / (5 * len(dims)))
        if judge["accuracy"] < 4:
            checks.append({"name": "judge_accuracy", "passed": False, "critical": True, "detail": "judge accuracy < 4"})
    critical_fail = any(c["critical"] and not c["passed"] for c in checks)
    return {"passed": (not critical_fail) and score >= threshold, "score": round(score, 3),
            "checks": checks, "judge": judge, "issues": issues}
