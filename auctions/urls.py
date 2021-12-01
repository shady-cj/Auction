from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="createlisting"),
    path("<int:product_id>/listing_page", views.listings_page, name="listingpage"),
    path("category", views.category, name="category"),
    path("category_items/<int:category_id>", views.category_items, name="categoryitems"),
    path("watchlist/<int:user_id>", views.watchlist,name="watchlist"),
    path("remove_watchlist/<int:user_id>", views.remove_watchlist, name="watchlistremove"),
    path("comment/<int:product_id>", views.comment, name="comment"),
    path("bid/<int:product_id>",views.bid, name="bid"),
    path("close_bid", views.close_bid, name='closebid'),
    path("delete_comment/<int:comment_id>", views.delete_comment, name="commentdelete"),
    path("closed_listing", views.closed_listing, name="closedlisting")
]