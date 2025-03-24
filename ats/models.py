# ats/models.py (for Application model)
from django.db import models
from user.models import User, Resume
from recruiter.models import Job

class Application(models.Model):
    application_id = models.CharField(primary_key=True, max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    matching_rate = models.DecimalField(max_digits=5, decimal_places=2)
    apply_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.application_id


class Selection(models.Model):
    selection_id = models.CharField(primary_key=True, max_length=50)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='selections')
    selection_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.selection_id
