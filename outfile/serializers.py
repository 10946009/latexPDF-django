from models import Problem, InputOutput
from rest_framework import serializers

class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = '__all__'

class InputOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = InputOutput
        fields = '__all__'