
from django.urls import path
from .views import RegisterAPI, LoginAPI, current_user, LogoutView
from . import views
from .models import User
from .serializers import RegisterSerializer


urlpatterns = [


    path('', views.apiOverview, name="api-overview"),
   	path('book-list/', views.bookList, name="book-list"),
   	path('book-detail/<str:pk>/', views.bookDetail, name="book-detail"),
   	path('book-create/', views.bookCreate, name="book-create"),
    path('book-update/<str:pk>/', views.bookUpdate, name="book-update"),
   	path('book-delete/<str:pk>/', views.bookDelete, name="task-delete"),
    path('book-borrow/<str:pk>/', views.bookborrow, name="book-borrow"),
    path('book-return/<str:pk>/', views.bookreturn, name="book-return"),
    path('register', RegisterAPI.as_view(), name='register'),
    path('login', LoginAPI.as_view(), name='login'),
    path('current_user', views.current_user, name="current_user"),
    path('logout', LogoutView.as_view(), name='logout'),

]
