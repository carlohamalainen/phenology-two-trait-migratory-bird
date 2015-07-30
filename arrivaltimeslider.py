import os.path
import numpy as np
import matplotlib.pyplot as plt
import pickle

from pywrapper import solvedbo

U_Q_MIN  = 125
U_Q_MAX  = 140
U_Q_STEP = 1

pickled_data_file = os.path.join(os.path.abspath(os.path.curdir), 'arrival_times.p')

try:
    (_U_Q_MIN, _U_Q_MAX, _U_Q_STEP, u_q_values, data) = pickle.load(open(pickled_data_file, 'rb'))

    recompute = _U_Q_MIN != U_Q_MIN or _U_Q_MAX != U_Q_MAX or _U_Q_STEP != U_Q_STEP
except:
    recompute = True

if recompute:
    # This can take a few minutes.
    data = {}

    u_q_values = np.arange(U_Q_MIN, U_Q_MAX + 1, U_Q_STEP)

    for u_q in u_q_values:
        data[u_q] = solvedbo(u_q)

    pickle.dump((U_Q_MIN, U_Q_MAX, U_Q_STEP, u_q_values, data,), open(pickled_data_file, 'wb'))
else:
    (U_Q_MIN, U_Q_MAX, U_Q_STEP) = (_U_Q_MIN, _U_Q_MAX, _U_Q_STEP)

def get_data(u_q):
    x_cV = data[u_q]['x_cV']
    yzV  = data[u_q]['yzV']
    nV   = data[u_q]['nV']
    z_n  = data[u_q]['z_n']

    x_cV = x_cV[0, :]

    arrival_date  = yzV[:, 0]
    laying_date   = yzV[:, 0] + yzV[:,1]
    hatching_date = yzV[:,0] + yzV[:, 1] + z_n

    return (x_cV, arrival_date, laying_date, hatching_date,)

def get_line_data_for_bokeh(u_q):
    (x_cV, arrival_date, laying_date, hatching_date,) = get_data(u_q)

    return { 'x_cV':            x_cV,
             'arrival_date':    arrival_date,
             'laying_date':     laying_date,
             'hatching_date':   hatching_date,
           }

def fill_between(x1, y1, x2, y2):
    """
    Similar to matplotlib's fill_between. We use this
    output in bokeh's patch() function.
    """

    new_x = np.append(x1.tolist(), x2.tolist()[::-1])
    new_y = np.append(y1.tolist(), y2.tolist()[::-1])

    return (new_x, new_y)

def get_patch_data_for_bokeh(u_q):
    (x_cV, arrival_date, laying_date, hatching_date,) = get_data(u_q)

    # ax.fill_between(x_cV, x_cV, hatching_date, facecolor='black')
    (hatching_fill_x, hatching_fill_y) = fill_between(x_cV, x_cV, x_cV, hatching_date)

    # ax.fill_between(x_cV, x_cV, laying_date,   facecolor='0.4')
    (laying_fill_x, laying_fill_y) = fill_between(x_cV, x_cV, x_cV, laying_date)

    # ax.fill_between(x_cV, laying_date, arrival_date,  facecolor='0.7')
    (arrival_fill_x, arrival_fill_y) = fill_between(x_cV, laying_date, x_cV, arrival_date)

    return { 'hatching_fill_x': hatching_fill_x,
             'hatching_fill_y': hatching_fill_y,
             'laying_fill_x':   laying_fill_x,
             'laying_fill_y':   laying_fill_y,
             'arrival_fill_x':  arrival_fill_x,
             'arrival_fill_y':  arrival_fill_y,
           }

def plot(u_q):
    """
    fig, ax = plt.subplots(figsize=(4, 3),
                           subplot_kw={'axisbg':'#EEEEEE',
                                       'axisbelow':True})
    ax.grid(color='w', linewidth=2, linestyle='solid')
    x = np.linspace(0, 10, 1000)
    ax.plot(x, amplitude * np.sin(x), color=color,
            lw=5, alpha=0.4)
    ax.set_xlim(0, 10)
    ax.set_ylim(-1.1, 1.1)
    return fig
    """

    fig, ax = plt.subplots(figsize=(6, 5),
                           subplot_kw={'axisbg':'#EEEEEE',
                                       'axisbelow':True})

    (x_cV, arrival_date, laying_date, hatching_date,) = get_data(u_q)

    ax.plot(x_cV, x_cV,          color='black')
    ax.plot(x_cV, arrival_date,  linewidth=4, color='purple', label='Arrival time')
    ax.plot(x_cV, laying_date,   linewidth=4, color='red',    label='Laying time')
    ax.plot(x_cV, hatching_date, linewidth=4, color='green',  label='Hatching date')

    ax.fill_between(x_cV, x_cV, hatching_date, facecolor='black')
    ax.fill_between(x_cV, x_cV, laying_date,   facecolor='0.4')
    ax.fill_between(x_cV, laying_date, arrival_date,  facecolor='0.7')
    ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    ax.set_xlim((140, 170))
    ax.set_ylim((120, 160))

    return fig

# from ipywidgets import StaticInteract, RangeWidget
# static_interact_arrival_times = StaticInteract(plot, u_q=RangeWidget(u_q_values[0], u_q_values[-1], u_q_values[1] - u_q_values[0]))
