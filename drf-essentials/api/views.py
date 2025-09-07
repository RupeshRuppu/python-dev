from students.models import Student
from employees.models import Employee
from rest_framework.response import Response
from api.serializers import StudentSerializer, EmployeeSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    # RetrieveDestroyAPIView,
)
from rest_framework.viewsets import ViewSet, ModelViewSet
from blogs.models import Blog, Comment
from blogs.serializers import BlogSerializer, CommentSerializer

# # Create your views here.
# def studentsView(request):
#     students = Student.objects.all().values()
#     students_list = list(students)
#     return JsonResponse(students_list, safe=False)


# function based views
@api_view(["GET", "POST"])
def studentsView(request):
    if request.method == "GET":
        students = Student.objects.all().order_by("id")
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def studentsDetailView(request, id):
    try:
        student = Student.objects.get(pk=id)
    except Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = StudentSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        student_data = StudentSerializer(student).data
        data = {**student_data, **request.data}
        serializer = StudentSerializer(student, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class based views
class Employees(APIView):
    def get(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeDetailsView(APIView):

    def get_object(self, pk):
        try:
            employee = Employee.objects.get(pk=pk)
            return employee
        except Employee.DoesNotExist:
            raise Http404

    def get(self, request, id):
        employee = self.get_object(id)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        employee = self.get_object(id)
        employee_data = EmployeeSerializer(employee).data
        data = {**employee_data, **request.data}
        serializer = EmployeeSerializer(employee, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        employee = self.get_object(id)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""
Mixins
    - ListModelMixin - list()
    - CreateModelMixin - create()
    - RetriewModelMixin - retrieve()
    - UpdateModelMixin - update()
    - DestroyModelMixin - destroy()
"""


class EmployeesMixin(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class EmployeeDetailsViewMixin(
    DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericAPIView
):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = "id"

    def get(self, request, id):
        return self.retrieve(request, id)

    # override & add our functionality
    def update(self, request, id):
        employee = get_object_or_404(Employee, pk=id)
        employee_data = EmployeeSerializer(employee).data
        data = {**employee_data, **request.data}
        serializer = EmployeeSerializer(employee, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        return self.update(request, id)

    def delete(self, request, id):
        return self.destroy(request, id)


"""
GENERICS
    - ListAPIView - listing objects
    - CreateAPIView - creating the objects
    - RetrieveAPIView - retrieve a single object using pk
    - UpdateAPIView - updating a single object using pk
    - DestroyAPIView - deleting a single object using pk

    - ListCreateAPIView
    - RetrieveUpdateAPIView
    - RetrieveUpdateDestroyAPIView
"""


class EmployeesGenerics(ListAPIView, CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeesDetailsGenerics(RetrieveAPIView, DestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = "id"


# patch available
class EmployeesGenericsCombined(ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeesDetailsGenericsCombined(RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = "id"


# view-sets
# it's a subset of views it combines the functionalities
# of both views & serializers
#
# we can extens viewsets.ViewSet, viewsets.ModelViewSet
# in case of viewsets.ViewSet - provide list, create, retrieve, update & delete
# in case of viewsets.ModelViewSet we just need to provide the serializer & queryset


class EmployeeViewSet(ViewSet):
    def list(self, request):
        queryset = Employee.objects.all()
        serializer = EmployeeSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        employee = get_object_or_404(Employee, pk=pk)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        employee_data = EmployeeSerializer(employee).data
        data = {**employee_data, **request.data}
        serializer = EmployeeSerializer(employee, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# here patch is also available
class EmployeeModelViewSet(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


# blogs & comments views
class BlogsView(ListCreateAPIView):
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()


class BlogsDetailedView(RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    lookup_field = "id"


class CommentView(ListCreateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


class CommentsDetailedView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = "id"
