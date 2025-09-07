import django_filters


class CustomEmployeeFilter(django_filters.FilterSet):
    designation = django_filters.CharFilter(
        field_name="designation", lookup_expr="iexact"
    )
    emp_name = django_filters.CharFilter(field_name="emp_name", lookup_expr="icontains")
    emp_id_min = django_filters.CharFilter(
        method="filter_by_empid", label="FROM EMP ID"
    )
    emp_id_max = django_filters.CharFilter(method="filter_by_empid", label="TO EMP ID")

    def filter_by_empid(self, qs, name, value):
        if name == "emp_id_min":
            return qs.filter(id__gte=value)
        elif name == "emp_id_max":
            return qs.filter(id__lte=value)
        return qs
