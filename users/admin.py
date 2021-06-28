from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(my_user)
admin.site.register(Ongoing)
admin.site.register(Question)
admin.site.register(Quiz)