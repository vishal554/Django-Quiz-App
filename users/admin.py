from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Question)
admin.site.register(FIB_Question)
admin.site.register(MCQ_Question)
admin.site.register(Quiz)
admin.site.register(Taken)
admin.site.register(users_answer)