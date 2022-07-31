from django.urls import path
from django.views.decorators.cache import cache_page

from mainapp import views
from mainapp.apps import MainappConfig
from django.views.generic import RedirectView

app_name = MainappConfig.name

urlpatterns = [
    path('contacts/', views.ContactsView.as_view(), name="contacts"),

    #Courses
    path('courses/', cache_page(300)(views.CoursesListView.as_view()), name='courses',),
    path('courses/add/', views.CoursesCreateView.as_view(), name='courses_create'),
    path('courses/<int:pk>/update/', views.CoursesUpdateView.as_view(), name='courses_update'),
    path('courses/<int:pk>/detail/', views.CoursesDetailView.as_view(), name='courses_detail'),
    path('courses/<int:pk>/delete/', views.CoursesDeleteView.as_view(), name='courses_delete'),
    path("course_feedback/", views.CourseFeedbackFormProcessView.as_view(), name='course_feedback'),


    path('docsite/', views.DocSiteView.as_view(), name="docsite"),
    path('', views.IndexView.as_view(), name="index"),
    path('login/', RedirectView.as_view(url="authapp/login")),

    #News
    path('news/', views.NewsListView.as_view(), name='news'),
    path('news/add/', views.NewsCreateView.as_view(), name='news_create'),
    path('news/<int:pk>/update/', views.NewsUpdateView.as_view(), name='news_update'),
    path('news/<int:pk>/detail/', views.NewsDetailView.as_view(), name='news_detail'),
    path('news/<int:pk>/delete/', views.NewsDeleteView.as_view(), name='news_delete'),

    #Logs
    path('logs/', views.LogView.as_view(), name='logs_list'),
    path('logs/download/', views.LogDownloadView.as_view(), name='logs_download'),
]

