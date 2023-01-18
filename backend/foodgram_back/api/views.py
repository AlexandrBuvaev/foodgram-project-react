# from rest_framework.decorators import api_view
# from users.models import User
# from .serializers import SignUpSerializers
# from rest_framework.response import Response
# from rest_framework import status


# @api_view(['POST'])
# def sign_up_view(request):
#     """Функция для авторизации."""
#     serializer = SignUpSerializers(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     email = serializer.data.get('email')
#     username = serializer.data.get('username')
#     last_name = serializer.data.get('last_name')
#     first_name = serializer.data.get('first_name')
#     password = serializer.data.get('password')
#     user, create = User.objects.get_or_create(
#         username=username, email=email, last_name=last_name,
#         first_name=first_name, password=password
#     )
#     return Response(serializer.data, status=status.HTTP_200_OK)
