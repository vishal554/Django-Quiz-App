from django.views import View
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, render
from quizapp.utils import get_data_of_quiz, get_question_choice_set
from quizapp.models import *


# Create your views here.

class HomeView(View):
    """
    renders the Register page to the User

    **Context**

    ``form``
        instance of UserRegisterForm class

    **Template:**

    :template:`users/register.html`

    """

    def get(self, request):
        username = request.user
        if not username:
            redirect('login')
        all_quizes = Quiz.objects.all()

        ongoing_quiz_id = []
        all_quiz_id = []
        taken_quizes = []

        if not (request.user.is_authenticated):
            return render(request, 'users/index.html', {"Quizes": all_quizes})

        ongoings = Taken.objects.filter(username=username, submitted=False)
        taken_quiz_id = Taken.objects.filter(username=username, submitted=True)

        for quiz in ongoings:
            ongoing_quiz_id.append(str(quiz.quiz_id.quiz_id))

        for quiz in taken_quiz_id:
            taken_quizes.append(str(quiz.quiz_id.quiz_id))

        for quiz in all_quizes:
            all_quiz_id.append(str(quiz.quiz_id))

        # Remove the ongoing and taken quizes from available quiz list
        for quiz in list(all_quiz_id):
            if quiz in ongoing_quiz_id:
                all_quiz_id.remove(quiz)
            if quiz in taken_quizes:
                all_quiz_id.remove(quiz)

        # Get all the available Quiz object from quiz ids
        available_quizes = []
        for quiz_id in all_quiz_id:
            available_quizes.append(Quiz.objects.get(quiz_id=quiz_id))

        # Get all the Quiz object from ongoing quiz ids
        ongoings = []
        for quiz_id in ongoing_quizes:
            ongoings.append(Quiz.objects.get(quiz_id=quiz_id))

        return render(request, 'users/index.html', {"Quizes": quizes, "ongoing_quizes": ongoings})


class TakeQuizView(View):
    """
    renders the TakeQuiz page to the User

    **Context**
    
    'quiz_id': quiz_id of current quiz
    'question': question object
    'choices': choices set
    'time_limit': time limit 
    'total_questions': number of total questions
    'current': current question number
    
    """

    def get(self, request):
        continuing = False
        quiz_id = request.GET.get('quiz_id')
        question_choice_set, time_limit = get_question_choice_set(quiz_id)
        total_questions = len(list(question_choice_set))
        print(question_choice_set)

        # check if the user is continuing the quiz
        username = request.user
        print(request.user.is_authenticated)
        if not username.is_authenticated:
            return redirect('login')
        user_answers = UsersAnswer.objects.filter(username=username)
        question_ids = Question.objects.filter(quiz_id=quiz_id)
        q_id_list = []

        for i in question_ids:
            q_id_list.append(str(i.question_id))

        for i in user_answers:
            if str(i.question_id.question_id) in q_id_list:
                if i.question_id in list(question_choice_set):
                    del question_choice_set[i.question_id]
                continuing = True

        if continuing:
            taken = Taken.objects.get(username=username, quiz_id=quiz_id)
            time_limit = int(taken.time_taken)

        current_question_number = (
            total_questions - len(list(question_choice_set))) + 1

        try:
            (question, choices) = next(iter(question_choice_set.items()))
        except:
            return redirect('profile')

        context = {
            'quiz_id': quiz_id,
            'question': question, 
            'choices': choices, 
            'time_limit': time_limit,
            'total_questions': total_questions, 
            'current': current_question_number
        }

        if len(list(question_choice_set)) > 1:
            context['last'] = 'no'
            return render(request, 'users/take_quiz.html', context)
        elif len(list(question_choice_set)) == 1:
            context['last'] = 'yes'
            return render(request, 'users/take_quiz.html', context)


@method_decorator(login_required, name='dispatch')
class ResultsView(View):
    """
    Shows the result of the quiz after the

    user has submitted the quiz.

    **Context**

    'marks_obtained': The Marks obtained by the user,
    'total_marks': the Total marks of the quiz,
    'percentage': Percentage of the user,
    'questions': QuerySet of the question objects present in the quiz,
    'UsersAnswer': The answer user has given,
    'correct_answer': The correct answer of the question
    'time_taken': the time taken by the user

    **Template:**

    :template:'users/results.html'

    """

    template_name = 'users/results.html'

    def post(self, request):

        try:
            quiz_id = request.POST.get('quiz_id')
            username = request.user
            question_id = request.POST['question_id']
            last = request.POST.get('last', '')
            time_taken = request.POST['time_remaining']
            if request.is_ajax():
                answer = request.POST.get('choice', '')
            else:
                answer = request.POST.get('btnradio', '')
        except:
            return redirect('login')

        # add the last question to the UsersAnswer Model
        question_instance = Question.objects.filter(
            question_id=question_id).get()
        # check if the answer already exists
        try:
            if(UsersAnswer.objects.get(username=username, question_id=question_instance)):
                UsersAnswer.objects.filter(
                    username=username, question_id=question_instance).update(answer=answer)
        except:
            UsersAnswer.objects.create(
                username=username, question_id=question_instance, answer=answer)

        question_ids = Question.objects.filter(quiz_id=quiz_id)

        # add answers to the questions as empty that user has not attempted
        if last == 'no':
            user_answers = UsersAnswer.objects.filter(username=username)
            user_answered = []
            for i in user_answers:
                user_answered.append(i.question_id)

            for i in question_ids:
                if i not in user_answered:
                    UsersAnswer.objects.create(
                        username=username, question_id=i, answer="")

        # Fetch the correct answers and also the answer user has given
        quiz_ins = Quiz.objects.get(quiz_id=quiz_id)

        # get context from the function
        context = get_data_of_quiz(quiz_id, username)

        # check if the Taken object already exists or not
        try:
            if Taken.objects.get(username=username, quiz_id=quiz_ins):
                Taken.objects.filter(username=username, quiz_id=quiz_ins).update(
                    marks_obtained=context['marks_obtained'], time_taken=time_taken, submitted=True)

        except:
            Taken.objects.create(username=username, quiz_id=quiz_ins,
                                 submitted=True, marks_obtained=context['marks_obtained'], time_taken=time_taken)

        if request.is_ajax():
            print('inside ajax')
            return JsonResponse({})
        return render(request, 'users/results.html', context)


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    """
    Shows the quizes submitted by the user

    **Context**

    'marks_obtained': The Marks obtained by the user,
    'total_marks': the Total marks of the quiz,
    'percentage': Percentage of the user,
    'questions': QuerySet of the question objects present in the quiz,
    'UsersAnswer': The answer user has given,
    'correct_answer': The correct answer of the question

    **Template:**

    :template:'users/results.html'

    **Template:**

    :template: 'users/results.html'

    """

    template_name = 'users/results.html'

    def get(self, request):
        username = request.user
        taken = Taken.objects.filter(username=username, submitted=True)
        quizes = []
        for i in taken:
            quizes.append(i.quiz_id)

        context = {
            'taken': taken,
            'quizes': quizes
        }

        return render(request, 'users/profile.html', context)

    def post(self, request):
        # shows the details of the quiz submitted by
        # the user in the results template
        try:
            quiz_id = request.POST['quiz_id']
            username = request.user
        except:
            return redirect('login')

        context = get_data_of_quiz(quiz_id, username)
        return render(request, self.template_name, context)


def save_and_cont_later(request):
    """
    Saves the state so that user can login 

    later and continue with the quiz.

    """

    if request.method == "POST" and request.is_ajax():

        # Getting post data
        username = request.user
        question_id = request.POST['question_id']
        answer = request.POST.get('choice', '')
        time_rem = int(request.POST['time_remaining'])
        quiz_id = request.POST['quiz_id']
        last = request.POST.get('last', 'no')

        # Add the answer to the UsersAnswer model
        question_instance = Question.objects.filter(
            question_id=question_id).get()
        try:
            if(UsersAnswer.objects.get(username=username, question_id=question_instance)):
                UsersAnswer.objects.filter(
                    username=username, question_id=question_instance).update(answer=answer)
        except:
            UsersAnswer.objects.create(
                username=username, question_id=question_instance, answer=answer)

        quiz_id_ins = Quiz.objects.get(quiz_id=quiz_id)

        # check if the question is the last question of the quiz.
        # If it is then submit the quiz
        if last == 'yes':
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

            # check if the user has already saved this quiz before or not
            try:
                if Taken.objects.get(username=username, quiz_id=quiz_id_ins, submitted=False):
                    Taken.objects.filter(username=username, quiz_id=quiz_id_ins, submitted=False).update(
                        submitted=True, marks_obtained=marks_obt, time_taken=time_rem)
            except:
                Taken.objects.create(username=username, quiz_id=quiz_id_ins,
                                     submitted=True, marks_obtained=marks_obt, time_taken=time_rem)
        else:

            # check if the user has already saved this quiz before or not
            try:
                if Taken.objects.get(username=username, quiz_id=quiz_id_ins, submitted=False):
                    Taken.objects.filter(username=username, quiz_id=quiz_id_ins).update(
                        time_taken=time_rem)
            except:
                Taken.objects.create(username=username, quiz_id=quiz_id_ins,
                                     submitted=False, marks_obtained=0, time_taken=time_rem)

        return render(request, 'users/logout.html')


def save_data(request):
    """
    Saves the data to the UsersAnswer Model

    and sends the next question to the page

    via JsonResponse.

    """
    # Get the questions and choice set

    quiz_id = request.POST['quiz_id']
    question_choice_set, time_limit = get_question_choice_set(quiz_id)
    total_questions = len(list(question_choice_set))

    if request.method == "POST" and request.is_ajax():
        # Add the answer to the UsersAnswers model
        username = request.user
        question_id = request.POST['question_id']
        answer = request.POST['choice']

        question_instance = Question.objects.filter(
            question_id=question_id).get()
        try:
            if(UsersAnswer.objects.get(username=username, question_id=question_instance)):
                UsersAnswer.objects.filter(
                    username=username, question_id=question_instance).update(answer=answer)
        except:
            UsersAnswer.objects.create(
                username=username, question_id=question_instance, answer=answer)

        # Get Attempted Questions
        u_answers = UsersAnswer.objects.filter(username=username)
        q_id_list = []
        for i in u_answers:
            q_id_list.append(str(i.question_id.question_id))

        # Delete Attempted questions from the main set of questions
        question_choice_set_copy = question_choice_set
        for i in list(question_choice_set_copy):
            if str(i.question_id) in q_id_list:
                del question_choice_set[i]

        # get the first Key-value pair
        try:
            (question, choices) = next(iter(question_choice_set.items()))
        except:
            return redirect('profile')

        current_question_number = (
            total_questions - len(list(question_choice_set))) + 1

        #convert the model to Dictionary
        question_obj = model_to_dict(question)
        question_obj['question_id'] = question.question_id

        # check if the question is the last question
        if len(list(question_choice_set)) > 1:
            if str(question.type) == 'MCQ':
                choices_obj = model_to_dict(choices)
                return JsonResponse({'question': question_obj, 'choices': choices_obj, 'last': 'no', 'total_questions': total_questions, 'current': current_question_number})
            else:
                return JsonResponse({'question': question_obj, 'choices': '__none', 'last': 'no', 'total_questions': total_questions, 'current': current_question_number})

        elif len(list(question_choice_set)) == 1:
            if str(question.type) == 'MCQ':
                choices_obj = model_to_dict(choices)
                return JsonResponse({'question': question_obj, 'choices': choices_obj, 'last': 'yes', 'total_questions': total_questions, 'current': current_question_number})
            else:
                return JsonResponse({'question': question_obj, 'choices': '__none', 'last': 'yes', 'total_questions': total_questions, 'current': current_question_number})

        else:
            return redirect('profile')
