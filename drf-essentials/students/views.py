from django.http import HttpResponse


# web application endpoint
def students(request):
    students = [
        {"id": 1, "name": "John Doe"},
    ]
    return HttpResponse(students)
