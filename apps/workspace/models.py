from django.db import models
from apps.users.models import User
from django.utils import timezone
from django.utils.text import slugify
from apps.workspace.choices import TaskPriorityChoices, TaskRewardChoices, TaskTypeChoices


class Workspace(models.Model):
    title = models.CharField(max_length=240)
    creator = models.ForeignKey(
        User, related_name='created_workspaces', on_delete=models.CASCADE
    )
    description = models.TextField(null=True, blank=True)
    icon = models.ImageField(upload_to='workspaces/icons', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    ceo = models.CharField(max_length=240, null=True, blank=True)
    headquarter = models.CharField(max_length=240, null=True, blank=True)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Workspace, self).save(*args, **kwargs)


class WorkspaceMember(models.Model):
    user = models.ForeignKey(User, related_name='workspaces', on_delete=models.CASCADE)
    workspace = models.ForeignKey(
        Workspace, related_name='members', on_delete=models.CASCADE
    )
    is_leader = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'workspace',)


class Invitation(models.Model):
    role_choices = (
        ('EMPLOYEE', 'employee'),
        ('MANAGER', 'manager'),
        ('LEADER', 'leader'),
    )
    workspace = models.ForeignKey(Workspace, related_name='invitations', on_delete=models.CASCADE)
    email = models.EmailField()
    invited_by = models.ForeignKey(User, related_name='invites', on_delete=models.SET_NULL, null=True)
    invited_at = models.DateTimeField(default=timezone.now)
    role = models.CharField(choices=role_choices, default='EMPLOYEE', max_length=100)


class Service(models.Model):
    workspace = models.ForeignKey(Workspace, related_name='services', on_delete=models.CASCADE)
    title = models.CharField(max_length=240)
    price = models.FloatField()
    description = models.TextField()

    def __str__(self):
        return self.title


class CaseStudy(models.Model):
    workspace = models.ForeignKey(Workspace, related_name='case_studies', on_delete=models.CASCADE)
    title = models.CharField(max_length=240)
    description = models.TextField()
    cover = models.ImageField(upload_to='workspaces/cover')


class Project(models.Model):
    user = models.ForeignKey(User, related_name='projects', on_delete=models.CASCADE)
    workspace = models.ForeignKey(Workspace, related_name='projects', on_delete=models.CASCADE)
    title = models.CharField(max_length=240, null=True, blank=True)
    description = models.TextField()
    service = models.ForeignKey(Service, related_name='projects', on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-id']


class Transaction(models.Model):
    user = models.ForeignKey(User, related_name='transactions', on_delete=models.CASCADE)
    workspace = models.ForeignKey(Workspace, related_name='transactions', on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    amount = models.FloatField(default=0)

    class Meta:
        ordering = ['-id']


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
    progress = models.PositiveIntegerField(default=0)
    reward = models.CharField(choices=reward_choices.choices(), default=reward_choices.P10.value, max_length=100)
    is_pending = models.BooleanField(default=True)
    # predefined tutorial id (foreign key behaviour)
    # tutorial = models.CharField(max_length=100, null=True, blank=True)
    project = models.ForeignKey(
        Project, related_name='tasks', on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        ordering = ['-id']


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

    
class TaskComment(models.Model):
    task = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='task_comments', on_delete=models.CASCADE)
    internal_chat = models.BooleanField(default=True)
    text = models.TextField()


class Notifications(models.Model):
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    text = models.TextField()
    seen = models.BooleanField(default=False)
    workspace = models.ForeignKey(Workspace, related_name='notifications', on_delete=models.CASCADE)

    class Meta:
        ordering = ["-id"] 

