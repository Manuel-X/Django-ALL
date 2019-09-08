# render html file and redirect to any desired url
from django.shortcuts import render,redirect


#404 page
from django.http import Http404


# write http directly in views, mo need to render templates
from django.http import HttpResponse   


#views function sends data to render an html file
from django.shortcuts import render 

#Q used for search
from django.db.models import Q

#import Store model from models file
from .models import Store,Item


#import all forms from forms file
from .forms import StoreForm,SignupForm,SigninForm,SigninForm,ItemForm


#import messages 
from django.contrib import messages


#import login,logout and authenticate functions
from django.contrib.auth import login,logout,authenticate


# Create your views here.

def home(request):
	#Http Response function takes only http content
	return HttpResponse("<h1> Hello! </h1>") 



def simple_render(request):
	#render function should have atleast request and html file to render
	return render(request, 'simple.html')  



def render_with_context(request):
	#render function returning a context dictionary
	return render(request,'simple_wc.html',{"msg": "simple html file with context"})



def simple_list(request):
	#list of stores defined inside context(list of dictionaries inside the context dictionary)
	context = {
		"stores": [
			{"name": "whatever",  "location": "whatever"},
			{"name": "name",      "location": "place"},
			{"name": "you want",  "location": "you want"},
		],
	}
	return render(request, 'simple_list.html',context)



def simple_detail(request):
	#simple detail function for one of the stores chosen and placed manually
	context = {
		"store": 
		{
			"name": "whatever",
			"location": "whatever",
			"description": "more about the store",
		}
	}
	return render(request, 'simple_detail.html',context)


def store_list(request):
	#grabs list of stores from models that grabs data from database

	stores = Store.objects.all()
	query = request.GET.get('q')
	if query:
		stores = stores.filter(
			Q(name__icontains=query)|Q(description__icontains=query)
		).distinct()
	context = {
		"stores": stores
	}
	return render(request,'list.html',context)


def store_detail(request,store_slug):
	#grabs detail for specific store(by slug) from models that grabs data from database
	store_obj = Store.objects.get(slug = store_slug)
	items = store_obj.items.all() 
	query = request.GET.get('q')
	if query:
		items = stores.filter(
			Q(name__icontains=query)
		).distinct()


	
	#items = store_obj.items.all()       #can be used when related name is used(look from store side)
										 #items of store can be called from html page
	#items = Item.objects.filter(store = store_obj)  #look from item side 

	context = {
		"store": store_obj,
		#"items": items                 #items of store can be called from html page usings: store.items.all
	}
	return render(request,'detail.html', context)



def store_create(request):
	#create new store view

	#permission ---start---
	if request.user.is_anonymous:   # if no user is logged in, go to signin page and ask user to signin
		messages.success (request, "Please sign in!")
		return redirect('app:signin')
	#permision ----end-----
	
	form = StoreForm()  #form variable is populated with an emplty StoreForm

	if request.method == "POST":          				    #if post request is done(from create html) - 
		form = StoreForm(request.POST, request.FILES)		#- form variable is populate with data - 
		if form.is_valid():									#- enterd from user inside StoreForm
			store_obj = form.save(commit=False)		   	    # if form data is valid save form(object)
			store_obj.owner = request.user                  # before savin automatically assign loged - 
			store_obj.save()								# - in user as owner, then save
			messages.success (request, "new store added successfully")
			return redirect('app:list')							# after saving go back to stores list
	context = {
		"form": form                   						#pass form in context to create.html page
	}
	return render(request,'create.html', context)


def store_update(request,store_slug):
	#update existing store view

	store = Store.objects.get(slug=store_slug)

	#permission ---start---
	if request.user != store.owner:   # if user is not store's owner redirect to list page or 404 page
		messages.warning (request, "Unauthorised access")
		return redirect('app:list')
		#raise Http404
	#permision ----end-----

	form = StoreForm(instance=store)
	if request.method == "POST":
		form = StoreForm(request.POST, request.FILES, instance=store)
		if form.is_valid():
			store_obj = form.save()
			messages.info (request, "store updated successfully")
			#return redirect('app:list')
			#return redirect('app:detail',store.slug)
			return redirect (store_obj)
	context = {
		"form" : form,
		"store": store
	}
	return render (request,'update.html',context)


def store_delete(request,store_slug):

	store = Store.objects.get(slug=store_slug)
	#permission ---start---
	if request.user != store.owner:   # if user is not store's owner redirect to list page
		messages.warning (request, "Unauthorised")
		return redirect('app:list')
		#raise Http404
	#permision ----end-----


	store.delete()
	messages.warning (request, "store deleted successfully")
	return redirect('app:list')



def item_create(request,store_slug):
	#create new store view

	store_obj = Store.objects.get(slug=store_slug)
	#permission ---start---
	if request.user != store_obj.owner:   # if user is not store's owner redirect to detail page or 404 page
		messages.warning (request, "Only owner of store has access")
		return redirect('app:detail', store_slug)
		#raise Http404
	#permision ----end-----

	form = ItemForm()
	if request.method == "POST":
		form = ItemForm(request.POST,request.FILES)
		if form.is_valid():
			item_obj = form.save(commit=False)
			item_obj.store = store_obj
			item_obj.save()
			return redirect ('app:detail', store_slug)
	context = {
		"form": form,
		"store": store_obj
	}
	return render(request, 'item_create.html', context)


def item_update(request,item_slug):
	#update existing item view
	item = Item.objects.get(slug=item_slug)
	store_obj = item.store
	store_slug = store_obj.slug

	#permission ---start---
	if request.user != store_obj.owner:   # if user is not store's owner redirect to detail page or 404 page
		messages.warning (request, "Only owner of restaurants has access")
		return redirect('app:detail', store_slug)
		#raise Http404
	#permision ----end-----

	form = ItemForm(instance=item)
	if request.method == "POST":
		form = ItemForm(request.POST, request.FILES, instance=item)
		if form.is_valid():
			item_obj = form.save()
			messages.info (request, "item updated successfully")
			#return redirect('app:list')
			#return redirect('detail',item.slug)
			return redirect ('app:detail',store_slug)
	context = {
		"form" : form,
		"item": item
	}
	return render (request,'item_update.html',context)



def signup(request):

	#permission ---start---
	if not request.user.is_anonymous:   # user is logged in, ask user to sign out first
		messages.success (request, "Sign out first!")
		return redirect('app:list')
	#permision ----end-----


	form = SignupForm()
	if request.method == "POST":
		form = SignupForm(request.POST)
		if form.is_valid():
			user_obj = form.save(commit=False)
			user_obj.set_password(user_obj.password)
			user_obj.save()
			login(request,user_obj)
			messages.success(request, 'Welcome %s!' %(user.obj.first_name))
			return redirect('app:list')
	context = {
		"form": form
	}
	return render(request,'signup.html',context)


def signin(request):

	#permission ---start---
	if not request.user.is_anonymous:   # user is logged in then WTF!
		messages.success (request, "You are already signed in!")
		return redirect('app:list')
	#permision ----end-----

	form= SigninForm()
	if request.method == "POST":
		form = SigninForm(request.POST)
		if form.is_valid():
			my_username = form.cleaned_data['username']  #form.save() not used as save is not wanted
			my_password = form.cleaned_data['password']  #cleaned data returns dictionary with username or password
			# returns user_obj if password and username is correct or returns None if wrong
			user_obj = authenticate(username=my_username, password=my_password)
			if user_obj is not None:
				login(request,user_obj)
				messages.success(request,'Welcome back %s!' %(user_obj.first_name))
				return redirect('app:list')  #if condition ends if redirected
			messages.warning(request,'incorrect username/password!')

	context={
		"form":form,
	}
	return render(request, 'signin.html', context)


def item_delete(request,item_slug):


	item = Item.objects.get(slug=item_slug)
	store= item.store
	store_slug = item.store.slug


	#permission ---start---
	if request.user != store.owner:   # if user is not store's owner redirect to detail page
		messages.warning (request, "Unauthorised access")
		return redirect('app:detail', store_slug)
		#raise Http404
	#permision ----end-----


	
	store_slug = item.store.slug
	item.delete()
	messages.warning (request, "item deleted successfully")
	return redirect ('app:detail',store_slug)



def signout(request):

	#permission ---start---
	if request.user.is_anonymous:   # user is logged out then WTF!
		messages.success (request, "You are already signed out!")
		return redirect('app:list')
	#permision ----end-----


	logout(request)
	return redirect('app:signin')





