from django.shortcuts import get_object_or_404
from students.models import Student
from employees.models import Employee
from .serializers import StudentSerializer, EmployeeSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import mixins, generics, viewsets
from blogs.models import Blog, Comment
from blogs.serializers import BlogSerializer, CommentSerializer
from api.paginations import CustomEmployeePagination, CustomBlogPagination
from employees.filters import CustomEmployeeFilter
from blogs.filters import CustomBlogFilter
from rest_framework.filters import SearchFilter, OrderingFilter


@api_view(["GET", "POST"])
def studentsView(req):
    if req.method == "GET":
        # get all students from table
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif req.method == "POST":
        serializer = StudentSerializer(data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def studentDetailView(req, id):
    try:
        student = Student.objects.get(id=id)
    except Student.DoesNotExist:
        return Response(
            {"message": f"No student present with id {id}"},
            status=status.HTTP_404_NOT_FOUND,
        )

    if req.method == "GET":
        serializer = StudentSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif req.method == "PUT":
        student_data = StudentSerializer(student).data
        data = {**student_data, **req.data}
        # to update resource pass it like this. (record & upadated data)
        serializer = StudentSerializer(student, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif req.method == "DELETE":
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class based views
"""
class Employees(APIView):
    def get(self, _):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, req):
        serializer = EmployeeSerializer(data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeDetail(APIView):
    def get_object(self, id):
        try:
            employee = Employee.objects.get(id=id)
            return employee
        except Employee.DoesNotExist:
            raise Http404

    def get(self, _, id):
        employee = self.get_object(id)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, req, id):
        employee = self.get_object(id)
        employee_data = EmployeeSerializer(employee).data
        data = {**employee_data, **req.data}
        serializer = EmployeeSerializer(employee, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, _, id):
        employee = self.get_object(id)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
"""

# mixins
"""
class Employees(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get(self, req):
        return self.list(req)

    def post(self, req):
        return self.create(req)


class EmployeeDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = "id"

    def update(self, request, id):
        try:
            employee = Employee.objects.get(id=id)
        except Employee.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        employee_data = EmployeeSerializer(employee).data
        data = {**employee_data, **request.data}
        serializer = EmployeeSerializer(employee, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # primary key based operations
    def get(self, req, id):
        return self.retrieve(req, id)

    def put(self, req, id):
        # self.update(req, id) does the job but needs complete resource object.
        return self.update(req, id)

    def delete(self, req, id):
        return self.destroy(req, id)
"""


"""
# generics
# class Employees(generics.ListAPIView, generics.CreateAPIView):
class Employees(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = "id"
"""

# viewsets.ViewSet
"""
class EmployeeViewset(viewsets.ViewSet):
    def list(self, req):
        queryset = Employee.objects.all()
        serializer = EmployeeSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, req):
        serializer = EmployeeSerializer(data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, req, pk=None):
        employee = get_object_or_404(Employee, pk=pk)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, req, pk=None):
        employee = get_object_or_404(Employee, pk=pk)
        serializer = EmployeeSerializer(employee, data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, req, pk):
        employee = get_object_or_404(Employee, pk=pk)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
"""


class EmployeeViewset(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    pagination_class = CustomEmployeePagination
    filterset_class = CustomEmployeeFilter


class BlogsView(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    # filterset_class = CustomBlogFilter
    pagination_class = CustomBlogPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["title", "body"]
    ordering_fields = ["id"]
    pagination_class = None


class CommentsView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class BlogDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    lookup_field = "id"


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = "id"
