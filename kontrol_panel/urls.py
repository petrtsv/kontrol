from django.urls import path

from kontrol_panel import views

app_name = 'kontrol_panel'
urlpatterns = [
    path('', views.index, name='index'),
    path('session/<int:session_id>', views.session_detail, name='session_detail'),
    path('session/new', views.new_session, name='new_session'),
    path('session/update', views.update_session, name='update_session'),
    path('session/plot/new', views.new_plot, name='new_plot'),
    path('session/plot/point/new', views.new_point, name='new_point'),
    path('session/plot/point/many_new', views.new_points, name='new_points'),
    path('session/plot/image/new', views.new_image, name='new_image'),
]
