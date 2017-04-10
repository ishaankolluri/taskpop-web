from django.conf.urls import url

from . import views

app_name = "taskpop"

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^login$', views.login, name="login"),

]