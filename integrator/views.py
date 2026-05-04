from rest_framework.decorators import api_view
from rest_framework.response import Response

from integrator.tasks import sync_products


@api_view(["POST"])
def trigger_sync(request):
    sync_products.delay()

    return Response({
        "status": "started"
    })