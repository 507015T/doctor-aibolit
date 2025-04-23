from datetime import datetime, time, date, timedelta
from typing import List
from django.conf import settings
from django.db.models import Q
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404
from .models import MedicationSchedule
from .serializers import MedicationScheduleSerializer


class MedicationScheduleService:
    @staticmethod
    def create_schedule(data: dict) -> MedicationSchedule:
        serializer = MedicationScheduleSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer.save()


    @staticmethod
    def get_schedules_for_user(user_id: int) -> List[int]:
        queryset = MedicationSchedule.objects.filter(
            Q(end_date__gte=date.today()) | Q(end_date__isnull=True), user_id=user_id
        )
        return list(queryset.values_list("id", flat=True))

    @staticmethod
    def get_schedule(user_id: int, schedule_id: int) -> MedicationSchedule:
        instance = get_object_or_404(
            MedicationSchedule, pk=schedule_id, user_id=user_id
        )

        if instance.end_date and instance.end_date < date.today():
            raise NotFound(
                {
                    "response": f"The medication '{instance.medication_name}' intake ended on {instance.end_date}"
                }
            )
        return instance

    @staticmethod
    def get_upcoming_takings(schedules_data, current_time, time_limit):
        def is_within_timeframe(time_str):
            time_obj = datetime.strptime(time_str, "%H:%M").time()
            return (
                time(8, 0) <= time_obj <= time(22, 0)
                and current_time.time() < time_obj < time_limit.time()
            )

        return [
            {
                "schedule_id": schedule[ "id" ],
                "schedule_name": schedule[ "medication_name" ],
                "schedule_times": list(
                    filter(is_within_timeframe, schedule["daily_plan"])
                ),
            }
            for schedule in schedules_data
            if any(map(is_within_timeframe, schedule[ "daily_plan" ]))
        ]
