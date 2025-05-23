from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
"""
pip install djangorestframework-simplejwt
"""
class RegisterView(APIView):
    def post(self, request):
        required_fields = ['username', 'password']
        if not all(field in request.data for field in required_fields):
            return Response({'error': '缺少必填字段'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create_user(
                username=request.data['username'],
                password=request.data['password'],
            )
            return Response({'message': '注册成功'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': "用户已存在"}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            from rest_framework_simplejwt.tokens import RefreshToken
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'username': user.username
                }
            })
        else:
            return Response({'error': '用户名或密码错误'}, status=status.HTTP_401_UNAUTHORIZED)