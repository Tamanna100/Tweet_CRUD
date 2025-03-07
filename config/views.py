from django.shortcuts import render, get_object_or_404


# path('',views.landing,name='landing')
def landing(request):
	return render(request, 'landing.html')









