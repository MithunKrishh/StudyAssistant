
# StudyAssistant Test Results

## Test 1 - Conversation Memory

Input:
"My DAA exam is on 2026-12-10 and I struggle with graph algorithms."

Follow-up:
"What subject is my exam and which topic do I struggle with?"

Expected:
The assistant remembers DAA and graph algorithms.

Actual:
[Record your actual result]

Status:
[PASS / FAIL]


## Test 2 - Exam Date Tool

Input:
"My exam is on 2026-12-10. How many days are left?"

Expected:
The days_until_exam tool is called and returns the correct number
of days remaining.

Actual:
[Record the tool call and answer]

Status:
[PASS / FAIL]


## Test 3 - Study Hours Tool

Input:
"Divide 12 hours equally between DAA, DBMS and OS."

Expected:
The split_study_hours tool is called and assigns 4 hours to
each subject.

Actual:
[Record the tool call and answer]

Status:
[PASS / FAIL]


## Test 4 - Normal Conversation

Input:
"How can I avoid distractions while studying?"

Expected:
The assistant gives useful study advice without calling a tool.

Actual:
[Record your actual result]

Status:
[PASS / FAIL]


## Test 5 - Out-of-Scope Question

Input:
"Explain how to repair a car engine."

Expected:
The assistant politely explains that it specializes in study planning
and cannot help with unrelated topics.

Actual:
[Record your actual result]

Status:
[PASS / FAIL]


## Test 6 - Tricky Input

Input:
"Divide -5 hours between DAA, OS and DBMS."

Expected:
The assistant uses the study-hours tool, identifies the invalid
input, and responds politely without crashing.

Actual:
[Record your actual result]

Status:
[PASS / FAIL]
