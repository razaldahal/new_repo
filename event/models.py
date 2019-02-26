from django.db import models
from main.models import BaseModel,User
from academic.models import Faculty

class EventType(BaseModel):
    name=models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
    	db_table = 'event_type'

class Event(BaseModel):
    type=models.ForeignKey(EventType,on_delete=models.CASCADE)
    name=models.CharField(max_length=255)
    description=models.TextField(null=True)
    progress=models.FloatField(default=0)  
    manager=models.ForeignKey(Faculty,on_delete=models.CASCADE)
    status=models.CharField(max_length=255)
    date_start=models.DateField()
    date_end=models.DateField()

    def __str__(self):
        return self.name

    class Meta:
    	db_table = 'event_event'