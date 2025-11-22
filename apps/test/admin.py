from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *



class IspAdmin(admin.ModelAdmin):
    list_per_page = 30


class TestAdmin(admin.ModelAdmin):
    list_per_page = 30

class AppAdmin(admin.ModelAdmin):
    list_per_page = 30


admin.site.register(Isp, IspAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(App, AppAdmin)
