from typing import Any, Dict, Optional
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.urls.base import reverse_lazy
#from django.urls.base import reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from blog.models import Post, Review, Comment
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
import random

from blog.forms import CommentForm

# first
#COMPLETED: [x] Завершена
def index(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/index.html', context)


"""
# Create your views here.
! Что выбрать для написания представления и почему?
! От чего это зависит?
! Какую стратегию выбрать и чему учиться?

? Функцию - простые действия, понятно до конца:
todo - Выборка объектов QuerySet (api моделей)
todo - Менеджер свой личный
todo - Методы модели

? Классы:
todo - Выборка объектов QuerySet (api моделей)
    todo - Когда точно знаем, что это не последнее изменение
    todo - Расширяемый подход
    todo - Миксины
    todo - Удобство (работы с частями, имеет значение правка кода, например в шаблонах)
    todo - Менеджер свой личный
    todo - Методы модели

Миксины (примесь) - добавляет действие к классу

? Менеджер свой личный

? Методы модели

Максимум подход

! Вокруг чего все крутится?
    #todo Разместить данные в модели (API методы)
    #todo Извлечь их оттуда как, сколько (мы делаем представление, чтобы работать с API методами модели)
    #todo Показать как и где

Конструкция класс - почему?
Максимальное расширение проекта и возможности написать, переписать под любые нужды
Засчет чего?

0. Переопределение методов
1. Множественное наследование
2. Использование миксинов
3. Использование собственных менеджеров выборки с базы
4. Использование методов модели
5. Декораторы
"""

""" Posts of following user profiles """
# TODO: делать
@login_required
def posts_of_following_profiles(request):
    pass


""" Post Like """
# TODO: делать
@login_required
def LikeView(request):
    pass


""" Post save """
# TODO: делать SaveView сохранение постов
@login_required
def SaveView(request):
    pass


""" Like post comments """
# TODO: делать
@login_required
def LikeCommentView(request): # , id1, id2              id1=post.pk id2=reply.pk
    pass


""" Home page with all posts """
# WORK: делаю
# FIXME BUG html
class HomePostListViewAllUsers(ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name = "posts"
    ordering = ["-date_created"]
    paginate_by = 3
    # https://docs.djangoproject.com/en/4.1/ref/class-based-views/
    def get_context_data(self, *args, **kwargs):
        context = super(HomePostListViewAllUsers, self).get_context_data()# разобрать метод super
        users = list(User.objects.exclude(pk=self.request.user.pk))# исключаем с помощью exclude (записи будут выводиться без учета редактирования)
        if len(users) > 3:
            out = 3
        else:
            out = len(users)
        random_user = random.sample(users, out)
        context["random_users"] = random_user
        return context


""" All the posts of the user """

# BUG: исправить нет пагинации paginate_by = 5, 
# https://docs.djangoproject.com/en/4.1/ref/class-based-views/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.paginate_by

class UserPostListView(ListView):
    # Модель Post в models.py
    paginate_by = 4
    model = Post
    context_object_name = 'blog_post_user_list'

    # Имя шаблона html
    template_name = 'blog/user_posts.html'
    

    # objects, model_постфикс, наш вариант
    # контекст переменная хранения данных
    # представление-модель-что это

    """
    context_object_name = 'blog_post_user_list' # вместо стандартного objects

    # пишем выборку
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username')) # (HTTP методы GET и POST)
        return Post.objects.filter(author=user).order_by('date_created')
    
"""
    
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username')) # (HTTP методы GET и POST)
        return Post.objects.filter(author=user).order_by('-date_created')
        # {'blog_post_user_list': queryset.order_by('-date_created')} для записи выше как словарь
        #return context
    

        #queryset = Post.objects.filter(title__startswith). # с учетом регистра
        #queryset.order_by("-date_created")


""" Create post """
# COMPLETED: [x] - завершено
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
""" About page """
# TODO: делать
def about(request):
    pass 

""" Search by post title or username """
# TODO: делать
def search(request):
    pass 


""" Liked posts """
# TODO: делать
@login_required
def AllLikeView(request):
    pass
    
# BUG сначала написать лайки и сохранение
""" Post detail view 
# WORK: сейчас делаю.
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'blog_post_detail'
"""

def post_detail_view(request, pk):
    # source stuff
    handle_page = get_object_or_404(Post, id=pk)
    # example blog_views_PostDetailView.ipynb
    total_comments = handle_page.comments_blog.all().filter(reply_comment=None).order_by('-id')
    total_comments2 = handle_page.comments_blog.all().order_by('-id')
    total_likes = handle_page.total_likes_post()
    total_saves = handle_page.total_saves_posts()
    # RELATED APP notification
    context = {}

    if request.method == "POST":
        comment_qs = None
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            form = request.POST.get("body")
            comment = Comment.objects.create(name_author=request.user,
                                             body = form,
                                             post=handle_page,
                                             reply_comment=comment_qs)
            comment.save()
            total_comments = handle_page.comments_blog.all().filter(reply_comment=None).order_by('-id')
    else:
        comment_form = CommentForm()
    context['comment_form'] = comment_form
    context["comments"] = total_comments
    context["post"] = handle_page
    return render(request, 'blog/post_detail.html', context)
# часть 6
# 6. Сделаем заголовки статей ссылками.
"""
# На сегодня этот код кривой в моём понимании, но суть в другом, можно писать что угодно. Код работает, но сегодня я бы просто использовал
LoginRequiredMixin, а прямо в классе CourseCreateView прописал бы проверку на группу и пере направление, иными словами UserSettingsViewMixin можно было вообще убрать.


class UserSettingsViewMixin(UserPassesTestMixin, View):
    def not_in_student_a_group2(self, user):
        if user:
            return user.groups.filter(
                name='old_school_before_2020').count() == 0  # d скобках указывается группа, для проверки входит ли в неё пользователь
        return False

    def get_login_url(self):
        if not self.request.user.is_authenticated:
            return super(UserSettingsView, self).get_login_url()
        else:
            # пере направление
            return '/students/NoAccess/'
"""

""" Delete post """
# import LoginRequiredMixin, UserPassesTestMixin,
# COMPLETED: [x] - завершено
#https://docs.djangoproject.com/en/4.2/topics/auth/default/#django.contrib.auth.mixins.UserPassesTestMixin
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = ('/')
    template_name = 'blog/delete_post.html'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

#https://docs.djangoproject.com/en/4.2/ref/urlresolvers/#reverse-lazy
"""


class CourseCreateView(UserSettingsViewMixin, PermissionRequiredMixin, OwnerCourseEditMixin, CreateView):
    permission_required = 'courses.add_course'
    
    def test_func(self, user):
        group = 'a_group2'
        return group
    
    def test_func(self, user):
        if user:
            return user.groups.filter(
                    name='old_school_before_2020').count() == 0  # d скобках указывается группа, для проверки входит ли в неё пользователь
        return False
"""

""" Главная страница со всеми сообщениями
в проекте first у нас index
"""

""" Update post """
# COMPLETED: [x] - завершено
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
""" Saved posts """
# TODO: делать
@login_required
def AllSaveView(request):
    pass


# представление для отзывов

def gallery_view(request):
    reviews = Review.objects.all()
    return render(request, 'blog/reviews.html', {'reviews': reviews})