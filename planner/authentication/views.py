from django.db.migrations import serializer
from django.http import request
from django.shortcuts import render
from django.contrib.auth import authenticate 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import ProfileSerializer
from planner.utils import generate_password,send_email
import threading

# Create your views here.


class LoginView(APIView):

    def post(self,request,*args,**kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username = username , password = password)
        if user:
            refresh_token = RefreshToken.for_user(user)
            access_token = refresh_token.access_token
            token, _ = Token.objects.get_or_create(user=user)
            data = {
                'token': token.key,
                'refresh_token': str(refresh_token),
                'access_token': str(access_token),
            }
            return Response(data,status=200)
        data = {'msg':'invalid user credentials'}
        return Response(data , status=400)

class UserRegistrationView(APIView):
    serializer_class = ProfileSerializer
    def post(self,request,*args,**kwargs):
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            profile = serializer.save()
            profile.email = username
            password = generate_password()
            profile.set_password(password)
            profile.save()
            recipient = profile.email
            subject = 'Planner Site-Login Credentials'
            context = {'name':profile.first_name,'username':profile.username,'password':password}
            template = 'emails/credentials.html'
            thread = threading.Thread(target=send_email,args=(recipient,subject,context,template))
            send_email(recipient,subject,context,template)

            data = {'Message':'Account Created Succesfully'}
            return Response(data,status=201)

        return Response(serializer.errors,status=400)