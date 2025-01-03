from rest_framework.serializers import ModelSerializer, SerializerMethodField
from django.db.models import Sum
from django.contrib.auth import get_user_model
from decimal import Decimal
from ombor.models import Kategoriya, Maxsulot, Birlik, OmborniYopish, Ombor, Korzinka
from ombor.models import OlinganMaxsulotlar, Buyurtma, JamiMahsulot, Talabnoma, RadEtilganMaxsulotlar
from ombor.models import BuyurtmaMaxsulot, KorzinkaMaxsulot
from users.serializers import UserGetSerializer

UserModel = get_user_model()



class KategoriyaSerializer(ModelSerializer):
    class Meta:
        model = Kategoriya
        fields = ['id', 'name']

class BirlikSerializer(ModelSerializer):
    class Meta:
        model = Birlik
        fields = ['id', 'name']

class MaxsulotGetSerializer(ModelSerializer):
    kategoriya = KategoriyaSerializer()
    birlik = BirlikSerializer()
    class Meta:
        model = Maxsulot
        fields = ['id', 'kategoriya', 'name', 'maxsulot_role', 'birlik', 'maxviylik', 'rasm']

class MaxsulotPostSerializer(ModelSerializer):
    class Meta:
        model = Maxsulot
        fields = ['id', 'kategoriya', 'name', 'maxsulot_role', 'birlik', 'maxviylik', 'rasm']

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


class KorzinkaGetMaxsulotSerializer(ModelSerializer):
    korzinka = KorzinkaSerializer()
    maxsulot = MaxsulotGetSerializer()
    class Meta:
        model = KorzinkaMaxsulot
        fields = ['id', 'korzinka', 'maxsulot', 'qiymat', 'sorov']

class KorzinkaPostMaxsulotSerializer(ModelSerializer):
    class Meta:
        model = KorzinkaMaxsulot
        fields = ['id', 'korzinka', 'maxsulot', 'qiymat', 'sorov']



class OlinganMaxsulotlarSerializer(ModelSerializer):
    class Meta:
        model = OlinganMaxsulotlar
        fields = '__all__'

class RadEtilganMaxsulotlarSerializer(ModelSerializer):
    class Meta:
        model = RadEtilganMaxsulotlar
        fields = '__all__'

class BuyurtmaSearchSerializer(ModelSerializer):
    class Meta:
        model = Buyurtma
        fields = '__all__'


class JamiMahsulotSerializer(ModelSerializer):
    yakuniy_qiymat = SerializerMethodField()

    class Meta:
        model = JamiMahsulot
        fields = '__all__'

    def get_yakuniy_qiymat(self, obj):
        olingan_jami_qiymat = OlinganMaxsulotlar.objects.filter(
            maxsulot=obj.maxsulot,
            active=True
        ).aggregate(total_qiymat=Sum('qiymat'))['total_qiymat'] or 0.0
        return Decimal(obj.qiymat) - Decimal(olingan_jami_qiymat)


class TalabnomaSerializer(ModelSerializer):
    class Meta:
        model = Talabnoma
        fields = '__all__'


    
