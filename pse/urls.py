from django.contrib import admin
from django.urls import path
from monitor.views import index, chartfront, sektor, about, daftarasing, daftarlokal, search

admin.site.site_header = 'Database HCG'
admin.site.site_title = 'Database HCG'


handler404 = 'monitor.views.handler404'
handler500 = 'monitor.views.handler500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('source/chart/front/<str:tipe>/<str:status>', chartfront),
    path('source/chart/sektor/<str:tipe>', sektor),
    path('about', about),
    path('pse-asing/<str:slug>', daftarasing),
    path('pse-lokal/<str:slug>', daftarlokal),
    path('search', search)
]
