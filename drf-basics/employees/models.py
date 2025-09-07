from django.db import models


class Employee(models.Model):

    class Meta:
        db_table = "employees"

    id = models.CharField(max_length=20, primary_key=True)
    emp_name = models.CharField(max_length=50)
    designation = models.CharField(max_length=50)

    def __str__(self):
        return self.emp_name
