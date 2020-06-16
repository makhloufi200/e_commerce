from django.db import models
from django.contrib.auth import get_user_model
from app.models import Items

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
			total += order_item.get_total()
        
		return total		