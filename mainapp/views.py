from django.conf import settings
from django.shortcuts import redirect
from django.views.generic import TemplateView
from datetime import datetime
import json
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponse, Http404

from mainapp.models import News


class ContactsView(TemplateView):
    template_name = "mainapp/contacts.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = [
            {
                'map': 'https://yandex.ru/map-widget/v1/-/CCUAZHcrhA',
                'city': 'Санкт‑Петербург',
                'phone': '+7-999-11-11111',
                'email': 'geeklab@spb.ru',
                'address': 'территория Петропавловская крепость, 3Ж'
            },
            {
                'map': 'https://yandex.ru/map-widget/v1/-/CCUAZHX3xB',
                'city': 'Казань',
                'phone': '+7-999-22-22222',
                'email': 'geeklab@kz.ru',
                'address': 'территория Кремль, 11, Казань, Республика Татарстан, Россия'
            },
            {
                'map': 'https://yandex.ru/map-widget/v1/-/CCUAZHh9kD',
                'city': 'Москва',
                'phone': '+7-999-33-11111',
                'email': 'geeklab@msk.ru',
                'address': 'Красная площадь, 7, Москва, Россия'
            }
        ]
        return context_data


class CoursesView(TemplateView):
    template_name = "mainapp/courses_list.html"


class DocSiteView(TemplateView):
    template_name = "mainapp/doc_site.html"


class IndexView(TemplateView):
    template_name = "mainapp/index.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = kwargs
        return context_data


class LoginView(TemplateView):
    template_name = "mainapp/login.html"


class NewsView(TemplateView):
    template_name = "mainapp/news.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = []
        # with open(settings.BASE_DIR / 'json_news.json', encoding='utf-8') as f:
        #     file_content = f.read()
        #     news_dict = json.loads(file_content)
        context_data['object_list'] = News.objects.all()
        # start = 5 * (kwargs["n"] - 1)
        # stop = start + 5
        # for i in range(start, stop):
        #     title, text = list(news_dict.items())[i]
        #     context_data['object_list'].append({
        #         'title': title,
        #         'text': text,
        #         'date': datetime.now()
        #     })
        context_data['prev'] = kwargs["n"] - 1
        context_data['next'] = kwargs["n"] + 1
        return context_data

    def get(self, *args, **kwargs):
        print(self.request.GET)
        st = self.request.GET.get('q', None)
        if st:
            return HttpResponseRedirect(f'https://yandex.ru/search/?text={st}&lr=213')
        return super().get(*args, **kwargs)


def PageNotFound(request, exception):
    return HttpResponseNotFound('Sorry, страница не найдена')


def test(request, n):
    if int(n) > 3:
        return redirect('mainapp:test')
    return HttpResponse(f'Test page {n}')
