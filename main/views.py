from django.shortcuts import redirect, render
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import numpy as np

from .em_models import (
    maxwell_garnett_eps,
    bruggeman_eps,
    coherent_potential_eps,
    mclachlan_eps
)


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

            f_range = np.arange(f_start, f_end + f_step, f_step)

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


def dashboard(request):
    return render(request, 'main/dashboard.html')
