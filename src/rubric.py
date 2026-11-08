SPEC = """Write a beginner lesson titled "Introduction to RAG" (Retrieval-Augmented Generation).
Audience: a 12th-grade student in India with LIMITED English. Use short sentences (about 12 words),
simple everyday words, and explain every technical term the first time. Use at least one
India-relevant example (e.g. NCERT, a college in Hyderabad, rupees). Use an everyday analogy.
Required sections (as markdown headings): What you will learn, What is RAG, How RAG works (4 steps:
chunk, embed, retrieve, generate), Why RAG is useful, Limits of RAG, Key words (table), Check yourself
(at least 4 questions WITH answers), Summary. Be factually correct: RAG does NOT retrain the model
and does NOT remove all hallucinations. Output markdown only."""

JUDGE_RUBRIC = """Score the lesson 1-5 on each dimension and list concrete problems.
- accuracy: every technical claim is correct (RAG does not retrain the model; it reduces, not removes, hallucinations)
- language: simple English for a limited-English 12th-grade learner; short sentences; terms explained
- pedagogy: clear flow, analogy, worked example, useful quiz
- cultural_fit: relevant, respectful examples for an Indian learner
Return ONLY JSON: {"accuracy":int,"language":int,"pedagogy":int,"cultural_fit":int,"issues":[str]}"""
