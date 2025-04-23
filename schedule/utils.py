from rest_framework.exceptions import ValidationError


def get_required_params(request, params):
    missing = [p for p in params if not request.query_params.get(p)]
    if missing:
        raise ValidationError({"response": f"Missing parameters: {", ".join(missing)}"})

    return [request.query_params.get(p) for p in params]
