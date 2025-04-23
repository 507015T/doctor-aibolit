from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.views import Response
from drf_spectacular.utils import extend_schema


# Create your views here.
@extend_schema(
    description="Получение ближайших приемов медикаментов для пользователя.",
    responses={201: {}},
    parameters=[],
)
@api_view(["POST"])
def create_user(request):
    new_user = get_user_model().objects.create(
        username=f"user_{get_user_model().objects.count() + 1}"
    )
    return Response({"user_id": new_user.pk}, status=201)
