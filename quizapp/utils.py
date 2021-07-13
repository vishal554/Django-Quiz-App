
from quizapp.models import FibQuestion, McqQuestion, Question, UsersAnswer


def get_data_of_quiz(quiz_id, username):
    marks_weightage = []
    u_answer = []
    correct_answer = []

    question_ids = Question.objects.filter(quiz_id=quiz_id)

    for i in question_ids:
        u_a = UsersAnswer.objects.get(
            username=username, question_id=i.question_id)
        u_answer.append(u_a.answer)
        marks_weightage.append(i.marks_weightage)
        if i.type == "MCQ":
            correct_answer.append(McqQuestion.objects.get(
                question_id=i.question_id).answer)
        else:
            correct_answer.append(FibQuestion.objects.get(
                question_id=i.question_id).answer)

    marks_obt = 0
    for i in range(len(u_answer)):
        if u_answer[i] == correct_answer[i]:
            marks_obt += marks_weightage[i]

    total_marks = sum(marks_weightage)
    perct = ((marks_obt/total_marks) * 100)

    context = {
        'marks_obtained': marks_obt,
        'total_marks': total_marks,
        'percentage': perct,
        'questions': question_ids,
        'UsersAnswer': u_answer,
        'correct_answer': correct_answer,
    }

    return context

def get_question_choice_set(quiz_id):
    # Get the Question and choices set
    question_set = Question.objects.filter(quiz_id=quiz_id)
    question_choice_set = {}
    time_limit = 0
    for i in question_set:
        time_limit += i.time_weightage
        if i.type == "MCQ":
            question_choice_set[i] = McqQuestion.objects.get(
                question_id=i.question_id)
        elif i.type == "FIB":
            question_choice_set[i] = 'FIB'
    return question_choice_set, time_limit

