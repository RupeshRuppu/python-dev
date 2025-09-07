from django.db import models
from uuid import uuid4

# Create your models here.


class Employee(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)
    emp_id = models.CharField(max_length=20)
    emp_name = models.CharField(max_length=50)
    designation = models.CharField(max_length=50)

    def __str__(self):
        return self.emp_name
