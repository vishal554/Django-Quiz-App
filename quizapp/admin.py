from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Question)
admin.site.register(FibQuestion)
admin.site.register(McqQuestion)
admin.site.register(Quiz)
admin.site.register(Taken)
admin.site.register(UsersAnswer)