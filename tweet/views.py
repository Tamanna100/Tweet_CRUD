
from django.contrib import messages
from django.db.models import Q #to query multiple items

from django.shortcuts import render, get_object_or_404 ,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login ,logout

from .models import  Tweet
from .forms import  TweetForm ,UserRegistrationForm

# path('', views.tweet_list, name='tweet_list'),
def tweet_list(request):
	tweets = Tweet.objects.all().order_by('-created_at')
	return render(request, 'tweet_list.html', {'tweets': tweets})


# path('create/', views.tweet_create, name='tweet_create')
@login_required
def tweet_create(request):
	# post data; sending data to server,data taken from user, when user fills up the form they are now sending it to
	# server; data validation needed before sending to server
	if request.method == 'POST':
		# form which user sent saving in an object "t_form"
		t_form =TweetForm(request.POST ,request.FILES)
		# checking if data is valid for security purpose; csrf token in html
		if t_form.is_valid():
			# saving the data from obj to a variable "tweet" ; not commiting to the server yet
			tweet = t_form.save(commit=False)
			# adding the user info in tweet variable
			tweet.user = request.user
			# finally saving it to the server
			tweet.save()
			# calling def tweet_list(request):
			return redirect('tweet_list')
	# get data; fetching a form page, sending to user, visiable to user, from server form is fetcing when user just
	# enters to tweet, empty form is given to them;
	else:
		# creating an empty form for user to crate tweet
		t_form = TweetForm()
	# sending the empty form in "tweet_form.html", through which this will be visiable to the user
	return render(request, 'tweet_form.html', {'t_form': t_form})



# path('<int:tweet_id>/edit/', views.tweet_edit, name='tweet_edit')
@login_required
def tweet_edit(request, tweet_id):
	#get tweet information from Tweet model according to tweet_id and for particular user
	tweet = get_object_or_404(Tweet, pk=tweet_id ,user=request.user)
	if request.method == 'POST':
		# form post request data is stored in t_form; instance=tweet is used when edit function, to bring the
		# previous data; this is a django form, not the bootstrap; if it was bootstrap then we had to give the
		# <input name =""> like
		# searched = request.POST['searched'], where ['searched'] is the name of the <input> tag
		t_form = TweetForm(request.POST ,request.FILES ,instance=tweet)
		if t_form.is_valid():
			tweet = t_form.save(commit=False)
			tweet.user = request.user
			tweet.save()
			return redirect('tweet_list')
	else:
		t_form =TweetForm(instance=tweet)
		return render(request, 'tweet_form.html', {'t_form': t_form})



# path('<int:tweet_id>/delete/', views.tweet_delete, name='tweet_delete')
@login_required
def tweet_delete(request, tweet_id):
	tweet = get_object_or_404(Tweet, pk=tweet_id ,user=request.user)
	if request.method == 'POST':
		tweet.delete()
		return redirect('tweet_list')
	return render(request, 'tweet_confirm_delete.html', {'tweet': tweet})

# path('register/', views.register, name='register')
def register(request):
	if request.method == 'POST':
		# build in post request "UserRegistrationForm(request.POST)" stored in form; this is a django form,
		# not the bootstrap; if it was bootstrap then we had to give the <input name =" "> like
		# searched = request.POST['searched'], where ['searched'] is the name of the <input> tag
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			# before saving password data can be cleaned by "cleaned_data['password1']" method; password1 is build in
			# variable
			user.set_password(form.cleaned_data['password1'])
			user.save()
			# build in login function
			login(request, user)
			return
	else:
		form = UserRegistrationForm()
	return render(request, 'registration/register.html', {'form': form})

# path('logout/', views.logged_out, name='logged_out')
def logged_out(request):
	#build in logout function
	logout(request)
	return render(request, 'registration/logged_out.html')



def search(request):
	if request.method == 'POST':
		# this "request.POST['searched']" searched came from the html bootstarp search form; input name = 'searched';
		# this is not a django form; if it was django form, it would be like "t_form=TweetForm(request.POST,request.FILES)"
		searched = request.POST['searched']
		#query from the DB of Tweet table; i_contains means case in-sensitive; Q for multiple field query
		searches = Tweet.objects.filter(Q(text__icontains=searched)) | Tweet.objects.filter \
			(user__username__icontains=searched)
		#test for null
		if not searches :
			messages.success(request, 'No such thing found')
			return redirect('tweet_list')
		elif searched =="":
			messages.success(request, 'Empty String')
			return redirect('tweet_list')
		else :
			return render(request, 'search.html', {'searches': searches})
