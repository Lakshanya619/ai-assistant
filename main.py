import re
import streamlit as st

# Choose one provider

from groq_client import generate_response
# from hf import generate_response


def looks_incomplete(text: str) -> bool:
    if not text or len(text.strip()) < 10:
        return True

    text = text.strip()

    if text.endswith(("**", "*", "-", "—", ":", ",", "(", "[", "{")):
        return True

    if not re.search(r"[.!?]\s*$", text):
        return True

    return False


def complete_answer(question: str) -> str:

    prompt = f"""
Answer clearly in numbered points.
Finish every point completely.

Question:
{question}
"""

    answer = generate_response(
        prompt,
        temperature=0.3,
        max_tokens=1024,
    )

    if looks_incomplete(answer):

        continuation = generate_response(
            f"""
Continue exactly from where you stopped.
Do not repeat anything.

Question:
{question}

Answer so far:
{answer}
""",
            temperature=0.3,
            max_tokens=1024,
        )

        answer += "\n" + continuation

    return answer


def main():

    st.set_page_config(
        page_title="AI Teaching Assistant",
        page_icon="🎓"
    )

    st.title("🎓 AI Teaching Assistant")

    question = st.text_input(
        "Ask your question"
    )

    if st.button("Ask"):

        if not question.strip():
            st.warning("Please enter a question.")
            return

        with st.spinner("Thinking..."):
            answer = complete_answer(question)

        st.markdown("### Answer")
        st.markdown(answer)


if __name__ == "__main__":
    main()
