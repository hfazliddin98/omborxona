from rest_framework.serializers import ModelSerializer, SerializerMethodField
from django.db.models import Sum
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

class OmborSerializer(ModelSerializer):
    class Meta:
        model = Ombor
        fields = '__all__'

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
    yakuniy_qiymat = SerializerMethodField()

    class Meta:
        model = JamiMahsulot
        fields = '__all__'

    def get_yakuniy_qiymat(self, obj):
        olingan_jami_qiymat = OlinganMaxsulot.objects.filter(
            maxsulot=obj.maxsulot,
            active=True
        ).aggregate(total_qiymat=Sum('qiymat'))['total_qiymat'] or 0.0
        return Decimal(obj.qiymat) - Decimal(olingan_jami_qiymat)


class TalabnomaSerializer(ModelSerializer):
    class Meta:
        model = Talabnoma
        fields = '__all__'


    
