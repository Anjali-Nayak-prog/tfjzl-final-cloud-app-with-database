from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User

from .models import Course, Enrollment, Question, Choice, Submission


def extract_answers(request):
    """
    Extract selected choice IDs from the submitted exam form.
    """
    submitted_answers = []

    for key in request.POST:
        if key.startswith('choice'):
            value = request.POST[key]
            submitted_answers.append(int(value))

    return submitted_answers


def submit(request, course_id):
    """
    Create an exam submission for the current user's enrollment
    and save the selected choices.
    """

    course = get_object_or_404(Course, pk=course_id)
    user = request.user

    enrollment = get_object_or_404(
        Enrollment,
        user=user,
        course=course
    )

    submission = Submission.objects.create(
        enrollment=enrollment
    )

    selected_choice_ids = extract_answers(request)

    choices = Choice.objects.filter(
        id__in=selected_choice_ids
    )

    submission.choices.set(choices)

    return redirect(
        'show_exam_result',
        course_id=course.id,
        submission_id=submission.id
    )


def show_exam_result(request, course_id, submission_id):
    """
    Calculate and display the learner's exam result.
    """

    course = get_object_or_404(Course, pk=course_id)

    submission = get_object_or_404(
        Submission,
        pk=submission_id
    )

    selected_choices = submission.choices.all()

    total_score = 0

    # Get all lessons belonging to the course
    lessons = course.lesson_set.all()

    # Get all questions belonging to those lessons
    questions = Question.objects.filter(
        lesson__in=lessons
    )

    for question in questions:

        correct_choices = set(
            question.choice_set.filter(
                is_correct=True
            )
        )

        selected_for_question = set(
            selected_choices.filter(
                question=question
            )
        )

        # Award the question's grade only when
        # all correct choices are selected.
        if correct_choices == selected_for_question:
            total_score += question.grade

    context = {
        'course': course,
        'grade': total_score,
        'choices': selected_choices,
        'questions': questions,
    }

    return render(
        request,
        'onlinecourseapp/exam_result_bootstrap.html',
        context
    )