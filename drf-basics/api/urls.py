from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("employees", views.EmployeeViewset, basename="employee")

urlpatterns = [
    path("", include(router.urls)),
    # students
    path("students/", views.studentsView),
    path("students/<str:id>/", views.studentDetailView),
    # blogs,comments
    path("blogs/", views.BlogsView.as_view()),
    path("comments/", views.CommentsView.as_view()),
    path("blogs/<int:id>/", views.BlogDetailView.as_view()),
    path("comments/<int:id>/", views.CommentDetailView.as_view()),
]
