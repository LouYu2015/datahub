from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
	url(r'^showtable/$', 'view.showdata.showTablePage'),
    url(r'^admin/', include(admin.site.urls)),
]
