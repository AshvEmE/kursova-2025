from django.shortcuts import redirect, render, get_object_or_404
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import numpy as np
from .models import SavedPlot
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods

from .em_models import (
    maxwell_garnett_eps,
    bruggeman_eps,
    coherent_potential_eps,
    mclachlan_eps
)


@login_required
@require_http_methods(["GET"])
def edit_plot_name(request, plot_id):
    plot = get_object_or_404(SavedPlot, id=plot_id, user=request.user)
    return render(request, 'main/edit_name_form.html', {'plot': plot})


@login_required
@require_http_methods(["POST"])
def update_plot_name(request, plot_id):
    plot = get_object_or_404(SavedPlot, id=plot_id, user=request.user)
    new_name = request.POST.get('name', '').strip()
    if new_name:
        plot.name = new_name
        plot.save()
    return HttpResponse(f'<h5 hx-get="{request.build_absolute_uri()}" hx-trigger="click" hx-target="this" hx-swap="outerHTML" class="editable-title" style="cursor: pointer;">{plot.name}</h5>')




def plot_graph(model_func, eps_m, eps_i, f_range):
    re_vals, im_vals = [], []
    for f in f_range:
        eff = model_func(eps_m, eps_i, f)
        if eff is not None:
            re_vals.append(eff.real)
            im_vals.append(eff.imag)
        else:
            re_vals.append(np.nan)
            im_vals.append(np.nan)

    plt.figure()
    plt.plot(f_range, re_vals, label="Re(ε)-1")
    plt.plot(f_range, im_vals, label="Im(ε)-1")
    plt.xlabel("Volume fraction")
    plt.ylabel("Effective dielectric permittivity")
    plt.legend()


    plt.grid(True)

    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close()

    return base64.b64encode(buf.getvalue()).decode("utf-8")


def index(request):
    if not request.user.is_authenticated:
        return redirect('login')

    plot_data = None
    error = None

    if request.method == "POST":
        try:
            model = request.POST.get('model')
            shape = request.POST.get('shape')
            eps_m = complex(request.POST.get('eps_m', '').replace(' ', ''))
            eps_i = complex(request.POST.get('eps_i', '').replace(' ', ''))

            f_range_str = request.POST.get('f_range', '')
            f_parts = [float(x.strip()) for x in f_range_str.split(',')]
            if len(f_parts) != 3:
                raise ValueError("Volume fraction must contain start, end, and step.")

            f_start, f_end, f_step = f_parts
            if f_step <= 0:
                raise ValueError("Step must be positive.")

            f_range_str = request.POST.get('f_range', '')
            f_parts = [float(x.strip()) for x in f_range_str.split(',')]
            if len(f_parts) != 3:
                raise ValueError("Volume fraction must contain start, end, and step.")

            f_start, f_end, f_step = f_parts
            if f_step <= 0:
                raise ValueError("Step must be positive.")

            # Використовуємо np.linspace для стабільної побудови діапазону з дробовим step
            num_points = int((f_end - f_start) / f_step) + 1
            f_range = np.linspace(f_start, f_start + f_step * (num_points - 1), num_points)




            if model == "Maxwell-Garnett":
                func = lambda em, ei, f: maxwell_garnett_eps(em, ei, f, shape)
            elif model == "Bruggeman":
                func = lambda em, ei, f: bruggeman_eps(em, ei, f)
            elif model == "Coherent Potential":
                func = lambda em, ei, f: coherent_potential_eps(em, ei, f, shape)
            elif model == "McLachlan":
                s = float(request.POST.get('s_param', '1.0'))
                t = float(request.POST.get('t_param', '1.0'))
                phi_c = float(request.POST.get('phi_c_param', '0.5'))
                func = lambda em, ei, f: mclachlan_eps(em, ei, f, s, t, phi_c)
            else:
                raise ValueError("Unsupported model selected.")

            plot_data = plot_graph(func, eps_m, eps_i, f_range)

        except ValueError as ve:
            error = f"Input error: {ve}"
        except Exception as e:
            error = f"Unexpected error: {str(e)}"

    return render(request, 'main/index.html', {
        'plot': plot_data,
        'error': error,
    })


@require_POST
@login_required
def delete_plot(request, plot_id):
    plot = get_object_or_404(SavedPlot, id=plot_id, user=request.user)
    plot.delete()
    return redirect('dashboard')


@login_required
def dashboard(request):
    saved_plots = SavedPlot.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'main/dashboard.html', {'saved_plots': saved_plots})


@login_required
def save_plot(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        model = request.POST.get('model')
        shape = request.POST.get('shape')
        eps_m = request.POST.get('eps_m')
        eps_i = request.POST.get('eps_i')
        f_range = request.POST.get('f_range')
        s_param = request.POST.get('s_param')
        t_param = request.POST.get('t_param')
        phi_c_param = request.POST.get('phi_c_param')
        image_base64 = request.POST.get('image_base64')

        SavedPlot.objects.create(
            user=request.user,
            name=name,
            model=model,
            shape=shape,
            eps_m=eps_m,
            eps_i=eps_i,
            f_range=f_range,
            s_param=s_param,
            t_param=t_param,
            phi_c_param=phi_c_param,
            image_base64=image_base64,
        )
        return HttpResponse(status=204)  # No content — не оновлює сторінку
