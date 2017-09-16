"""
Definition of urls for Blog.
"""

from datetime import datetime
from django.conf.urls import url, include
import django.contrib.auth.views
import app.views

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', app.views.home, name='home'),
    url(r'^about', app.views.about, name='about'),
    url(r'^search/$',
        app.views.search,
        name='search'),
    url(r'^search/category/(.+)$',
        app.views.searchCategory,
        name='searchCategory'),
    url(r'^search/author/(.+)$',
        app.views.searchAuthor,
        name='searchAuthor'),
    url(r'^submitPost/$',
        app.views.submitPost,
        name='submitPost'),
    url(r'^showPost/(\d+)/$',
        app.views.showPost,
        name='showPost'),
    url(r'^renderPost/$',
        app.views.renderPost,
        name='renderPost'),
    url(r'^createComment/$',
        app.views.createComment,
        name='createComment'),
    url(r'^register/$',
        app.views.registerUser,
        name='register'),
    url(r'^login/$',
        app.views.loginUser,
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout')

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    ]