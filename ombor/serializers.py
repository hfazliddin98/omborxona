from rest_framework import serializers
from django.db.models import Sum
from django.contrib.auth import get_user_model
from decimal import Decimal
from .models import Kategoriya, Maxsulot, Birlik, OmborniYopish, Ombor, Korzinka
from .models import OlinganMaxsulotlar, Buyurtma, JamiMahsulot, Talabnoma, RadEtilganMaxsulotlar

UserModel = get_user_model()



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

class BuyurtmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyurtma
        fields = '__all__'

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ("id", "first_name", "last_name")

class SimpleKorzinkaSerializer(serializers.ModelSerializer):
    maxsulot = serializers.SerializerMethodField()
    birlik = serializers.SerializerMethodField()
    class Meta:
        model = Korzinka
        fields = ("id", "maxsulot", "qiymat", "birlik")

    def get_maxsulot(self, korzinka: Korzinka):
        return korzinka.maxsulot.name

    def get_birlik(self, korzinka: Korzinka):
        return korzinka.birlik.name

class BuyurtmaListSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer()
    maxsulotlar = SimpleKorzinkaSerializer(many=True, source="korzinka_set")

    class Meta:
        model = Buyurtma
        fields = ("id", "user", "maxsulotlar")

class KorzinkaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Korzinka
        fields = '__all__'

class OlinganMaxsulotlarSerializer(serializers.ModelSerializer):
    class Meta:
        model = OlinganMaxsulotlar
        fields = '__all__'

class RadEtilganMaxsulotlarSerializer(serializers.ModelSerializer):
    class Meta:
        model = RadEtilganMaxsulotlar
        fields = '__all__'

class BuyurtmaSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyurtma
        fields = '__all__'


class JamiMahsulotSerializer(serializers.ModelSerializer):
    yakuniy_qiymat = serializers.SerializerMethodField()

    class Meta:
        model = JamiMahsulot
        fields = '__all__'

    def get_yakuniy_qiymat(self, obj):
        olingan_jami_qiymat = OlinganMaxsulotlar.objects.filter(
            maxsulot=obj.maxsulot,
            active=True
        ).aggregate(total_qiymat=Sum('qiymat'))['total_qiymat'] or 0.0
        return Decimal(obj.qiymat) - Decimal(olingan_jami_qiymat)


class TalabnomaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Talabnoma
        fields = '__all__'


    
