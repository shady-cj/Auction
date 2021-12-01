from .models import User

def watchlist_processor(request,):
	if 'user' in request.session:
		user_id=request.session["user"]
		users=User.objects.get(id=int(user_id))
		watchlists=users.watchlist.all()
		length=len(watchlists)
		return {"length":length,"watch":watchlists.exists()}