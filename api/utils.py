
from quizapp.models import McqQuestion, Question


def get_question_choice_set(quiz_id):
    
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