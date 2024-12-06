from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.viewsets import ModelViewSet
from .models import Users, Binos
from .serializers import UserSerializer, BinosSerializer


@csrf_exempt
def bosh_sahifa(request):
    return redirect('/swagger/')



class UserViewSet(ModelViewSet):
    queryset = Users.objects.filter(is_superuser=False)
    serializer_class = UserSerializer


class BinosViewSet(ModelViewSet):
    queryset = Binos.objects.all()
    serializer_class = BinosSerializer

