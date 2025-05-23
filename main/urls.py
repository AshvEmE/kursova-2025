from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('save-plot/', views.save_plot, name='save_plot'),
    path('delete-plot/<int:plot_id>/', views.delete_plot, name='delete_plot'),
    path('edit-name/<int:plot_id>/', views.edit_plot_name, name='edit_plot_name'),
    path('update-name/<int:plot_id>/', views.update_plot_name, name='update_plot_name'),



]
