from django.contrib import admin
from .models import SavedPlot

@admin.register(SavedPlot)
class SavedPlotAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'model', 'shape', 'created_at')
    list_filter = ('model', 'shape', 'created_at')
    search_fields = ('name', 'user__username')
