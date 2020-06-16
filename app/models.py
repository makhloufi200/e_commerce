from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from PIL import Image
# Create your models here.


class Category(models.Model):
	name = models.CharField(max_length=100)
	description = models.CharField(blank=True, max_length=1000)
	slug = models.SlugField(unique=True, blank=True)
	primary_category = models.BooleanField(default =False)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.id:                                
			self.slug = slugify(self.name)      
		super().save(*args, **kwargs)

	class Meta:
		ordering = ('name','created_at', )
		
	def get_absolute_url(self):
		return reverse_lazy('categorie', args=[self.slug])	
	
	@property
	def item_by_categ(self):
		return Items.objects.filter(category=self.pk)
		

class Items(models.Model):
	name = models.CharField(max_length=100)
	image = models.ImageField(upload_to='items/', blank=True)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	created_at = models.DateTimeField(auto_now_add=True)
	description = models.CharField(blank=True, max_length=1000)
	slug = models.SlugField(unique=True, blank=True)
	category = models.ForeignKey(Category, related_name="items", on_delete=models.CASCADE)
	discount_price = models.FloatField(blank=True, null=True)

	def __str__(self):
		return self.name
	
	def get_absolute_url(self):
		return reverse('items', args=[self.pk, self.slug])

	def save(self, *args, **kwargs):
		if not self.id:     
                            
			self.slug = slugify(self.name)      
		super().save(*args, **kwargs)

	class Meta:
		ordering = ('name',)    