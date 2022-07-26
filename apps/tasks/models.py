from django.db import models
from django.utils import timezone
from apps.tasks.choices import TaskPriorityChoices, TaskRewardChoices, TaskTypeChoices

from apps.users.models import User


class Task(models.Model):
    type_choices = TaskTypeChoices
    priority_choices = TaskPriorityChoices
    reward_choices = TaskRewardChoices
    title = models.CharField(max_length=150, null=True, blank=True)
    assignor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    assignee = models.ForeignKey(User, related_name="tasks", on_delete=models.SET_NULL, null=True, blank=True)
    assigned_at = models.DateTimeField(default=timezone.now)
    deadline_at = models.DateTimeField(null=True, blank=True)
    type = models.CharField(choices=type_choices.choices(), default=type_choices.GENERAL.value, max_length=100)
    priority = models.CharField(choices=priority_choices.choices(), default=priority_choices.LOW.value, max_length=100)
    progress = models.PositiveIntegerField()
    reward = models.CharField(choices=reward_choices.choices(), default=reward_choices.P10.value, max_length=100)
    is_pending = models.BooleanField(default=True)
    # predefined tutorial id (foreign key behaviour)
    tutorial = models.CharField(max_length=100, null=True, blank=True)


class Feedback(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(
        User, related_name="feedbacks", on_delete=models.CASCADE, null=True, blank=True
    )
    rating = models.PositiveIntegerField()
    title = models.CharField(max_length=50, null=True, blank=True)
    text = models.TextField(max_length=1000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    task = models.OneToOneField(Task, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["-id",]

    def __str__(self):
        return str(self.title)