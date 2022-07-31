from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, ListView, DeleteView, View
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponse, Http404, JsonResponse, FileResponse
from mainapp.forms import CourseFeedbackForm, MailFeedbackForm
from mainapp.models import News, Courses, Lessons, Teachers, CourseFeedback
import logging
from django.core.cache import cache
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from mainapp import tasks

logger = logging.getLogger(__name__)


def PageNotFound(request, exception):
    return HttpResponseNotFound('Sorry, страница не найдена')


class ContactsView(TemplateView):
    template_name = "mainapp/contacts.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context_data["form"] = MailFeedbackForm(user=self.request.user)
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

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            cache_lock_flag = cache.get(f"mail_feedback_lock_{self.request.user.pk}")
            if not cache_lock_flag:
                cache.set(
                    f"mail_feedback_lock_{self.request.user.pk}",
                    "lock",
                    timeout=60,
                )
                messages.add_message(self.request, messages.INFO, _("Message sent"))
                tasks.send_feedback_mail.delay(self.request.POST.get("user_id"), self.request.POST.get("message"))
            else:
                messages.add_message(
                    self.request,
                    messages.WARNING,
                    _("You can send only one message per 5 minutes"),
                )
        return HttpResponseRedirect(reverse_lazy("mainapp:contacts"))


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
        feedback_list_key = f'course_feedback_{context["course_object"].pk}'
        cached_feedback_list = cache.get(feedback_list_key)
        if cached_feedback_list is None:
            context["feedback_list"] = CourseFeedback.objects.filter(course=context["course_object"]).select_related()
            cache.set(feedback_list_key, context["feedback_list"], timeout=300)
        else:
            context["feedback_list"] = cached_feedback_list

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


class LogView(UserPassesTestMixin, TemplateView):
    template_name = 'mainapp/logs.html'

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        log_lines = []
        with open(settings.BASE_DIR / "var/log/main_log.log") as log_file:
            for i, line in enumerate(log_file):
                if i == 1000:
                    break
                log_lines.insert(0, line)
            context_data['logs'] = log_lines
        return context_data


class LogDownloadView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, *args, **kwargs):
        return FileResponse(open(settings.LOG_FILE, 'rb'))
