from django.http import HttpResponse

# Create your views here.


def students(req):
    student = [{"id": 1, "name": "rupesh", "age": 23}]
    return HttpResponse(student)
