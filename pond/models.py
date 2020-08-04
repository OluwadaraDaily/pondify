from django.db import models
from django.contrib.auth.models import User
from django.core import serializers

# Create your models here.

class Pond(models.Model):

	owner = models.ForeignKey(User, on_delete = models.CASCADE, default = "1", related_name = "owner")
	pond_name = models.CharField(max_length = 64)
	channel_id = models.IntegerField(default = "0000000")

	def check_pond(name, channel):
		ponds = Pond.objects.all()

		for pond in ponds:
			if((name == pond.pond_name) or (channel == pond.channel_id)):
				return False
			else:
				return True

	
	def is_valid_pond(self):
		return (self.owner.len() > 0) and (self.pond_name.len() > 0) and (self.channel_id.len() > 0)
	
	
	def __str__(self):
		return f"{self.pond_name} | ID:{self.channel_id} | Owner: {self.owner.username}"