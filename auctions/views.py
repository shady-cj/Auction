from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import permission_required,login_required

from .models import User,Product,Category,Watchlist,Comment,Bid


def index(request):
	return render(request, "auctions/index.html",{"products":Product.objects.all()})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))



def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first_name=request.POST["first"]
        last_name=request.POST["last"]
        dob=request.POST["dob"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password,first_name=first_name, last_name=last_name, date_of_birth=dob)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
        
def create_listing(request,):
	if request.method=="POST":
		productname=request.POST["product_name"]
		productdescription=request.POST["product_description"]
		productprice=request.POST["product_price"]
		productimage=request.FILES["product_image"]
		productcreator=User.objects.get(id=int(request.POST["creator"]))
		productcategory=Category.objects.get(id=int(request.POST["category"]))
		save_product=Product(product_name=productname,product_description=productdescription,product_price=productprice,product_image=productimage,product_category=productcategory,product_creator=productcreator)
		save_product.save()
		Watchlist.objects.create(watchlist_product=save_product)
		return HttpResponseRedirect(reverse("index"))
	return render(request, "auctions/create_listing.html",{"categories":Category.objects.all()})

@login_required(redirect_field_name="redirect",login_url='login')
def listings_page(request,product_id):
	request.session["id"]=product_id
	productinfo=Product.objects.get(id=product_id)
	watchlist=Watchlist.objects.get(watchlist_product=productinfo)
	bids=productinfo.bids.all()
	lastbid=productinfo.bids.all().last()
	message="This Product is closed and out of auction"
	alert="Congratulations you won the bid on this product"
	creatormessage="You have closed this product thus no longer active"
	user=User.objects.get(id=request.user.id)
	userwatchlist=user.watchlist.filter(watchlist_product=productinfo).exists()
	return render(request, "auctions/listing_page.html",{"userwatchlist":userwatchlist,"watchlist":watchlist,"creator":productinfo.product_creator.id,"product":productinfo,"bids":bids,"bid_total":len(bids),"comments":productinfo.comments.all(),"closemessage":message,"alert":alert,"lastbid":lastbid,"creatormessage":creatormessage})
	
def category(request,):
	return render(request, "auctions/category.html", {"categories":Category.objects.all()})
	
def category_items(request, category_id):
	category=Category.objects.get(id=category_id)
	category_item=category.categories.all()
	return render(request, "auctions/category_items.html", {"category":category, "category_item":category_item})
	
def watchlist(request,user_id):
	user=User.objects.get(id=user_id)
	request.session["user"]=user_id
	if request.method=="POST":
		watchlistproduct=Watchlist.objects.get(id=int(request.POST["addwatchlist"]))
		user.watchlist.add(watchlistproduct)
		if "id" in request.session:
			product=request.session["id"]
			return HttpResponseRedirect(reverse('listingpage', args=(product, )))
	return render(request,"auctions/watchlist.html",{"watchlists":user.watchlist.all(),})
	
def remove_watchlist(request,user_id):
	user=User.objects.get(id=user_id)
	if request.method=="POST":
		watchlistproduct=Watchlist.objects.get(id=int(request.POST["watchlist"]))
		user.watchlist.remove(watchlistproduct)
		if "id" in request.session:
			product=watchlistproduct.watchlist_product.id
			return HttpResponseRedirect(reverse("listingpage", args=(product, )))
		
def comment(request,product_id):
	product=Product.objects.get(id=product_id)
	if request.method=="POST":
		comment=request.POST["comment"]
		user=User.objects.get(id=int(request.POST["user"]))
		if comment is not None:
			save_comment=Comment.objects.create(comment=comment,comment_user=user)
			product.comments.add(save_comment)
			return HttpResponseRedirect(reverse("listingpage", args=(product.id, )))
			
def bid(request, product_id):
	product=Product.objects.get(id=product_id)
	if request.method=="POST":
		bid=float(request.POST["bidprice"])
		bid_user=User.objects.get(id=int(request.POST["user"]))
		if product.bids.all().count()==0:
			Bid.objects.create(bid=bid,bid_user=bid_user,bid_product=product)
			return HttpResponseRedirect(reverse("listingpage", args=(product.id, )))
		if bid > product.bids.all().last().bid:
			Bid.objects.create(bid=bid,bid_user=bid_user,bid_product=product)
			return render(request, "auctions/listing_page.html",{"product":product,"comments":product.comments.all(), "message":"Your bid has been placed","bid_total":len(product.bids.all())})
		elif bid==product.bids.all().last().bid:
			return render(request, "auctions/listing_page.html",{"product":product,"comments":product.comments.all(), "message":"Your bid must be higher than the previous bids","bid_total":len(product.bids.all())})
		else:
			return render(request, "auctions/listing_page.html",{"product":product,"comments":product.comments.all(), "message":"Your bid is lower than the previous bids","bid_total":len(product.bids.all())})
	return render(request,"auctions/bid.html",{"bids":product.bids.all()})
		
def close_bid(request,):
	if request.method=="POST":
		product=Product.objects.get(id=int(request.POST["closebid"]))
		product.active=False
		product.save()
		return HttpResponseRedirect(reverse("index"))
	
def delete_comment(request,comment_id):
	if request.method=="POST":
		if "id" in request.session:
			productid=request.session["id"]
			comment=Comment.objects.get(id=comment_id)
			comment.delete()
			return HttpResponseRedirect(reverse("listingpage", args=(productid, )))
def closed_listing(request,):
	return render(request, "auctions/closed_listing.html",{"products":Product.objects.all()})