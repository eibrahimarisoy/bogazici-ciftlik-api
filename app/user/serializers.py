from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

from core.models import City, District, Neighborhood, Address


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user objects"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'username', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticated user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = ('Kullanıcı Bulunamadı')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'


class NeighborhoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Neighborhood
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = '__all__'

    def to_representation(self, instance):
        rep = super(AddressSerializer, self).to_representation(instance)
        rep['city'] = instance.city.name
        rep['district'] = instance.district.name
        rep['neighborhood'] = instance.neighborhood.name
        return rep