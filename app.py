
import streamlit as st
import assistant_core


st.set_page_config(
    page_title="StudyPilot",
    page_icon="🎓",
    layout="centered",
)

st.title("🎓 StudyPilot")
st.caption(
    "Your AI study companion — plan revision, track exams, "
    "and organize your study time."
)

st.markdown(
    "StudyPilot helps you create realistic study plans, "
    "manage subjects, and prepare for upcoming exams."
)


# Sidebar
with st.sidebar:
    st.header("Settings")

    api_key = st.text_input(
        "Your Gemini API key",
        type="password",
        help="Get your key from Google AI Studio.",
    )

    st.markdown(
        "[Get a Gemini API key](https://aistudio.google.com/apikey)"
    )

    st.caption(
        "Your key is used for this session only. "
        "It is not stored in this project."
    )

    if st.button("Clear conversation"):
        st.session_state.chat = []
        st.session_state.history = []
        st.rerun()


# Initialize conversation memory
if "chat" not in st.session_state:
    st.session_state.chat = []

if "history" not in st.session_state:
    st.session_state.history = []


# Display previous messages
for role, message, tools_used in st.session_state.chat:
    with st.chat_message(role):
        st.write(message)

        if tools_used:
            with st.expander("🔧 Tools used"):
                for item in tools_used:
                    st.markdown(f"**{item['tool']}**")
                    st.caption(f"Input: {item['args']}")
                    st.caption(f"Result: {item['result']}")


# Welcome message
if not st.session_state.chat:
    st.info(
        "Try asking:\n\n"
        "- I have a DAA exam on 2026-12-10. How many days are left?\n"
        "- Split 12 hours between DAA, DBMS and OS.\n"
        "- Help me plan my revision for this week."
    )


# Chat input
question = st.chat_input("Ask StudyPilot anything about your studies...")

if question:

    # Display user message
    st.session_state.chat.append(
        ("user", question, None)
    )

    if not api_key:
        answer = "Please enter your Gemini API key in the sidebar first."
        used = []

    else:
        try:
            llm = assistant_core.make_llm(api_key)

            answer, used, new_history = assistant_core.run_turn(
                llm,
                st.session_state.history,
                question,
            )

            st.session_state.history = new_history

        except Exception as error:
            answer = (
                "Something went wrong. Please check your Gemini API key, "
                "internet connection, or try again later. "
                f"Error type: {type(error).__name__}"
            )
            used = []

    # Save answer to the displayed chat
    st.session_state.chat.append(
        ("assistant", answer, used)
    )

    st.rerun()
