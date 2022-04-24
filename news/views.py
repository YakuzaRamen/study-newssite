from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView

from .models import News, Category
from .forms import NewsForm

"""Возвращает список всех новостей"""


class HomeNews(ListView):
    model = News
    template_name = 'news\home_news_list.html'
    context_object_name = 'news'

    def get_queryset(self):
        return News.objects.filter(is_published=True)


"""Возвращает список всех новостей (используется с index.html)"""


def index(request):
    news = News.objects.all()
    context = {
        'news': news,
        'title': 'Список новостей'
    }

    return render(request, 'news/index.html', context=context)


"""Возвращает категорию новости"""


def get_category(request, category_id):
    news = News.objects.filter(category_id=category_id)
    category = Category.objects.get(pk=category_id)
    context = {
        'news': news,
        'category': category
    }
    return render(request, 'news/category.html', context=context)


"""Возвращает конкретную новость"""


def view_news(request, news_id):
    news_item = get_object_or_404(News, pk=news_id)
    return render(request, 'news/view_news.html', {"news_item": news_item})


"""Добавляет новость на сайт"""


def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            # раскоментить при использовании формы без использовании модели
            #     news = News.objects.create(**form.cleaned_data)
            # использовать при варианте связанным с моделью
            news = form.save()
            return redirect(news)
    else:
        form = NewsForm()
    return render(request, 'news/add_news.html', {'form': form})
