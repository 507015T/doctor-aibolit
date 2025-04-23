from datetime import datetime, time, timedelta, date
from django.db.models.query_utils import Q
from rest_framework import mixins
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from backend import settings
from schedule.filters import MedicationScheduleFilter
from schedule.models import MedicationSchedule
from schedule.serializers import MedicationScheduleSerializer
from drf_spectacular.utils import (
    OpenApiExample,
    extend_schema,
    OpenApiParameter,
    extend_schema_view,
)


# swagger
@extend_schema_view(
    list=extend_schema(
        operation_id="list_medication_schedules",
        description="Получение списка расписаний для пользователя.",
        parameters=[
            OpenApiParameter(
                name="user_id",
                description="ID пользователя, для которого нужно получить расписания.",
                required=True,
                type=int,
                examples=[
                    OpenApiExample(
                        "Пример запроса с user_id=1",
                        value=1,
                        description="Запрос для пользователя с id=1",
                    )
                ],
            )
        ],
        filters=False,
        examples=[
            OpenApiExample(
                "Пример успешного ответа",
                value={
                    "user_schedules": [1, 2, 3],
                },
            ),
            OpenApiExample(
                "Пример ответа, если не найдено расписаний приемов(или же пользователя)",
                value={
                    "user_schedules": [],
                },
            ),
        ],
    ),
    retrieve=extend_schema(
        operation_id="retrieve_medication_schedule",
        description="Получение подробной информации о расписании для пользователя.",
        parameters=[
            OpenApiParameter(
                name="user_id",
                description="ID пользователя.",
                required=True,
                type=int,
                examples=[OpenApiExample("Пример правильного запроса", value=1)],
            ),
            OpenApiParameter(
                name="schedule_id",
                description="ID расписания для получения данных.",
                required=True,
                type=int,
                examples=[OpenApiExample("Пример правильного запроса", value=1)],
            ),
        ],
        responses={200: MedicationScheduleSerializer},
        examples=[
            OpenApiExample(
                "Пример успешного ответа 1",
                value={
                    "id": 1,
                    "medication_name": "Фурацилин",
                    "frequency": 11,
                    "user_id": 1,
                    "daily_plan": [
                        "08:00",
                        "09:30",
                        "11:00",
                        "12:15",
                        "13:45",
                        "15:00",
                        "16:30",
                        "18:00",
                        "19:15",
                        "20:45",
                        "22:00",
                    ],
                    "duration_days": 4,
                    "start_date": "2025-08-23",
                    "end_date": "2025-08-27",
                },
            ),
            OpenApiExample(
                "Пример успешного ответа 2",
                value={
                    "id": 2,
                    "medication_name": "Миноксидил",
                    "frequency": 3,
                    "user_id": 1,
                    "daily_plan": ["08:00", "15:00", "22:00"],
                    "duration_days": None,
                    "start_date": "2025-06-01",
                    "end_date": None,
                },
            ),
        ],
    ),
    create=extend_schema(
        operation_id="create_medication_schedule",
        description="Создание нового расписания для пользователя.",
        responses={201: MedicationScheduleSerializer},
        examples=[OpenApiExample("Пример правильного запроса", value={
            "medication_name": "Парацетомол",
            "frequency": 8,
            "duration_days": 4,
            "user_id": 1,
        }), OpenApiExample("Пример ответа", value={"schedule_id": 1})
]
    ),
    next_takings=extend_schema(
        operation_id="next_takings_medication_schedule",
        description="Получение ближайших предстоящих приемов медикаментов для пользователя.",
        parameters=[
            OpenApiParameter(
                name="user_id",
                description="ID пользователя, для которого нужно получить предстоящие приемы.",
                required=True,
                type=int,
                examples=[
                    OpenApiExample(
                        "Пример запроса с user_id=1",
                        value=1,
                        description="Запрос для пользователя с id=1",
                    )
                ],
            )
        ],
        examples=[
            OpenApiExample(
                "Пример успешного ответа",
                value={
                    "user_id": "1",
                    "next_takings": [
                        {
                            "schedule_id": 1,
                            "schedule_name": "Фурацилин",
                            "schedule_times": ["08:00", "09:45"],
                        },
                        {
                            "schedule_id": 2,
                            "schedule_name": "Тренболон",
                            "schedule_times": ["08:00", "09:00"],
                        },
                        {
                            "schedule_id": 3,
                            "schedule_name": "Ингаверин",
                            "schedule_times": ["08:00"],
                        },
                    ],
                },
            ),
            OpenApiExample(
                "Пример ответа, если не найдено следующих приемов(или же пользователя)",
                value={
                    "user_id": "1",
                    "next_takings": [],
                },
            ),
        ],
        responses={
            200: {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "schedule_id": {"type": "integer"},
                        "schedule_name": {"type": "string"},
                        "schedule_times": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                    },
                },
            }
        },
    ),
)
class MedicationScheduleViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = MedicationSchedule.objects.filter(
        Q(end_date__gte=date.today()) | Q(end_date__isnull=True)
    )
    serializer_class = MedicationScheduleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MedicationScheduleFilter

    def _get_required_params(self, request, params):
        missing = [p for p in params if not request.query_params.get(p)]
        if missing:
            raise ValidationError(
                {"response": f"Missing parameters: {", ".join(missing)}"}
            )

        return [request.query_params.get(p) for p in params]

    def list(self, request, *args, **kwargs):
        user_id = self._get_required_params(request, ["user_id"])
        queryset = self.filter_queryset(self.get_queryset())
        schedule_ids = queryset.values_list("id", flat=True)
        return Response({"user_schedules": list(schedule_ids)})

    def retrieve(self, request, *args, **kwargs):
        user_id, schedule_id = self._get_required_params(
            request, ["user_id", "schedule_id"]
        )

        instance = get_object_or_404(
            MedicationSchedule, pk=schedule_id, user_id=user_id
        )
        end_date_taking = instance.end_date
        if end_date_taking and end_date_taking < date.today():
            raise NotFound(
                {
                    "response": f"The medication '{instance.medication_name}' intake ended on {end_date_taking}"
                }
            )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {"schedule_id": response.data["id"]}
        return response

    @action(["get"], detail=False)
    @extend_schema(
        description="Получение ближайших приемов медикаментов для пользователя.",
        responses={
            200: {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "schedule_id": {"type": "integer"},
                        "schedule_name": {"type": "string"},
                        "schedule_times": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                    },
                },
            }
        },
        parameters=[
            {
                "name": "user_id",
                "required": True,
                "type": "integer",
                "description": "ID пользователя, для которого нужно получить предстоящие приемы.",
            }
        ],
    )
    def next_takings(self, request, *args, **kwargs):
        user_id = self._get_required_params(request, ["user_id"])[0]
        next_takings_period = 120 if settings.TESTING else settings.NEXT_TAKINGS_PERIOD
        current_time = (
            datetime.strptime("07:59", "%H:%M") if settings.TESTING else datetime.now()
        )
        time_limit = current_time + timedelta(minutes=next_takings_period)

        schedules = MedicationSchedule.objects.filter(
            Q(end_date__gte=date.today()) | Q(end_date__isnull=True), user__id=user_id
        )
        scheduled_data = self.get_serializer(schedules, many=True).data
        upcoming_takings = self._get_upcoming_takings(
            scheduled_data, current_time, time_limit
        )
        return Response({"user_id": user_id, "next_takings": upcoming_takings})

    def _get_upcoming_takings(self, scheduled_data, current_time, time_limit):
        def is_within_timeframe(time_str):
            time_obj = datetime.strptime(time_str, "%H:%M").time()
            return (
                time(8, 0) <= time_obj <= time(22, 0)
                and current_time.time() < time_obj < time_limit.time()
            )

        return [
            {
                "schedule_id": schedule["id"],
                "schedule_name": schedule["medication_name"],
                "schedule_times": list(
                    filter(is_within_timeframe, schedule["daily_plan"])
                ),
            }
            for schedule in scheduled_data
            if any(map(is_within_timeframe, schedule["daily_plan"]))
        ]
