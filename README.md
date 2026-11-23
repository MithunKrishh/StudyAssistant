# StudyAssistant

StudyPilot is an AI-powered academic planning assistant that helps
students prepare for exams, organize revision, and manage study time.

## Features

- Conversational AI study assistant
- Remembers information during the active chat session
- Calculates days remaining until exams
- Divides study hours equally among subjects
- Generates personalized revision plans
- Shows which tools were used to answer
- Clear conversation option

## Tools

### days_until_exam
Calculates the number of days remaining until an exam using a given date.

Input format: YYYY-MM-DD

### split_study_hours
Divides total available study hours equally among a list of subjects.

## Technologies Used

- Python
- Streamlit
- LangChain
- Google Gemini

## Run Locally

1. Clone the repository.
2. Create a virtual environment.
3. Install requirements.
4. Run Streamlit.

```bash
pip install -r requirements.txt
streamlit run app.py
```

The user must provide their own Gemini API key in the application.

## Limitations

- Conversation memory lasts only during the current active session.
- Study-hour distribution is equal and does not automatically account
  for difficulty or subject priority.
- It does not access external websites or verify academic information.
- AI-generated study plans should be reviewed by the student.

## Developer Questions

### 1. How does StudyPilot remember the conversation?

StudyPilot stores the recent messages in Streamlit session state.
The conversation history is sent to Gemini with each new question,
allowing it to remember subjects, exam dates, and preferences.

### 2. Why did you create your own tools?

The tools handle exact calculations that the AI should not guess.
One calculates days until an exam, and the other distributes
study hours across subjects.
