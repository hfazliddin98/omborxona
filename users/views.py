from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.viewsets import ModelViewSet
from .models import Users
from .serializers import UserSerializer


@csrf_exempt
def bosh_sahifa(request):
    return redirect('/swagger/')



class UserViewSet(ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
