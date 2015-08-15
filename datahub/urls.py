from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^showtable/$', 'view.showdata.showTablePage', {'path': r'test\ex2data2.txt'}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'view.auth.showLogInPage'),
    url(r'^logout/$', 'view.auth.showLogOutPage'),
]
