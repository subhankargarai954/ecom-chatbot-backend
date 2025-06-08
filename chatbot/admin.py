# Register your models here.
from .models import ChatMessage
from django.contrib import admin
from .models import Product

admin.site.register(Product)
admin.site.register(ChatMessage)
