from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render

from .models import Course, Enrollment, Submission


def course_details_bootstrap(request, course_id):
	"""Render a Bootstrap course details page with lessons and exam questions."""
	course = get_object_or_404(Course, pk=course_id)
	enrollment = Enrollment.objects.filter(course=course, user=request.user).first()
	return render(
		request,
		"onlinecourse/course_details_bootstrap.html",
		{"course": course, "enrollment": enrollment},
	)


def submit(request, course_id):
	"""Create a submission from selected exam choices and show results."""
	if request.method != "POST":
		return HttpResponseBadRequest("Invalid request method.")

	enrollment_id = request.POST.get("enrollment_id")
	if not enrollment_id:
		return HttpResponseBadRequest("Missing enrollment id.")

	enrollment = get_object_or_404(Enrollment, pk=enrollment_id, course_id=course_id)
	selected_choices = request.POST.getlist("choice")

	submission = Submission.objects.create(enrollment=enrollment)
	if selected_choices:
		submission.choices.set(selected_choices)

	return show_exam_result(request, course_id, enrollment.id, submission.id)


def show_exam_result(request, course_id, enrollment_id, submission_id):
	"""Calculate and render exam score for a submission."""
	course = get_object_or_404(Course, pk=course_id)
	enrollment = get_object_or_404(Enrollment, pk=enrollment_id, course=course)
	submission = get_object_or_404(Submission, pk=submission_id, enrollment=enrollment)

	selected_ids = set(submission.choices.values_list("id", flat=True))
	total_grade = 0
	earned_grade = 0
	detailed_results = []

	for question in course.questions.prefetch_related("choices").all():
		question_choices = list(question.choices.all())
		question_choice_ids = {choice.id for choice in question_choices}
		chosen_for_question = selected_ids.intersection(question_choice_ids)
		correct_ids = {choice.id for choice in question_choices if choice.is_correct}

		question_score = question.grade
		total_grade += question_score
		is_correct = chosen_for_question == correct_ids
		if is_correct:
			earned_grade += question_score

		detailed_results.append(
			{
				"question": question,
				"choices": question_choices,
				"chosen_ids": chosen_for_question,
				"correct_ids": correct_ids,
				"is_correct": is_correct,
			}
		)

	score = round((earned_grade / total_grade) * 100, 2) if total_grade else 0

	return render(
		request,
		"onlinecourse/exam_result.html",
		{
			"course": course,
			"submission": submission,
			"score": score,
			"earned_grade": earned_grade,
			"total_grade": total_grade,
			"results": detailed_results,
		},
	)
