from django.db import models
from django.contrib.auth.models import User

# Create your models here.

from django.db import models

class Assignment(models.Model):
    STATUS_CHOICES = [
        ('Not Started', 'Not Started'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    module_name = models.CharField(max_length=100)
    assignment_name = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Not Started')

    def __str__(self):
        return self.assignment_name
