from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'view.auth.showLogInPage'),
    url(r'^logout/$', 'view.auth.showLogOutPage'),
    url(r'^upload/(?P<username>[^/]+)/(?P<path>.*)$', 'view.fileManager.showUploadPage'),
    url(r'^view/(?P<username>[^/]+)/(?P<path>.*)$', 'view.fileManager.showFileOrFolder'),
]
