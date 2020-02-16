from django.conf.urls import url
from .views import FileView, TestView
urlpatterns = [
  url(r'^upload/$', FileView.as_view(), name='file-upload'),
  url(r'^test/$', TestView.as_view(), name='test'),
]
