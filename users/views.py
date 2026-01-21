from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from users.serializers import SignupSerializer


class SignupAPIView(APIView):
    permission_classes = [AllowAny,]
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message': 'User created successfully.'}, status=201)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

class MeViewAPIView(APIView):
    def get(self, request):
        return Response({
            'username': request.user.username,
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'role': request.user.role
        })
