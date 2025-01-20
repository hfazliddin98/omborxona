from rest_framework.serializers import ModelSerializer, SerializerMethodField, Serializer, PrimaryKeyRelatedField
from django.db.models import Sum, Value, DecimalField
from django.db.models.functions import Coalesce
from django.contrib.auth import get_user_model
from decimal import Decimal
from asosiy.settings import DOMEN
from ombor.models import Kategoriya, Maxsulot, Birlik, OmborniYopish, Ombor, Korzinka
from ombor.models import OlinganMaxsulot, Buyurtma, JamiMahsulot, Talabnoma, RadEtilganMaxsulot
from ombor.models import BuyurtmaMaxsulot, KorzinkaMaxsulot
from users.choices import MaxsulotRoleChoice
from users.serializers import UserGetSerializer


UserModel = get_user_model()

class BirlikSerializer(ModelSerializer):
    class Meta:
        model = Birlik
        fields = ['id', 'name', 'created_at']

# kategoriya

class KategoriyaMaxsulotSerializer(ModelSerializer):
    birlik = BirlikSerializer()
    class Meta:
        model = Maxsulot
        fields = ['id', 'name', 'maxsulot_role', 'birlik', 'maxviylik', 'rasm', 'created_at']

class KategoriyaGetSerializer(ModelSerializer):
    maxsulot = KategoriyaMaxsulotSerializer(many=True, read_only=True)
    class Meta:
        model = Kategoriya
        fields = ['id', 'name', 'maxsulot', 'created_at']

class KategoriyaPostSerializer(ModelSerializer):

    class Meta:
        model = Kategoriya
        fields = ['name']


# maxsulot

class MaxsulotKategoriyaSerializer(ModelSerializer):
    class Meta:
        model = Kategoriya
        fields = ['id', 'name', 'created_at']
 

class MaxsulotGetSerializer(ModelSerializer):
    kategoriya = MaxsulotKategoriyaSerializer()
    birlik = BirlikSerializer()
    class Meta:
        model = Maxsulot
        fields = ['id', 'kategoriya', 'name', 'maxsulot_role', 'birlik', 'maxviylik', 'rasm', 'created_at']


class MaxsulotPostSerializer(ModelSerializer):
    class Meta:
        model = Maxsulot
        fields = ['kategoriya', 'name', 'maxsulot_role', 'birlik', 'maxviylik', 'rasm']


# ombor

class OmborniYopishSerializer(ModelSerializer):
    class Meta:
        model = OmborniYopish
        fields = ['id', 'yopish']


class OmborGetSerializer(ModelSerializer):
    maxsulot = MaxsulotGetSerializer()
    class Meta:
        model = Ombor
        fields = ['id', 'maxsulot', 'qiymat', 'created_at']

class OmborPostSerializer(ModelSerializer):
    class Meta:
        model = Ombor
        fields = ['maxsulot', 'qiymat']

# buyurtma


class BuyurtmaMaxsulotSerializer(ModelSerializer):
    maxsulot = MaxsulotGetSerializer()
    class Meta:
        model = BuyurtmaMaxsulot
        fields = ['id', 'buyurtma', 'maxsulot', 'qiymat', 'created_at']

class BuyurtmaSerializer(ModelSerializer):
    komendant_user = UserGetSerializer()
    maxsulotlar = BuyurtmaMaxsulotSerializer(many=True, read_only=True)
    class Meta:
        model = Buyurtma
        fields = [
            'id', 'komendant_user', 'buyurtma_role', 'maxsulotlar', 
            'prorektor', 'bugalter', 'omborchi', 'rttm', 'xojalik',
            'rad_etish', 'izoh', 'created_at'
            ]


# korzinka

class KorzinkaMaxsulotSerializer(ModelSerializer):
    maxsulot = MaxsulotGetSerializer()  

    class Meta:
        model = KorzinkaMaxsulot
        fields = ['id', 'maxsulot', 'qiymat'] 

class KorzinkaMaxsulotPostSerializer(ModelSerializer):
    class Meta:
        model = KorzinkaMaxsulot
        fields = ['maxsulot', 'qiymat']


class KorzinkaSerializer(ModelSerializer):
    maxsulotlar = KorzinkaMaxsulotSerializer(many=True, read_only=True)

    class Meta:
        model = Korzinka
        fields = ['id', 'komendant_user', 'maxsulot_role', 'maxsulotlar'] 



# rad etilgan maxsulot

class KeyingiMaxsulotSerializer(ModelSerializer):
    komendant_user = UserGetSerializer()
    maxsulotlar = BuyurtmaMaxsulotSerializer(many=True, read_only=True)
    class Meta:
        model = Buyurtma
        fields = ['id', 'komendant_user', 'maxsulotlar', 'created_at']

class RadEtilganMaxsulotSerializer(ModelSerializer):
    rad_etgan_user = UserGetSerializer()
    buyurtma = KeyingiMaxsulotSerializer()
    class Meta:
        model = RadEtilganMaxsulot
        fields = ['id', 'rad_etgan_user', 'buyurtma', 'active', 'created_at']

class RadEtilganMaxsulotPostSerializer(ModelSerializer):
    class Meta:
        model = RadEtilganMaxsulot
        fields = ['active']




class JamiMahsulotSerializer(ModelSerializer):
    """Mahsulot qiymatini chiqarish uchun serializer"""
    maxsulot = MaxsulotGetSerializer()

    class Meta:
        model = JamiMahsulot
        fields = ['id', 'maxsulot', 'qiymat', 'created_at']


class JamiMahsulotGetSerializer(ModelSerializer):
    """Kategoriya ichida mahsulotlar va qiymatlarini chiqarish uchun serializer"""
    maxsulotlar = SerializerMethodField()

    class Meta:
        model = Kategoriya
        fields = ['id', 'name', 'maxsulotlar', 'created_at']

    def get_maxsulotlar(self, obj):
        # JamiMahsulot ichidagi mahsulotlarni ushbu kategoriya bo‘yicha olish
        jami_mahsulotlar = JamiMahsulot.objects.filter(maxsulot__kategoriya=obj)
        return JamiMahsulotSerializer(jami_mahsulotlar, many=True).data
    


class TalabnomaSerializer(ModelSerializer):
    class Meta:
        model = Talabnoma
        fields = ['active']

    
