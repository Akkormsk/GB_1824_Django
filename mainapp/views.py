from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, ListView, DeleteView
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponse, Http404, JsonResponse

# from mainapp import models
from mainapp.forms import CourseFeedbackForm
from mainapp.models import News, Courses, Lessons, Teachers, CourseFeedback


def PageNotFound(request, exception):
    return HttpResponseNotFound('Sorry, страница не найдена')


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


class BaseListView(ListView):
    paginate_by = 5

    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class CoursesListView(BaseListView):
    model = Courses


class CoursesDetailView(DetailView):
    model = Courses
    # template_name = "mainapp/courses_detail.html"

    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["course_object"] = get_object_or_404(Courses, pk=self.kwargs.get('pk'))
        context["lessons"] = Lessons.objects.filter(course=context["course_object"])
        context["teachers"] = Teachers.objects.filter(course=context["course_object"])
        context["feedback_list"] = CourseFeedback.objects.filter(course=context["course_object"])
        if self.request.user.is_authenticated:
            if not CourseFeedback.objects.filter(course=context["course_object"], user=self.request.user).count():
                context["feedback_form"] = CourseFeedbackForm(course=context["course_object"], user=self.request.user)
        return context


class CourseFeedbackFormProcessView(LoginRequiredMixin, CreateView):
    model = CourseFeedback
    form_class = CourseFeedbackForm

    def form_valid(self, form):
        self.object = form.save()
        rendered_card = render_to_string("mainapp/includes/feedback_card.html", context={"item": self.object})
        return JsonResponse({"card": rendered_card})


class CoursesCreateView(PermissionRequiredMixin, CreateView):
    model = Courses
    fields = '__all__'
    success_url = reverse_lazy('mainapp:courses')
    permission_required = ('mainapp.add_courses',)


class CoursesUpdateView(PermissionRequiredMixin, UpdateView):
    model = Courses
    fields = '__all__'
    success_url = reverse_lazy('mainapp:courses')
    permission_required = ('mainapp.change_courses',)


class CoursesDeleteView(PermissionRequiredMixin, DeleteView):
    model = Courses
    success_url = reverse_lazy('mainapp:courses')
    permission_required = ('mainapp.delete_courses',)


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


class NewsListView(BaseListView):
    model = News


class NewsDetailView(DetailView):
    model = News


class NewsCreateView(PermissionRequiredMixin, CreateView):
    model = News
    fields = '__all__'
    success_url = reverse_lazy('mainapp:news')
    permission_required = ('mainapp.add_news',)


class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    model = News
    fields = '__all__'
    success_url = reverse_lazy('mainapp:news')
    permission_required = ('mainapp.change_news',)


class NewsDeleteView(PermissionRequiredMixin, DeleteView):
    model = News
    success_url = reverse_lazy('mainapp:news')
    permission_required = ('mainapp.delete_news',)
