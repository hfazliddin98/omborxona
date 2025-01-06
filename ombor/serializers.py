from rest_framework.serializers import ModelSerializer, SerializerMethodField, Serializer
from django.db.models import Sum, Value, DecimalField
from django.db.models.functions import Coalesce
from django.contrib.auth import get_user_model
from decimal import Decimal
from ombor.models import Kategoriya, Maxsulot, Birlik, OmborniYopish, Ombor, Korzinka
from ombor.models import OlinganMaxsulot, Buyurtma, JamiMahsulot, Talabnoma, RadEtilganMaxsulot
from ombor.models import BuyurtmaMaxsulot, KorzinkaMaxsulot
from users.serializers import UserGetSerializer

UserModel = get_user_model()

class BirlikSerializer(ModelSerializer):
    class Meta:
        model = Birlik
        fields = ['id', 'name']

# kategoriya

class KategoriyaMaxsulotSerializer(ModelSerializer):
    birlik = BirlikSerializer()
    class Meta:
        model = Maxsulot
        fields = ['id', 'name', 'maxsulot_role', 'birlik', 'maxviylik', 'rasm']

class KategoriyaGetSerializer(ModelSerializer):
    maxsulot = KategoriyaMaxsulotSerializer(many=True, read_only=True)
    class Meta:
        model = Kategoriya
        fields = ['id', 'name', 'maxsulot']

class KategoriyaPostSerializer(ModelSerializer):

    class Meta:
        model = Kategoriya
        fields = ['id', 'name']


# maxsulot

class MaxsulotKategoriyaSerializer(ModelSerializer):
    class Meta:
        model = Kategoriya
        fields = ['id', 'name']

class MaxsulotGetSerializer(ModelSerializer):
    kategoriya = MaxsulotKategoriyaSerializer()
    birlik = BirlikSerializer()
    class Meta:
        model = Maxsulot
        fields = ['id', 'kategoriya', 'name', 'maxsulot_role', 'birlik', 'maxviylik', 'rasm']

class MaxsulotPostSerializer(ModelSerializer):
    class Meta:
        model = Maxsulot
        fields = ['id', 'kategoriya', 'name', 'maxsulot_role', 'birlik', 'maxviylik', 'rasm']


# ombor

class OmborniYopishSerializer(ModelSerializer):
    class Meta:
        model = OmborniYopish
        fields = ['id', 'yopish']


class OmborGetSerializer(ModelSerializer):
    maxsulot = MaxsulotGetSerializer()
    class Meta:
        model = Ombor
        fields = ['id', 'maxsulot', 'qiymat']

class OmborPostSerializer(ModelSerializer):
    class Meta:
        model = Ombor
        fields = ['id', 'maxsulot', 'qiymat']

# buyurtma

class BuyurtmaGetSerializer(ModelSerializer):
    komendant_user = UserGetSerializer()
    class Meta:
        model = Buyurtma
        fields = ['id', 'komendant_user', 'buyurtma_role', 'tasdiqlash', 'rad_etish', 'izoh']

class BuyurtmaPostSerializer(ModelSerializer):
    class Meta:
        model = Buyurtma
        fields = ['id', 'komendant_user', 'buyurtma_role', 'tasdiqlash', 'rad_etish', 'izoh']

class BuyurtmaMaxsulotGetSerializer(ModelSerializer):
    buyurtma = BuyurtmaGetSerializer()
    maxsulot = MaxsulotGetSerializer()
    class Meta:
        model = BuyurtmaMaxsulot
        fields = ['id', 'buyurtma', 'maxsulot', 'qiymat']

class BuyurtmaMaxsulotPostSerializer(ModelSerializer):
    class Meta:
        model = BuyurtmaMaxsulot
        fields = ['id', 'buyurtma', 'maxsulot', 'qiymat']

# korzinka

class KorzinkaSerializer(ModelSerializer):
    komendant_user= UserGetSerializer()
    class Meta:
        model = Korzinka
        fields = ['id', 'komendant_user']


class KorzinkaMaxsulotGetSerializer(ModelSerializer):
    korzinka = KorzinkaSerializer()
    maxsulot = MaxsulotGetSerializer()
    class Meta:
        model = KorzinkaMaxsulot
        fields = ['id', 'korzinka', 'maxsulot', 'qiymat', 'sorov']

class KorzinkaMaxsulotPostSerializer(ModelSerializer):
    class Meta:
        model = KorzinkaMaxsulot
        fields = ['id', 'korzinka', 'maxsulot', 'qiymat', 'sorov']

# olingan maxsulot

class OlinganMaxsulotGetSerializer(ModelSerializer):
    buyurtma = BuyurtmaGetSerializer()
    maxsulot = MaxsulotGetSerializer()
    class Meta:
        model = OlinganMaxsulot
        fields = ['id', 'buyurtma', 'maxsulot', 'qiymat']


class OlinganMaxsulotPostSerializer(ModelSerializer):
    class Meta:
        model = OlinganMaxsulot
        fields = ['id', 'buyurtma', 'maxsulot', 'qiymat']


# rad etilgan maxsulot

class RadEtilganMaxsulotGetSerializer(ModelSerializer):
    rad_etgan_user = UserGetSerializer()
    buyurtma = BuyurtmaGetSerializer()
    maxsulot = MaxsulotGetSerializer()
    class Meta:
        model = RadEtilganMaxsulot
        fields = ['id', 'rad_etgan_user', 'buyurtma', 'maxsulot', 'qiymat']

class RadEtilganMaxsulotPostSerializer(ModelSerializer):
    class Meta:
        model = RadEtilganMaxsulot
        fields = ['id', 'rad_etgan_user', 'buyurtma', 'maxsulot', 'qiymat']





class JamiMahsulotSerializer(ModelSerializer):
    """Mahsulot qiymatini chiqarish uchun serializer"""
    maxsulot = MaxsulotGetSerializer()

    class Meta:
        model = JamiMahsulot
        fields = ['id', 'maxsulot', 'qiymat']


class JamiMahsulotGetSerializer(ModelSerializer):
    """Kategoriya ichida mahsulotlar va qiymatlarini chiqarish uchun serializer"""
    maxsulotlar = SerializerMethodField()

    class Meta:
        model = Kategoriya
        fields = ['id', 'name', 'maxsulotlar']

    def get_maxsulotlar(self, obj):
        # JamiMahsulot ichidagi mahsulotlarni ushbu kategoriya bo‘yicha olish
        jami_mahsulotlar = JamiMahsulot.objects.filter(maxsulot__kategoriya=obj)
        return JamiMahsulotSerializer(jami_mahsulotlar, many=True).data





class TalabnomaSerializer(ModelSerializer):
    class Meta:
        model = Talabnoma
        fields = '__all__'


    
