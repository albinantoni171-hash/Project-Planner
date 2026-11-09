from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import ProfileSerializer
from planner.utils import generate_password,send_email
import threading

# Create your views here.

class LoginView(APIView):
    def post (self,request,*args,**kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username,password=password)

        if user:
            refresh_token =  RefreshToken.for_user(user)
            access_token = refresh_token.access_token

            data = {'refresh':str(refresh_token),'access':str(access_token)}

            return Response(data,status=200)
        
        data = {'msg':'incorrect username or password'}

        return Response(data,status=400)


class UserRegisterView(APIView):
    serializer_class = ProfileSerializer

    def post(self,request,*args,**kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            profile = serializer.save()
            profile.email = username
            password = generate_password()
            profile.password = password
            profile.set_password(password)
            profile.save()
            recipient = profile.email
            subject = 'Project Planner Login Credentials'
            context = {'name':profile.first_name,'username':profile.username,'password':password}
            template = 'emails/credentials.html'

            thread = threading.Thread(target=send_email,args=(recipient,context,subject,template))
            send_email(recipient,context,subject,template)

            data = {'msg':'Account successfully created'}
            
            return Response(data,status=201)
        return Response(serializer.errors,status=400)