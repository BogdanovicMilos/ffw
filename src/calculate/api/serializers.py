import json
from rest_framework import serializers
from ..models import Calculate


class AddSerializer(serializers.ModelSerializer):

    class Meta:
        model = Calculate
        fields = ('array',)


class CalculateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Calculate
        fields = ('calculatons',)


class ResetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Calculate
        fields = ('id', 'array', 'calculations',)
        extra_kwargs = ({'id': {'read_only': True}, 'array': {'read_only': True}, 'calculations': {'read_only': True}})

    def create(self, validated_data):
        array = self.context['array']
        calculations = self.context['calculations']
        user = self.context['user']

        return Calculate.objects.create(
            user=user,
            array=array,
            calculations=calculations
        )


class HistorySerializer(serializers.ModelSerializer):
    array = serializers.SerializerMethodField()
    calculations = serializers.SerializerMethodField()

    class Meta:
        model = Calculate
        fields = ('id', 'array', 'calculations',)
        extra_kwargs = ({'id': {'read_only': True}, 'array': {'read_only': True}, 'calculations': {'read_only': True}})

    @staticmethod
    def get_array(obj):
        return json.loads(obj.array)

    @staticmethod
    def get_calculations(obj):
        return json.loads(obj.calculations)