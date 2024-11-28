import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from asosiy.settings import DOMEN
from rest_framework import serializers
from .models import Users

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'username','first_name', 'last_name', 'password', 'name', 'superadmin', 'prorektor', 'bugalter', 'xojalik_bolimi', 'it_park', 'omborchi', 'komendant', 'qr_code', 'parol']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Users(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            name=validated_data.get('name', ''),
            superadmin=validated_data.get('superadmin', False),
            prorektor=validated_data.get('prorektor', False),
            bugalter=validated_data.get('bugalter', False),
            xojalik_bolimi=validated_data.get('xojalik_bolimi', False),
            it_park=validated_data.get('it_park', False),
            omborchi=validated_data.get('omborchi', False),
            komendant=validated_data.get('komendant', False),
            parol=validated_data['password'],  # Shifrlanmagan holda saqlanadi
        )
        user.set_password(validated_data['password'])  # Parolni shifrlash

        username = validated_data['username']
        data = f"https://ombor.kspi.uz/users/{username}/"

        # Generate the QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(data)
        qr.make()
        img = qr.make_image()

        # Save the image to an in-memory file
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        file_name = f"{username}.png"

        # Create the UserQrCode instance
        
        user.qr_code.save(file_name, ContentFile(buffer.read()), save=True)
        return user



