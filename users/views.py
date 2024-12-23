from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from .models import Users, Binos
from .serializers import UserSerializer, BinosSerializer


@csrf_exempt
def bosh_sahifa(request):
    return redirect('/swagger/')



class UserViewSet(ModelViewSet):
    queryset = Users.objects.filter(is_superuser=False)
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'name','bino','superadmin',
        'prorektor','bugalter','xojalik_bolimi',
        'it_park','omborchi','komendant'
        ]


class BinosViewSet(ModelViewSet):
    queryset = Binos.objects.all()
    serializer_class = BinosSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']

