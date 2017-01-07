from bokeh.io import curdoc
from bokeh.layouts import column, widgetbox
from bokeh.plotting import Figure
from bokeh.models import Plot, ColumnDataSource
from bokeh.models.widgets import Slider, Paragraph

from arrivaltimeslider import get_line_data_for_bokeh, get_patch_data_for_bokeh, U_Q_MIN, U_Q_MAX, U_Q_STEP

line_source  = ColumnDataSource()
patch_source = ColumnDataSource()

line_source  = ColumnDataSource(data=dict(x_cV=[],
                                          arrival_date=[],
                                          laying_date=[],
                                          hatching_date=[],))


patch_source = ColumnDataSource(data=dict(hatching_fill_x=[],
                                          hatching_fill_y=[],
                                          laying_fill_x=[],
                                          laying_fill_y=[],
                                          arrival_fill_x=[],
                                          arrival_fill_y=[],))

u_q_slider = Slider(
                title='u_q',
                name='u_q_slider',
                value=U_Q_MIN,
                start=U_Q_MIN,
                end=U_Q_MAX,
                step=U_Q_STEP,
                callback_policy='mouseup',
                )

toolset = 'crosshair,pan,reset,resize,save,wheel_zoom'

plot = Figure(
            plot_height=400,
            plot_width=400,
            tools=toolset,
            x_range=[130, 180],
            y_range=[110, 180],
            webgl=True,
            )

plot.patch('arrival_fill_x',  'arrival_fill_y',  source=patch_source, color='#D3D3D3')
plot.patch('hatching_fill_x', 'hatching_fill_y', source=patch_source, color='#000000')
plot.patch('laying_fill_x',   'laying_fill_y',   source=patch_source, color='#A9A9A9')

plot.line('x_cV', 'x_cV',          source=line_source, line_width=4, color='black')
plot.line('x_cV', 'arrival_date',  source=line_source, line_width=4, color='purple', legend='Arrival time')
plot.line('x_cV', 'laying_date',   source=line_source, line_width=4, color='red',    legend='Laying time')
plot.line('x_cV', 'hatching_date', source=line_source, line_width=4, color='green',  legend='Hatching date')

plot.legend.location = 'top_left'

def do_update():
    u_q = u_q_slider.value
    line_source.data  = get_line_data_for_bokeh(float(u_q))
    patch_source.data = get_patch_data_for_bokeh(float(u_q))

def update_data(attrname, old, new):
    do_update()

do_update()

u_q_slider.on_change('value', update_data)

inputs = widgetbox(u_q_slider)

title_paragraph = Paragraph(text='Phenology of two interdependent traits - bokehslider2017')

curdoc().title = 'Phenology of two interdependent traits'
curdoc().add_root(column(title_paragraph, plot, inputs))
