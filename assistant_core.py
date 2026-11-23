
from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langchain_google_genai import ChatGoogleGenerativeAI

from tools import TOOLS


CHAT_MODEL = "gemini-2.5-flash"

MAX_HISTORY = 20
MAX_STEPS = 4


SYSTEM_PROMPT = """
You are StudyPilot, a friendly and practical AI study planner.

YOUR JOB:
Help students organize revision, prepare for exams, divide study time,
understand study topics, and create realistic study schedules.

MEMORY:
Remember information shared during the current conversation, including:
- Subjects the student studies
- Exam dates
- Weak topics
- Available study hours
- Study preferences
- Their progress

Use the conversation history when answering follow-up questions.
Do not ask the student to repeat information they already shared.

TOOLS:
Use days_until_exam when calculating the number of days remaining
until a specific exam date.

Use split_study_hours when distributing study time across multiple
subjects.

Do not perform date or time calculations by guessing when a tool
can calculate them accurately.

LIMITS:
Stay focused on studying, exams, learning, and academic planning.

If the user asks something unrelated, politely explain that you are
StudyPilot and specialize in academic planning.

Do not invent exam dates, available hours, or student progress.

Make study plans realistic, with breaks and manageable workloads.

Be encouraging, but do not make answers unnecessarily long.

If a tool returns an error or invalid input, explain the problem
politely and ask the student to correct it.
"""


def make_llm(api_key):
    return ChatGoogleGenerativeAI(
        model=CHAT_MODEL,
        temperature=0.3,
        google_api_key=api_key,
    )


def text_of(content):
    """Convert Gemini's response into readable text."""
    if isinstance(content, str):
        return content

    return "".join(
        part.get("text", "") if isinstance(part, dict) else str(part)
        for part in content
    )


def run_turn(llm, history, question, system_prompt=SYSTEM_PROMPT):
    """Answer one question, call tools if needed, and update conversation history."""

    by_name = {tool.name: tool for tool in TOOLS}
    llm_with_tools = llm.bind_tools(TOOLS)

    messages = (
        [SystemMessage(content=system_prompt)]
        + history[-MAX_HISTORY:]
        + [HumanMessage(content=question)]
    )

    used = []
    answer = ""

    for _ in range(MAX_STEPS):
        ai = llm_with_tools.invoke(messages)
        messages.append(ai)

        # If Gemini gives a normal answer, stop.
        if not ai.tool_calls:
            answer = text_of(ai.content)
            break

        # If Gemini requests a tool, run it.
        for call in ai.tool_calls:
            tool = by_name.get(call["name"])

            if tool is None:
                result = ToolMessage(
                    content="Tool not found.",
                    tool_call_id=call["id"],
                    name=call["name"],
                )

            else:
                try:
                    result = tool.invoke(call)

                except Exception as error:
                    result = ToolMessage(
                        content=f"Tool error: {type(error).__name__}",
                        tool_call_id=call["id"],
                        name=call["name"],
                    )

            # Record which tool was used.
            used.append({
                "tool": call["name"],
                "args": call["args"],
                "result": str(result.content),
            })

            # Give the tool result back to Gemini.
            messages.append(result)

    if not answer:
        answer = (
            "I couldn't finish that request. "
            "Try asking in a simpler way."
        )

    # Store the conversation for future turns.
    new_history = (
        history
        + [
            HumanMessage(content=question),
            AIMessage(content=answer),
        ]
    )[-MAX_HISTORY:]

    return answer, used, new_history
