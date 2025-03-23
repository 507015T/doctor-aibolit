from datetime import datetime, timedelta
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from schedule.models import MedicationSchedule, User


class MedicationScheduleSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="user"
    )
    daily_plan = serializers.SerializerMethodField()
    end_date = serializers.SerializerMethodField()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")
        if request:
            path = request.path
            user_id = request.query_params.get("user_id")
            schedule_id = request.query_params.get("schedule_id")
            if not (
                (path == "/schedule/" and user_id and schedule_id)
                or (path == "/next_takings/")
            ):
                data.pop("daily_plan", None)
        return data

    def get_end_date(self, obj):
        return obj.end_date.strftime("%Y-%m-%d") if obj.end_date else None

    def validate_frequency(self, value):
        if not 1 <= value <= 15:
            raise ParseError("Frequency must be between 1 and 15 (inclusive)")
        return value

    def validate_daily_plan(self, value):
        request = self.context.get("request")
        if request:
            user_id = request.query_params.get("user_id")
            schedule_id = request.query_params.get("schedule_id")
            if user_id and schedule_id:
                return value

    def get_daily_plan(self, instance):
        if "daily_plan" not in self.fields:
            return None
        return self._generate_daily_plan(instance)

    def _generate_daily_plan(self, instance):
        frequency = instance.frequency
        start_time = datetime.strptime("8:00", "%H:%M")
        end_time = datetime.strptime("22:00", "%H:%M")
        if frequency == 1:
            return [start_time.strftime("%H:%M")]
        interval = (end_time - start_time) / (frequency - 1)
        times = []
        for i in range(frequency):
            estimated_time = start_time + i * interval
            minutes = estimated_time.minute

            new_minutes = (minutes + 14) // 15 * 15
            if new_minutes == 60:
                estimated_time = estimated_time.replace(minute=0) + timedelta(hours=1)
            else:
                estimated_time = estimated_time.replace(minute=new_minutes)

            times.append(estimated_time.strftime("%H:%M"))

        return times

    class Meta:
        model = MedicationSchedule
        fields = (
            "id",
            "medication_name",
            "frequency",
            "duration_days",
            "user_id",
            "start_date",
            "end_date",
            "daily_plan",
        )
