
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Product,Category,Watchlist,Comment,Bid

# Register your models here.

class bidadmin(admin.ModelAdmin):
	list_display=("bid_product","bid","bid_user")
class WatchlistAdmin(admin.ModelAdmin):
	def user(self, User):
		return ', '.join(f"{creator.username}" for creator in User.watchlist_user.all())
	list_display=("watchlist_product","user")

class ProductAdmin(admin.ModelAdmin):
	pass
admin.site.register(User,UserAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Category)
admin.site.register(Watchlist,WatchlistAdmin)
admin.site.register(Comment)
admin.site.register(Bid,bidadmin)