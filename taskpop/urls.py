from django.conf.urls import url

from . import views

app_name = "taskpop"

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^home$', views.home, name='home'),
    url(r'^edit$', views.edit, name='edit'),
    url(r'^login$', views.login, name="login"),
    url(r'^logout', views.logout, name="logout"),
    url(r'^create', views.create, name="create"),
    url(r'^calendar', views.calendar, name="calendar"),
    url(r'^settings', views.settings, name="settings"),
    url(r'^complete/(?P<task_id>\d+)/', views.complete, name="complete"),
    url(r'^save/(?P<task_id>\d+)/', views.save, name="save"),
    url(r'^blowup/(?P<task_id>\d+)/', views.blowup, name="blowup"),
    url(r'^delete/(?P<task_id>\d+)/', views.delete, name="delete"),
    url(r'^session', views.session, name="session"),
    url(r'^deauth', views.deauth, name="deauth"),
    url(r'^firsttimeuser', views.firsttimeuser, name="firsttimeuser"),
]
