from django.db import models
from main.models import BaseModel

class Class(BaseModel):
	name = models.CharField(max_length=11)
	description = models.TextField()

	def __str__(self):
		return self.name