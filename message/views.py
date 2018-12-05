from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.authentication import BasicAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import fields


from .models import Message,Message_Detail

from .serializers import MessageSerializer,MessageDetailSerializer

class MessageViewSet(viewsets.ModelViewSet):
	queryset = Message_Detail.objects.all()
	serializer_class = MessageDetailSerializer
	authentication_classes = [SessionAuthentication,BasicAuthentication]
	permission_classes = [IsAuthenticated]

	def create(self,request):
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid():
			data = serializer.data
			md = data['message']
			msg,created = Message.objects.get_or_create(title=md['title'],defaults={
				'description':md['description']})

			c = ContentType.objects.get_for_model(msg)

			md, c =Message_Detail.objects.get_or_create(content_type=c,object_id=msg.id,
												defaults={
												'message_id':msg.id,
												'sender_id':data['sender_id'],
												'receiver_id':data['receiver_id']

												}
												) 
			return Response(data)
		else:
			raise serializers.ValidationError({
				'Detail':['Please Enter Any Message']
				})

	def list(self,request):
		objects = Message_Detail.objects.filter(receiver_id=1,is_delivered=True)
		print(objects)
		output = []
		for obj in objects:
			message = obj.message
			temp={
			'title':message.title,
			'description':message.description,
			'sender_id':obj.sender_id,
			'time':obj.date_created,
			}
			output.append(temp)

			obj.is_delivered=True
			obj.save()
		return Response(output)



