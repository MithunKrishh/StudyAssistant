
from datetime import date
from langchain_core.tools import tool


@tool
def days_until_exam(exam_date: str) -> str:
    """Calculate the number of days remaining until an exam. Use when the student provides an exam date in YYYY-MM-DD format."""
    try:
        exam = date.fromisoformat(exam_date)
        today = date.today()
        days = (exam - today).days

        if days < 0:
            return f"The exam date was {-days} day(s) ago."

        if days == 0:
            return "The exam is today!"

        return f"{days} day(s) remaining until the exam."

    except ValueError:
        return "Invalid date. Please use YYYY-MM-DD format, for example 2026-12-10."


@tool
def split_study_hours(total_hours: float, subjects: str) -> str:
    """Divide total available study hours equally among the subjects provided as a comma-separated list. Use when a student asks to distribute revision time across subjects."""
    try:
        hours = float(total_hours)

        subject_list = [
            subject.strip()
            for subject in subjects.split(",")
            if subject.strip()
        ]

        if hours <= 0:
            return "Study hours must be greater than zero."

        if not subject_list:
            return "Please provide at least one subject."

        per_subject = hours / len(subject_list)

        result = f"Total study time: {hours} hours\n"
        result += f"Number of subjects: {len(subject_list)}\n"
        result += f"Each subject gets: {per_subject:.2f} hours\n\n"

        for subject in subject_list:
            result += f"- {subject}: {per_subject:.2f} hours\n"

        return result

    except (ValueError, TypeError):
        return "Invalid study hours. Please provide a valid number."


TOOLS = [days_until_exam, split_study_hours]
