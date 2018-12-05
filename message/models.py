from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import fields

from main.models import BaseModel

class Message(BaseModel):
	title = models.CharField(max_length=120)
	description = models.TextField()

class Message_Detail(BaseModel):
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
	object_id = models.PositiveIntegerField(null=True)
	content_object = fields.GenericForeignKey('content_type', 'object_id')

	message = models.ForeignKey(Message,on_delete=models.CASCADE)
	sender_id = models.IntegerField()
	receiver_id = models.IntegerField()
	is_group = models.BooleanField(default=False)
	is_delivered = models.BooleanField(default=False)