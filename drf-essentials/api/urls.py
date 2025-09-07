from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("employees", views.EmployeeViewSet, basename="employee")

router2 = DefaultRouter()
router2.register("employees", views.EmployeeModelViewSet)


urlpatterns = [
    path("students/", views.studentsView),
    path("students/<int:id>/", views.studentsDetailView),
    # employees class based views
    path("employees/", views.Employees.as_view()),
    path("employees/<str:id>/", views.EmployeeDetailsView.as_view()),
    # employees - mixins
    path("employees-mixins/", views.EmployeesMixin.as_view()),
    path("employees-mixins/<str:id>/", views.EmployeeDetailsViewMixin.as_view()),
    # employees - generics
    path("employees-generics/", views.EmployeesGenerics.as_view()),
    path("employees-generics/<str:id>/", views.EmployeesDetailsGenerics.as_view()),
    # employees - generics-combined-classes
    path("employees-generics-combined/", views.EmployeesGenericsCombined.as_view()),
    path(
        "employees-generics-combined/<str:id>/",
        views.EmployeesDetailsGenericsCombined.as_view(),
    ),
    path("viewset/", include(router.urls)),
    path("modelviewset/", include(router2.urls)),
    # blogs, comments
    path("blogs/", views.BlogsView.as_view()),
    path("blogs/<int:id>/", views.BlogsDetailedView.as_view()),
    path("comments/", views.CommentView.as_view()),
    path("comments/<int:id>/", views.CommentsDetailedView.as_view()),
]
