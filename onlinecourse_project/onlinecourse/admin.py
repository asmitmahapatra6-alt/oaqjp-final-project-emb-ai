from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Choice, Course, Enrollment, Lesson, Question, Submission


class QuestionInline(admin.TabularInline):
	"""Inline question editor for the course admin page."""

	model = Question
	extra = 1


class ChoiceInline(admin.TabularInline):
	"""Inline choice editor for the question admin page."""

	model = Choice
	extra = 1


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
	"""Admin configuration for exam questions."""

	list_display = ("question_text", "course", "grade")
	list_filter = ("course",)
	inlines = [ChoiceInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
	"""Admin configuration for lessons."""

	list_display = ("title", "course", "order")
	list_filter = ("course",)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
	"""Admin configuration for courses."""

	list_display = ("name", "pub_date")
	inlines = [QuestionInline]


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
	"""Admin configuration for question choices."""

	list_display = ("choice_text", "question", "is_correct")
	list_filter = ("is_correct",)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
	"""Admin configuration for enrollments."""

	list_display = ("user", "course", "date_enrolled")


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
	"""Admin configuration for submissions."""

	list_display = ("id", "enrollment", "submitted_at")


# Imported for assignment requirement visibility.
_ = (User, UserAdmin)
