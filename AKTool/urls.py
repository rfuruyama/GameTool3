from django.urls import path
from . import views

app_name = 'AKTool'
urlpatterns = [
    path('', views.Welcome.as_view(), name='welcome'),
    path('login/', views.signin, name='login'),
    path('logout/', views.Signout.as_view(), name='logout'),
    path('create_account/', views.SignUp.as_view(), name='signup'),
    path('create_success/', views.create_account, name='create_success'),
    path('<str:username>/home/', views.home, name='home'),
    path('<str:username>/charaselect/', views.charaSelect, name='charaSelect'),
    path('<str:username>/<str:chara_id>/', views.charaDetail, name='charaDetail'),
    path('<str:username>/tagselect', views.tagSelect, name='tagSelect'),
]