from django.contrib import admin

# Register your models here.
from .models import Login,Users,Skills,Projects

admin.site.register(Login)
admin.site.register(Users)
admin.site.register(Skills)
admin.site.register(Projects)
