from .rubric import SPEC

SYSTEM = "You are an expert teacher who writes lessons for Indian school students with limited English."


def generate(llm, attempt: int, feedback=None, inject_error=False) -> str:
    prompt = SPEC
    if feedback:
        prompt += "\n\nA reviewer found these problems in your previous draft. Fix ALL of them and keep everything else:\n"
        prompt += "\n".join(f"- {f}" for f in feedback)
    if inject_error:
        prompt += ("\n\nDELIBERATE_ERROR (testing only): include two false claims - say RAG retrains the model "
                   "every night, and that RAG removes all wrong answers.")
    return llm.complete(SYSTEM, prompt)
