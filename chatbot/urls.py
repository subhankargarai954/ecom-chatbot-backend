from .views import chat_history, reset_chat
from .views import register_user, chat_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list, name='product-list'),
    path('products/<int:pk>/', views.product_detail, name='product-detail'),
    path('test/', views.test_view, name='test_view'),    
]

urlpatterns += [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += [
    path('register/', register_user, name='register'),
]

urlpatterns += [
    path('chat/', chat_view, name='chat'),
]


urlpatterns += [
    path('chat/history/', chat_history, name='chat-history'),
    path('chat/reset/', reset_chat, name='chat-reset'),
]
