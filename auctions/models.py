from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    first_name=models.CharField(max_length=20, blank=True)
    last_name=models.CharField(max_length=20, blank=True)
    date_of_birth=models.DateField(blank=True, null=True)


class Category(models.Model):
	category_name=models.CharField(max_length=64,)	
	def __str__(self,):
		return f"{self.category_name}"


class Product(models.Model):
	product_name=models.CharField(max_length=64,)
	product_price=models.DecimalField(max_digits=10, decimal_places=2)
	product_description=models.CharField(max_length=64, blank=True)
	product_image=models.ImageField(upload_to='images/%Y/%m/%d', null=True, blank=True)
	product_category=models.ForeignKey(Category,on_delete=models.CASCADE,null=True,related_name="categories", blank=True)
	product_creation_date=models.DateTimeField(auto_now_add=True,null=True)
	product_creator=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True, related_name="productcreator")
	active=models.BooleanField(default=True)

	def __str__(self,):
		return f"{self.product_name} {self.product_description}, price(${self.product_price}) "
		

class Bid(models.Model):
	bid=models.DecimalField(max_digits=10, decimal_places=2)	
	bid_user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="userbid")
	bid_product=models.ForeignKey(Product,on_delete=models.CASCADE,blank=True,null=True,related_name="bids")
	
	def __str__(self,):
		return f"${self.bid} bid by {self.bid_user} on {self.bid_product}"


class Watchlist(models.Model):
	watchlist_product=models.ForeignKey(Product, on_delete=models.CASCADE,null=True,blank=True)
	watchlist_user=models.ManyToManyField(User,blank=True, related_name="watchlist",)
	
	def __str__(self,):
		return f"{self.watchlist_product}"


class Comment(models.Model):
	comment_user=models.ForeignKey(User, on_delete=models.SET_NULL,blank=True, null=True)
	comment=models.TextField(blank=True)
	comment_datetime=models.DateTimeField(auto_now=False,default=timezone.now)
	comment_product=models.ManyToManyField(Product, blank=True, related_name="comments")
	def __str__(self,):
		return f"{self.comment} by \"{self.comment_user}\" on {self.comment_datetime}"