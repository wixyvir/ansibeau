from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def hello(request):
    """
    Simple hello endpoint to verify the backend is running.
    """
    return Response({
        'message': 'Hello from Ansible UI Backend',
        'version': '0.2.0',
        'status': 'running'
    })
