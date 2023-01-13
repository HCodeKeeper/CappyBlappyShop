from rest_framework.serializers import ModelSerializer, SlugRelatedField
from user_profiles.models import Profile, Telephone


class TelephoneSerializer(ModelSerializer):
    class Meta:
        model = Telephone
        fields = ['number']


class ProfileSerializer(ModelSerializer):
    telephone = SlugRelatedField(slug_field='number')

    class Meta:
        model = Profile
        fields = ['first_name', 'second_name', 'telephone', 'email', 'has_premium']