from django_filters import FilterSet, RangeFilter


class CustomBlogFilter(FilterSet):
    id = RangeFilter(field_name="id")
