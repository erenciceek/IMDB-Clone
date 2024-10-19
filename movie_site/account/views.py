from .serializers import RegistrationSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.decorators import api_view
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated



@api_view(['POST',])
def registration_view(request):
    
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data) 
        
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = "Registration successful"
            data['username'] = account.username
            data['email'] = account.email
            
            refresh = RefreshToken.for_user(account)
            data['token'] = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }    
        else:
            data = serializer.errors
        
        return Response(data, status=status.HTTP_201_CREATED)  
        

# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         try:
#             refresh_token = request.data["refresh"]
#             if not refresh_token:
#                 return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
            
#             token = RefreshToken(refresh_token)
#             token.blacklist()

#             return Response({"detail": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
#         except Exception as e:
#             return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)