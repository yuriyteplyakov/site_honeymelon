from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from ckeditor.fields import RichTextField
#from django.utils.text import slugify
from pytils.translit import slugify #(сторонняя библиотека автозаполнения slug лучше использувать стандартную выше)
# pip install pytils
# postgresql - нужна

#from django.template.defaultfilters import slugify
from django.db.models.signals import pre_save #Сохранение до создания
from django.dispatch import receiver
# Create your models here.
# Класс

class Post(models.Model):
    """
    class - значит поддерживает методы
    модель содержит поля
    поля имеют настройки поведения
    """
    # мета опции
    class Meta:
        verbose_name = 'Создать пост'
        verbose_name_plural = 'Создать посты'
    # Поля модели
    title =models.CharField(max_length=200, help_text="не более 200 символов", db_index=True, verbose_name='Введите заголовок поста') # настройки полей
    # content = models.TextField(max_length=5000, blank=True, null=True, help_text="не более 5000 символов")
    content = RichTextField(max_length=5000, blank=True, null=True, help_text="не более 5000 символов")
    date_created = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='blog_cards/%Y/%m/%d', blank=True)
    date_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE) # null=True если анонимный пользователь create article
    # в url при использовании slug обязательно добавлять id + get_absolute_url()
    slug = models.SlugField(max_length=50) # unique=True для уникальности (подумать)
    likes_post = models.ManyToManyField(User, related_name='post_likes', blank=True, verbose_name='Лайки')
    #reply = models.ForeignKey('self', null=True, related_name='reply_ok', on_delete=models.CASCADE)
    saves_posts = models.ManyToManyField(User, related_name="blog_posts_save", blank=True, verbose_name='Сохранённые посты пользователя')


    """
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)
    """


    def total_likes_post(self):
        return self.likes.count()
    
    def total_saves_posts(self):
        return self.saves_posts.count()

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


    # методы модели
    def __str__(self):
        return self.title
    




@receiver(pre_save, sender=Post) #в декораторе указываем сигнал и с чем работать
def prepopulated_slug(sender, instance, **kwargs):
    instance.slug = slugify(instance.title)

""" Модель комментариев блога """
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments_blog", on_delete=models.CASCADE)
    name_author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    likes_comment = models.ManyToManyField(User, related_name="likes_blog_comment", blank=True)
    reply_comment = models.ForeignKey('self', null=True, related_name="replies_comment", on_delete=models.CASCADE)
    
    def total_likes_comment(self):
        return self.likes_comment.count()
    
    def __str__(self):
        return "%s - %s - %s" %(self.post.title, self.name_author, self.id)
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})