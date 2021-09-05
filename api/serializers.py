from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Diagnostic, Comorbidity, Person

User = get_user_model()


class DiagnosticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnostic
        fields = '__all__'


class ComorbiditySerializer(serializers.ModelSerializer):
    class Meta:
        model = Comorbidity
        fields = '__all__'


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        exclude = ['user']

    sex = serializers.ChoiceField(choices=['female', 'male', 'other'], required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    height = serializers.FloatField(required=True, min_value=0)
    weight = serializers.FloatField(required=True, min_value=0)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.save()

        person = Person(
            user=user,
            birthday=validated_data['birthday'],
            height=validated_data['height'],
            weight=validated_data['weight'],
            sex=validated_data['sex'],
            diagnostic=validated_data['diagnostic'],
        )
        person.save()

        person.comorbidities.set(validated_data['comorbidities'])
        person.save()

        return person
