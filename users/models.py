from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_online = models.BooleanField(default=False)
    following = models.ManyToManyField(User, related_name="following", blank=True)
    friends = models.ManyToManyField(User, related_name="my_friends", blank=True)
    bio = models.CharField(max_length=150, blank=True)
    date_of_birth = models.CharField(max_length=5, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    image = models.ImageField(default='default_profile.png', upload_to='profiles_img', blank=True, null=True)

    def profile_posts(self):
        """
        чтобы установить связь между пользователем и постом, 
        напишите связанное имя модели в маленьком регистре, 
        а затем используйте _set.
        fields.name_model_relation + _set.method()
        """
        return self.user.post_set.all()# _set как постфикс
    
    def get_friends(self):
        return self.friends.all()
    
    def get_friends_no(self):
        return self.friends.all().count()
    
    def __str__(self):
        return f'{self.user.username} Profile'

STATUS_CHOICES = (
    ('send', 'send'),#Разобраться почему два send и accepted
    ('accepted', 'accepted'),
)

class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="friend_sender")
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="friend_receiver")
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"
