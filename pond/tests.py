from django.test import TestCase
from .models import Pond
from django.contrib.auth.models import User

# Create your tests here.

class ModelsTestCase(TestCase):

	def setUp(self):

		#Create Users
		u1 = User.objects.create("Tofunmi", "daraoloye99@gmail.com", "Tofunmi", "Awodiji")
		# u2 = User("")
		
		#Create Ponds
		p1 = Pond.objects.create(owner = u1, pond_name = "Test1", channel_id = 1002025)
		p2 = Pond.objects.create(owner = u1, pond_name = "Test2", channel_id = 0000)

	def test_channel_id(self):
		""" Testing for the validity of each pond to be created """
		# u1 = User.objects.filter(pk=1)
		p1 = Pond.objects.filter(pond_name = 'Test1')
		p2 = Pond.objects.filter(pond_name = "Test2")
		
		self.assertTrue(p1.is_valid_pond())
		self.assertFalse(p2.is_valid_pond())