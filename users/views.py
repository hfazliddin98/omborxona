from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from .models import Users, Binos
from .serializers import UserGetSerializer, UserPostSerializer, BinosSerializer


@csrf_exempt
def bosh_sahifa(request):
    return redirect('/swagger/')


class UserViewSet(ModelViewSet):
    queryset = Users.objects.filter(is_superuser=False)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['role']
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:  # GET uchun
            return UserGetSerializer
        return UserPostSerializer  # POST, PUT, PATCH uchun


class BinosViewSet(ModelViewSet):
    queryset = Binos.objects.all()
    serializer_class = BinosSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']

