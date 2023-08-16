from rest_framework import serializers

class AttendanceStatusSerializer(serializers.Serializer):
    status = serializers.CharField()
    count = serializers.IntegerField()
