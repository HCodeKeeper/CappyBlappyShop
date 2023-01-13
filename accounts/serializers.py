from rest_framework.serializers import ModelSerializer, SlugRelatedField
from user_profiles.models import Profile, Telephone


class ProfileSerializer(ModelSerializer):
    telephone = SlugRelatedField(slug_field='number', queryset=Telephone.objects.all())

    class Meta:
        model = Profile
        fields = ['first_name', 'second_name', 'telephone', 'email', 'has_premium']
