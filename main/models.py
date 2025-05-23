from django.db import models
from django.conf import settings

class SavedPlot(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_plots')


    # Параметри моделі
    model = models.CharField(max_length=50)
    shape = models.CharField(max_length=20)

    # Комплексні значення як текст
    eps_m = models.CharField(max_length=50)
    eps_i = models.CharField(max_length=50)

    # Діапазон об'ємної частки
    f_range = models.CharField(max_length=50)


    # McLachlan параметри (опціонально)
    s_param = models.CharField(max_length=20, blank=True, null=True)
    t_param = models.CharField(max_length=20, blank=True, null=True)
    phi_c_param = models.CharField(max_length=20, blank=True, null=True)

    # Збережене зображення графіка
    image_base64 = models.TextField(blank=True, null=True)

    # Назва графіка
    name = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.model})"
