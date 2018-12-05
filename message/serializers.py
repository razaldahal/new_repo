from rest_framework import serializers


class MessageSerializer(serializers.Serializer):
	title = serializers.CharField(max_length=120)
	description = serializers.CharField(max_length=120)

class MessageDetailSerializer(serializers.Serializer):
	message = MessageSerializer()
	sender_id = serializers.IntegerField()
	receiver_id = serializers.IntegerField()


