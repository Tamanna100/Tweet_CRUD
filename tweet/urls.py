from django.urls import path
from . import views



urlpatterns = [
# def tweet_list(request) ; 'tweet_list.html';
    path('', views.tweet_list, name='tweet_list'),

# def tweet_create(request) ; if POST: return redirect('tweet_list'); else return render(request, 'tweet_form.html', {'t_form': t_form});
    path('create/', views.tweet_create, name='tweet_create'),

# def tweet_edit(request, tweet_id) ; if POST: return redirect('tweet_list') else:return render(request, 'tweet_form.html', {'t_form': t_form})
    path('<int:tweet_id>/edit/', views.tweet_edit, name='tweet_edit'),

# def tweet_delete(request, tweet_id): ; if POST: return redirect('tweet_list') else:return render(request, 'tweet_confirm_delete.html', {'tweet': tweet});
    path('<int:tweet_id>/delete/', views.tweet_delete, name='tweet_delete'),


# def register(request); if POST return redirect('tweet_list') else:return render(request, 'registration/register.html', {'form': form})
    path('register/', views.register, name='register'),# def tweet_list() ; 'tweet_list.html';


# def logged_out(request); 'registration/logged_out.html'
    path('logout/', views.logged_out, name='logged_out'),# def tweet_list() ; 'tweet_list.html';

    path('search/', views.search, name='search'),


]
