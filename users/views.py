from rest_framework.views import APIView
from rest_framework.response import Response

class MeViewAPIView(APIView):
    def get(self, request):
        return Response({
            'username': request.user.username,
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'role': request.user.role
        })
