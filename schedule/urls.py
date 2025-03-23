
from rest_framework.routers import DefaultRouter

from django.urls import re_path
from .views import MedicationScheduleViewSet

# router = DefaultRouter()
# router.register("schedule", MedicationScheduleViewSet)


# urlpatterns = router.urls
urlpatterns= [
    re_path(r"^schedule/$", MedicationScheduleViewSet.as_view({"post": "create", "get": "retrieve"}), name="schedules-detail"),
    re_path(r"^schedules/$", MedicationScheduleViewSet.as_view({"get": "list"}), name="schedules-list"),
    re_path(r"^next_takings/$", MedicationScheduleViewSet.as_view({"get": "next_takings"}), name="next-takings-medicine-for-user"),
    # re_path(r"^schedule/$", MedicationScheduleViewSet.as_view({"post": "create"}), name="schedule-create"),
]
