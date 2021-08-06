from .models import News, Category
from .forms import NewsForm, RegisterUserForm, UserLoginForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy


class HomeNews(ListView):
    model = News
    template_name = 'news/index.html'
    context_object_name = 'data'
    paginate_by = 2

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context


class NewsCategory(ListView):
    model = News
    template_name = 'news/category.html'
    context_object_name = 'news'
    allow_empty = False

    paginate_by = 2

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True)
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context


class ViewNews(DetailView):
    model = News
    template_name = 'news/view_news.html'
    context_object_name = 'news_item'


class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    success_url = reverse_lazy('home')
    login_url = '/admin/'


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Вы успешно зарегистрировались!')
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации!')
    else:
        form = RegisterUserForm()
    return render(request, 'news/register.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')
