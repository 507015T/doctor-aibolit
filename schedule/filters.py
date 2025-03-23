from .models import MedicationSchedule
from django_filters import rest_framework as filters


class MedicationScheduleFilter(filters.FilterSet):
    user_id = filters.NumberFilter(field_name="user_id")
    schedule_id = filters.NumberFilter(field_name="id")

    class Meta:
        model = MedicationSchedule
        fields = ["user_id", "schedule_id"]
