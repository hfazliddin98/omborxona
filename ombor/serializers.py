from rest_framework import serializers
from .models import Kategoriya, MaxsulotNomi, Birlik, OmborniYopish, Ombor, Korzinka

class KategoriyaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kategoriya
        fields = '__all__'

class MaxsulotNomiSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaxsulotNomi
        fields = '__all__'

class BirlikSerializer(serializers.ModelSerializer):
    class Meta:
        model = Birlik
        fields = '__all__'

class OmborniYopishSerializer(serializers.ModelSerializer):
    class Meta:
        model = OmborniYopish
        fields = '__all__'

class OmborSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ombor
        fields = '__all__'

class KorzinkaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Korzinka
        fields = '__all__'


