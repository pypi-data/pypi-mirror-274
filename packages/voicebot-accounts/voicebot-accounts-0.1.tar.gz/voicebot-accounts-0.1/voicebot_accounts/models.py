from __future__ import annotations
# from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# class UserManager(BaseUserManager):
#     def create_user(
#         self, email: str, password: str | None = None, **other_fields
#     ) -> User: 
#         user = User(email=email, **other_fields)
        
#         if password: 
#             user.set_password(password)
#         else:
#             user.set_unusable_password()
            
#         user.save()
#         return user
    
#     def create_superuser(self, email: str, password: str | None = None, **other_fields) -> User:
#         other_fields.setdefault("is_staff", True)
#         other_fields.setdefault("is_superuser", True)
#         other_fields.setdefault("is_active", True)
        
#         if other_fields.get("is_staff") is not True:
#             raise ValueError("Superuser must be assigned to is_staff=True.")
#         if other_fields.get("is_superuser") is not True:
#             raise ValueError("Superuser must be assigned to is_superuser=True.")
        
#         return self.create_user(email, password, **other_fields)
    
    

# class User(AbstractUser):

#     # remove default fields
#     first_name : str = models.CharField(max_length=60, null=True)
#     last_name : str = models.CharField(max_length=60, null=True)

#     email: str = models.EmailField("Email Address", unique=True)
#     username: str = models.CharField(max_length=60)
#     token_name : str = models.CharField(max_length=60, null=True)
    
#     bio: str = models.TextField(blank=True)
#     image: str | None = models.URLField(null=True, blank=True)

#     followers = models.ManyToManyField("self", blank=True, symmetrical=False)

#     EMAIL_FIELD = "email"
#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS: list[str] = []

#     objects = UserManager()


#     def get_full_name(self) -> str:
#         if self.first_name and self.last_name:
#             return f"{self.first_name} {self.last_name}"
#         else: 
#             return self.username
       

#     def get_short_name(self) -> str:
#         if self.first_name and self.last_name:
#             return f"{self.first_name[0]}{self.last_name}"
#         else:
#             return self.username


class ConnectorToken(models.Model):
    credentials = models.TextField()

class Connectors(models.Model):

    connector_name = models.CharField(max_length=60)
    connecting_to = models.CharField(max_length=60)
    date_created = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token_email = models.CharField(max_length=60, null=True)
    token = models.ForeignKey(ConnectorToken, on_delete=models.CASCADE, null=True)

class PhoneNumber(models.Model):

    number = models.CharField(max_length=60)
    number_type = models.CharField(max_length=60)
    feature = models.CharField(max_length=60)
    cost = models.CharField(max_length=60)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

class Agents(models.Model):

    AGENT_CHOICES = [
        ('incoming', 'Incoming'),
        ('outgoing', 'Outgoing'),
        ('batch', 'Batch'),
    ]

    agent_name = models.CharField(max_length=60)
    agent_type = models.CharField(max_length=20, choices=AGENT_CHOICES)
    prompt = models.TextField()
    connector = models.ForeignKey(Connectors, on_delete=models.CASCADE, null=True)
    first_sentence = models.CharField(max_length=256,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    phone_number = models.ForeignKey(PhoneNumber, on_delete=models.CASCADE, null=True)

class CallLogs(models.Model):

    call_id = models.CharField(max_length=60)
    connector = models.ForeignKey(Connectors, on_delete=models.CASCADE, null=True)
    analysis = models.TextField(null=True, blank=True)