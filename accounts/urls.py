from django.urls import path,include
from .views import RegisterView,LoginView,ForgotPasswordPage,ResetPasswordPage,ActivationAccountPage,DashboardView  
from .views import logout
urlpatterns = [
    path('oauth/', include('allauth.urls')),
    path('',DashboardView.as_view(),name='dashboard'),
    path('dashboard/',DashboardView.as_view(),name='dashboard'),
    
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'), 
    # path('logout/',LogoutView.as_view(),name='logout'),
    path('logout/',logout,name='logout'),
     
    path('activate/<uid64>/<token>/',ActivationAccountPage.as_view(),name='activate'),
    path('resetpass/<uid64>/<token>/',ResetPasswordPage.as_view(),name='resetpass'),
    
    path('forgot-password/',ForgotPasswordPage.as_view(), name='forgot-password'),
]
