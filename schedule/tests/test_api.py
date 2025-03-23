from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail

from schedule.models import MedicationSchedule


class MedicationScheduleAPITestCase(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create(username="testuser")

    def test_post_schedule(self):
        data = {
            "medication_name": "Парацетомол",
            "frequency": 8,
            "duration_days": 4,
            "user_id": self.user.id,
        }
        response = self.client.post(
            reverse("schedules-detail"), data=data, format="json"
        )
        self.assertEqual(
            status.HTTP_201_CREATED, response.status_code, response.content
        )
        expected_data = {"schedule_id": 1}
        self.assertEqual(expected_data, response.data, response.content)
        self.assertTrue(
            MedicationSchedule.objects.filter(medication_name="Парацетомол").exists()
        )

    def test_post_schedule_with_wrong_frequency(self):
        data = {
            "medication_name": "Ингаверин",
            "frequency": 17,
            "duration_days": 4,
            "user": self.user.id,
        }
        response = self.client.post(
            reverse("schedules-detail"), data=data, format="json"
        )
        self.assertEqual(
            status.HTTP_400_BAD_REQUEST, response.status_code, response.content
        )
        expected_data = {
            "detail": ErrorDetail(
                string="Frequency must be between 1 and 15 (inclusive)",
                code="parse_error",
            )
        }
        self.assertEqual(expected_data, response.data, response.content)
        self.assertEqual(MedicationSchedule.objects.all().count(), 0)

    def test_post_schedule_without_duration_days(self):
        data = {
            "medication_name": "Фурацелин",
            "frequency": 15,
            "user_id": self.user.id,
        }
        response = self.client.post(
            reverse("schedules-detail"), data=data, format="json"
        )
        self.assertEqual(
            status.HTTP_201_CREATED, response.status_code, response.content
        )
        expected_data = {"schedule_id": 1}
        self.assertEqual(expected_data, response.data, response.content)
        self.assertTrue(
            MedicationSchedule.objects.filter(medication_name="Фурацелин").exists()
        )
        self.assertEqual(MedicationSchedule.objects.all().count(), 1)

    def test_post_schedule_without_user_id(self):
        data = {
            "medication_name": "Фурацелин",
            "frequency": 15,
            "duration_days": 4,
        }
        response = self.client.post(
            reverse("schedules-detail"), data=data, format="json"
        )
        self.assertEqual(
            status.HTTP_400_BAD_REQUEST, response.status_code, response.content
        )
        expected_data = {
            "user_id": [ErrorDetail(string="This field is required.", code="required")]
        }
        self.assertEqual(expected_data, response.data, response.content)

        self.assertEqual(MedicationSchedule.objects.all().count(), 0)

    def test_post_schedule_without_medication_name(self):
        data = {
            "frequency": 15,
            "duration_days": 4,
            "user_id": self.user.id,
        }
        response = self.client.post(
            reverse("schedules-detail"), data=data, format="json"
        )
        self.assertEqual(
            status.HTTP_400_BAD_REQUEST, response.status_code, response.content
        )
        expected_data = {
            "medication_name": [
                ErrorDetail(string="This field is required.", code="required")
            ]
        }
        self.assertEqual(expected_data, response.data, response.content)

        self.assertEqual(MedicationSchedule.objects.all().count(), 0)

    def test_get_schedules_with_params_user_id(self):
        MedicationSchedule.objects.create(
            medication_name="TestPill", frequency=3, user=self.user
        )
        MedicationSchedule.objects.create(
            medication_name="TestPill2", frequency=5, user=self.user, duration_days=3
        )
        MedicationSchedule.objects.create(
            medication_name="TestPill3", frequency=8, user=self.user
        )
        response = self.client.get(
            reverse("schedules-list"), format="json", query_params={"user_id": 1}
        )
        expected_data = {"user_schedules": [1, 2, 3]}
        self.assertEqual(expected_data, response.data, response.content)

    def test_get_daily_plan(self):
        MedicationSchedule.objects.create(
            medication_name="TestPill",
            frequency=3,
            user=self.user,
        )
        response = self.client.get(
            reverse("schedules-detail"),
            format="json",
            query_params={"user_id": 1, "schedule_id": 1},
        )
        expected_data = {
            "id": 1,
            "medication_name": "TestPill",
            "frequency": 3,
            "user_id": 1,
            "daily_plan": ["08:00", "15:00", "22:00"],
            "duration_days": None,
            "start_date": datetime.now().strftime("%Y-%m-%d"),
            "end_date": None,
        }
        self.assertEqual(expected_data, response.data, response.content)
        MedicationSchedule.objects.create(
            medication_name="TestPill2", frequency=11, user=self.user, duration_days=4
        )
        response = self.client.get(
            reverse("schedules-detail"),
            format="json",
            query_params={"user_id": 1, "schedule_id": 2},
        )
        expected_data = {
            "id": 2,
            "medication_name": "TestPill2",
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
            "start_date": datetime.now().strftime("%Y-%m-%d"),
            "end_date": (datetime.now() + timedelta(days=4)).strftime("%Y-%m-%d"),
        }

        self.assertEqual(expected_data, response.data, response.content)

    def test_get_daily_plan_without_user_id(self):

        MedicationSchedule.objects.create(
            medication_name="TestPill2", frequency=11, user=self.user, duration_days=4
        )
        response = self.client.get(
            reverse("schedules-list"),
            format="json",
            query_params={"schedule_id": 1},
        )
        expected_data = {
            "response": ErrorDetail(
                string="Missing parameters: user_id", code="invalid"
            )
        }
        self.assertEqual(
            status.HTTP_400_BAD_REQUEST, response.status_code, response.content
        )
        self.assertEqual(expected_data, response.data, response.content)

    def test_get_daily_plan_without_schedule_id(self):
        MedicationSchedule.objects.create(
            medication_name="TestPill2", frequency=11, user=self.user, duration_days=4
        )
        response = self.client.get(
            reverse("schedules-detail"),
            format="json",
            query_params={"user_id": 1},
        )
        expected_data = {
            "response": ErrorDetail(
                string="Missing parameters: schedule_id", code="invalid"
            )
        }
        self.assertEqual(
            status.HTTP_400_BAD_REQUEST, response.status_code, response.content
        )
        self.assertEqual(expected_data, response.data, response.content)

    def test_get_daily_plan_without_params(self):
        MedicationSchedule.objects.create(
            medication_name="TestPill2", frequency=11, user=self.user, duration_days=4
        )
        response = self.client.get(
            reverse("schedules-detail"),
            format="json",
        )
        expected_data = {
            "response": ErrorDetail(
                string="Missing parameters: user_id, schedule_id", code="invalid"
            )
        }
        self.assertEqual(
            status.HTTP_400_BAD_REQUEST, response.status_code, response.content
        )
        self.assertEqual(expected_data, response.data, response.content)

    def test_get_next_takings(self):
        MedicationSchedule.objects.create(
            medication_name="TestPill", frequency=9, user=self.user
        )
        MedicationSchedule.objects.create(
            medication_name="TestPill2", frequency=15, user=self.user, duration_days=3
        )
        MedicationSchedule.objects.create(
            medication_name="TestPill3", frequency=8, user=self.user
        )
        response = self.client.get(
            reverse("next-takings-medicine-for-user"),
            query_params={"user_id": 1},
            format="json",
        )
        """
        if you need change NEXT_TAKINGS_PERIOD in tests,
        move into schedule.views.MedicationScheduleViewSet.next_takings
        and change next_takings_period value

        for now next_takings_period = 120 minutes ( 2hours )
        and setting datetime.now() = 7:59am (set in the same func as the next_takings_period)
        """
        expected_data = {
            "user_id": "1",
            "next_takings": [
                {
                    "schedule_id": 1,
                    "schedule_name": "TestPill",
                    "schedule_times": ["08:00", "09:45"],
                },
                {
                    "schedule_id": 2,
                    "schedule_name": "TestPill2",
                    "schedule_times": ["08:00", "09:00"],
                },
                {
                    "schedule_id": 3,
                    "schedule_name": "TestPill3",
                    "schedule_times": ["08:00"],
                },
            ],
        }
        self.assertEqual(expected_data, response.data, response.content)

    def test_get_next_takings_with_wrond_end_date(self):
        MedicationSchedule.objects.create(
            medication_name="TestPill", frequency=9, user=self.user
        )
        test_schedule = MedicationSchedule.objects.create(
            medication_name="TestPill2", frequency=15, user=self.user, duration_days=3
        )
        test_schedule.start_date = datetime(2025, 3, 18)
        test_schedule.save()
        MedicationSchedule.objects.create(
            medication_name="TestPill3", frequency=8, user=self.user
        )
        MedicationSchedule.objects.create(
            medication_name="TestPill4", frequency=8, user=self.user, duration_days=1
        )
        MedicationSchedule.objects.create(
            medication_name="TestPill5", frequency=8, user=self.user, duration_days=120
        )
        response = self.client.get(
            reverse("next-takings-medicine-for-user"),
            query_params={"user_id": 1},
            format="json",
        )
        expected_data = {
            "user_id": "1",
            "next_takings": [
                {
                    "schedule_id": 1,
                    "schedule_name": "TestPill",
                    "schedule_times": ["08:00", "09:45"],
                },
                {
                    "schedule_id": 3,
                    "schedule_name": "TestPill3",
                    "schedule_times": ["08:00"],
                },
                {
                    "schedule_id": 4,
                    "schedule_name": "TestPill4",
                    "schedule_times": ["08:00"],
                },
                {
                    "schedule_id": 5,
                    "schedule_name": "TestPill5",
                    "schedule_times": ["08:00"],
                },
            ],
        }
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data, response.content)

    def test_get_scheudle_with_wrong_end_date(self):
        test_schedule = MedicationSchedule.objects.create(
            medication_name="TestPill2", frequency=15, user=self.user, duration_days=3
        )
        test_schedule.start_date = datetime(2025, 3, 18)
        test_schedule.save()
        response = self.client.get(
            reverse("schedules-detail"),
            query_params={"user_id": 1, "schedule_id": 1},
            format="json",
        )
        expected_data = {
            "response": ErrorDetail(
                string="The medication 'TestPill2' intake ended on 2025-03-21",
                code="not_found",
            )
        }
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual(expected_data, response.data)
