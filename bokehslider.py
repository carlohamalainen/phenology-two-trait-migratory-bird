import logging

logging.basicConfig(level=logging.DEBUG)

import numpy as np

from bokeh.plotting import figure
from bokeh.models import Plot, ColumnDataSource
from bokeh.properties import Instance
from bokeh.server.app import bokeh_app
from bokeh.server.utils.plugins import object_page
from bokeh.models.widgets import HBox, Slider, VBoxForm


from arrivaltimeslider import get_line_data_for_bokeh, get_patch_data_for_bokeh, U_Q_MIN, U_Q_MAX, U_Q_STEP

class PhenoApplication(HBox):
    extra_generated_classes = [["PhenoApplication", "PhenoApplication", "HBox"]]

    inputs = Instance(VBoxForm)

    u_q_slider = Instance(Slider)

    plot = Instance(Plot)
    line_source  = Instance(ColumnDataSource)
    patch_source = Instance(ColumnDataSource)

    @classmethod
    def create(cls):
        """
        One-time creation of resources.
        """
        obj = cls()

        obj.line_source  = ColumnDataSource(data=dict(
                                                    x_cV=[],
                                                    arrival_date=[],
                                                    laying_date=[],
                                                    hatching_date=[],))


        obj.patch_source = ColumnDataSource(data=dict(
                                                    hatching_fill_x=[],
                                                    hatching_fill_y=[],
                                                    laying_fill_x=[],
                                                    laying_fill_y=[],
                                                    arrival_fill_x=[],
                                                    arrival_fill_y=[],))

        obj.u_q_slider = Slider(
                        title='u_q',
                        name='u_q_slider',
                        value=U_Q_MIN,
                        start=U_Q_MIN,
                        end=U_Q_MAX,
                        step=U_Q_STEP
                        )

        toolset = 'crosshair,pan,reset,resize,save,wheel_zoom'

        plot = figure(
                    plot_height=400,
                    plot_width=400,
                    tools=toolset,
                    x_range=[130, 180],
                    y_range=[110, 180],
                    )

        plot.patch('arrival_fill_x',  'arrival_fill_y',  source=obj.patch_source, color='#D3D3D3')
        plot.patch('hatching_fill_x', 'hatching_fill_y', source=obj.patch_source, color='#000000')
        plot.patch('laying_fill_x',   'laying_fill_y',   source=obj.patch_source, color='#A9A9A9')

        plot.line('x_cV', 'x_cV',          source=obj.line_source, line_width=4, color='black')
        plot.line('x_cV', 'arrival_date',  source=obj.line_source, line_width=4, color='purple', legend='Arrival time')
        plot.line('x_cV', 'laying_date',   source=obj.line_source, line_width=4, color='red',    legend='Laying time')
        plot.line('x_cV', 'hatching_date', source=obj.line_source, line_width=4, color='green',  legend='Hatching date')

        plot.legend.orientation = 'top_left'

        obj.plot = plot
        obj.update_data()

        obj.inputs = VBoxForm(children=[obj.plot, obj.u_q_slider])

        obj.children.append(obj.inputs)

        return obj

    def setup_events(self):
        super(PhenoApplication, self).setup_events()
        if not self.u_q_slider: return
        getattr(self, 'u_q_slider').on_change('value', self, 'input_change')

    def input_change(self, obj, attrname, old, new):
        self.update_data()

    def update_data(self):
        u_q = self.u_q_slider.value

        logging.debug('PARAMS: u_q: %s', u_q)

        self.line_source.data  = get_line_data_for_bokeh(float(u_q))
        self.patch_source.data = get_patch_data_for_bokeh(float(u_q))

# Serves the URL /bokeh/phenology-two-trait-migratory-bird
@bokeh_app.route("/bokeh/phenology-two-trait-migratory-bird/")
@object_page("phenology")
def make_sliders():
    app = PhenoApplication.create()
    return app
