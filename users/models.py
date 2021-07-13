from django.contrib.auth.models import User

# Making the Email field of the User as Unique
User._meta.get_field('email')._unique = True