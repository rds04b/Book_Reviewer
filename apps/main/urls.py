from django.conf.urls import url
from . import views

app_name = 'main'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create$', views.create, name='create'),
    url(r'^delete/(?P<r_id>\d+)/(?P<b_id>\d+)$', views.delete, name='delete'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^login$', views.login, name='login'),
    url(r'^bookreview/(?P<id>\d+)$', views.bookreview, name='bookreview'),
    url(r'^edit_review/(?P<id>\d+)$', views.edit_review, name='edit_review'),
    url(r'^new_book$', views.new_book, name='new_book'),
    url(r'^new_review/(?P<id>\d+)$', views.new_review, name='new_review'),
    url(r'^user/(?P<id>\d+)$', views.user, name='user'),
    url(r'^bookhome$', views.bookhome, name='bookhome'),
    url(r'^book_entry$', views.book_entry, name='book_entry'),
    url(r'^like/(?P<id>\d+)$', views.like, name='like'),
    url(r'^book_like/(?P<id>\d+)/(?P<b_id>\d+)$', views.book_like, name='book_like'),
    url(r'^update_edit/(?P<id>\d+)/(?P<b_id>\d+)$', views.update_edit, name='update_edit'),
    ]
