from django.conf.urls import url

from . import views

app_name = "taskpop"

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^home$', views.home, name='home'),
    url(r'^edit$', views.edit, name='edit'),
    url(r'^login$', views.login, name="login"),
    url(r'^logout', views.logout, name="logout"),
]
