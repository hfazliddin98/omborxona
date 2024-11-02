from rest_framework import serializers
from .models import Kategoriya, Maxsulot, Birlik, OmborniYopish, Ombor, Korzinka
from .models import OlinganMaxsulotlar

class KategoriyaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kategoriya
        fields = '__all__'

class MaxsulotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maxsulot
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

class OlinganMaxsulotlarSerializer(serializers.ModelSerializer):
    class Meta:
        model = OlinganMaxsulotlar
        fields = '__all__'


