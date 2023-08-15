from typing import Optional
from django.urls.base import reverse_lazy
#from django.urls.base import reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, CreateView, DetailView, DeleteView
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

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

class UserPostListView(ListView):
    # Модель Post в models.py
    model = Post

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
    def get_context_data(self, **kwargs):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        queryset = Post.objects.filter(author=user)
        context = super().get_context_data(**kwargs)
        context['blog_post_user_list'] = queryset.order_by('-date_created')
        # {'blog_post_user_list': queryset.order_by('-date_created')} для записи выше как словарь
        return context
    

        #queryset = Post.objects.filter(title__startswith). # с учетом регистра
        #queryset.order_by("-date_created")

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'blog_post_detail'


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
#https://docs.djangoproject.com/en/4.2/topics/auth/default/#django.contrib.auth.mixins.UserPassesTestMixin
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('/')
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