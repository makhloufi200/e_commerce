from django.db import models
from django.contrib.auth import get_user_model
from app.models import Items
from django.conf import settings


# Create your models here.

User = get_user_model()

class Cart(models.Model):
	user = models.ForeignKey(User,on_delete = models.CASCADE)
	item = models.ForeignKey(Items,on_delete = models.CASCADE)
	quantity = models.IntegerField(default=1)
	created_at = models.DateTimeField(auto_now_add=True)
	purchased = models.BooleanField(default=False)
	
	def __str__(self):
		return f'{ self.quantity } of { self.item.name }'
		
	def get_total(self):
		total = self.item.price * self.quantity
		floattotal = float("{0:.2f}".format(total))
		
		return floattotal	
	
	def get_total_discount_item_price(self):
		return self.quantity * self.item.discount_price
		
	def get_amount_saved(self):
		return self.get_total() - self.get_total_discount_item_price()	
	
	def get_final_price(self):
		if self.item.discount_price:
			return self.get_total_discount_item_price()
		return self.get_total()

		
class Address(models.Model):
	gender_choice = (
			('male', 'Male'),
			('female', 'Female')
		)
	gender = models.CharField(choices=gender_choice, max_length=6)
	user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	first_name = models.CharField(max_length=50, verbose_name="Prénom")
	last_name = models.CharField(max_length=50, verbose_name="Nom")
	company = models.CharField(max_length=50, blank=True, verbose_name="Société")
	address = models.CharField(max_length=255, verbose_name="Adresse")
	additional_address = models.CharField(max_length=255, blank=True, verbose_name="Complément d'adresse")
	postcode = models.CharField(max_length=5, verbose_name="Code postal")
	city = models.CharField(max_length=50, verbose_name="Ville")
	phone = models.CharField(max_length=10, verbose_name="Téléphone")
	mobilephone = models.CharField(max_length=10, blank=True, verbose_name="Téléphone portable")
	fax = models.CharField(max_length=10, blank=True, verbose_name="Fax")
	workphone = models.CharField(max_length=10, blank=True, verbose_name="Téléphone travail")

	def __str__(self):
		return self.user.username

	class Meta:
		verbose_name_plural = 'Addresses'		
		
class Order(models.Model):
			
	orderitems = models.ManyToManyField(Cart)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	ordered = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	item = models.ForeignKey(Items, on_delete=models.CASCADE,null=True)
										  
	def __str__(self):
		return self.user.username
			
	def get_totals(self):
		total = 0
		for order_item in self.orderitems.all():
			total += order_item.get_final_price()
        
		return total			