from rest_framework import serializers
from .models import Users

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'username','first_name', 'last_name', 'password', 'name', 'superadmin', 'admin', 'komendant', 'parol']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Users(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            name=validated_data.get('name', ''),
            superadmin=validated_data.get('superadmin', False),
            admin=validated_data.get('admin', False),
            komendant=validated_data.get('komendant', False),
            parol=validated_data['password'],  # Shifrlanmagan holda saqlanadi
        )
        user.set_password(validated_data['password'])  # Parolni shifrlash
        user.save()
        return user
