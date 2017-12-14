from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from .import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^submit_leader/', views.submit_leader, name='submit_leader'),
    url(r'^create_tag/', views.create_tag, name='create_tag'),
    url(r'^create_leader_tag/', views.create_leader_tag, name='create_leader_tag'),
    url(r'^leader/(\d+)',views.leader,name='leader'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
