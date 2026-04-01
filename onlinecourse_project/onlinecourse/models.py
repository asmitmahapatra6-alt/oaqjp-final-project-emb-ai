from django.contrib.auth.models import User
from django.db import models


class Course(models.Model):
	"""A course available in the online learning platform."""

	name = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	pub_date = models.DateField(null=True, blank=True)

	def __str__(self) -> str:
		return self.name


class Lesson(models.Model):
	"""A lesson that belongs to a course."""

	course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
	title = models.CharField(max_length=200)
	content = models.TextField(blank=True)
	order = models.PositiveIntegerField(default=0)

	class Meta:
		ordering = ["order", "id"]

	def __str__(self) -> str:
		return f"{self.course.name} - {self.title}"


class Enrollment(models.Model):
	"""A user enrolled in a course."""

	user = models.ForeignKey(User, on_delete=models.CASCADE)
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	date_enrolled = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ("user", "course")

	def __str__(self) -> str:
		return f"{self.user.username} enrolled in {self.course.name}"


class Question(models.Model):
	"""An exam question associated with a course."""

	course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="questions")
	question_text = models.CharField(max_length=500)
	grade = models.PositiveIntegerField(default=1)

	def __str__(self) -> str:
		return self.question_text


class Choice(models.Model):
	"""A selectable answer for a question."""

	question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
	choice_text = models.CharField(max_length=300)
	is_correct = models.BooleanField(default=False)

	def __str__(self) -> str:
		return self.choice_text


class Submission(models.Model):
	"""Stores a learner's selected answers for an exam attempt."""

	enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name="submissions")
	choices = models.ManyToManyField(Choice)
	submitted_at = models.DateTimeField(auto_now_add=True)

	def __str__(self) -> str:
		return f"Submission {self.id} for {self.enrollment}"
