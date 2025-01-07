import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from asosiy.settings import DOMEN
from rest_framework import serializers
from .models import Users, Binos



class BinosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Binos
        fields = ['id', 'name']

class UserGetSerializer(serializers.ModelSerializer):
    bino = BinosSerializer()
    class Meta:
        model = Users
        fields = ['id', 'username', 'first_name', 'last_name', 'parol', 'lavozim', 'bino', 'role', 'is_active', 'created_at']
    

class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['username', 'first_name', 'last_name', 'password', 'lavozim', 'bino', 'role', 'is_active']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Foydalanuvchini yaratish
        password = validated_data.pop('password', None)
        user = Users(**validated_data)

        if password:
            user.set_password(password)  # Parolni shifrlash
            user.parol = password
        user.save()

        # QR kodni yaratish
        self.generate_qr_code(user)
        return user

    def update(self, instance, validated_data):
        # Foydalanuvchini yangilash
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)  # Parolni shifrlash
            instance.parol = password

        instance.save()

        # QR kodni qayta yaratish (agar username o‘zgargan bo‘lsa)
        if 'username' in validated_data:
            self.generate_qr_code(instance)
        return instance

    def generate_qr_code(self, user):
        """Foydalanuvchi uchun QR kodni yaratish va saqlash."""
        data = f"https://ombor.kspi.uz/users/{user.username}/"

        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(data)
        qr.make()
        img = qr.make_image()

        # QR kodni xotiraga saqlash
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        file_name = f"{user.username}.png"

        # QR kodni foydalanuvchi modeli bilan saqlash
        user.qr_code.save(file_name, ContentFile(buffer.read()), save=True)

        # QR kod uchun linkni saqlash
        user.qr_code_link = f"https://{DOMEN}{user.qr_code.url}"
        user.save()
