import plotly.express as px
from PIL import Image

from kontrol_panel.models import Plot, Point, ImageData


class HTMLPlotter:
    def to_html(self, plot: Plot) -> str:
        raise NotImplementedError()


class PlotlyPlotter(HTMLPlotter):
    HEIGHT = 750

    def to_html(self, plot: Plot) -> str:
        data = None
        if plot.type in (Plot.Type.TYPE_LINE, Plot.Type.TYPE_SCATTER):
            points = Point.objects.order_by('x_value').filter(plot=plot.pk)
            data = {'x_value': [], 'y_value': [], 'legend': []}
            for point in points:
                data['x_value'].append(point.x_value)
                data['y_value'].append(point.y_value)
                data['legend'].append(point.group)
        elif plot.type in (Plot.Type.TYPE_IMAGE,):
            try:
                data = Image.open(ImageData.objects.order_by('id').filter(plot=plot.pk).last().value)
            except AttributeError:
                data = {'x_value': [], 'y_value': [], 'legend': []}

        if plot.type == Plot.Type.TYPE_LINE:
            if data['legend']:
                fig = px.line(data, x='x_value', y='y_value', color='legend', title=plot.title, height=self.HEIGHT)
            else:
                fig = px.scatter(data, x='x_value', y='y_value', color='legend', title=plot.title, height=self.HEIGHT)
        elif plot.type == Plot.Type.TYPE_SCATTER:
            fig = px.scatter(data, x='x_value', y='y_value', color='legend', title=plot.title, height=self.HEIGHT)
        elif plot.type == Plot.Type.TYPE_IMAGE:
            if isinstance(data, Image.Image):
                fig = px.imshow(data, title=plot.title, height=self.HEIGHT)
            else:
                fig = px.scatter(data, x='x_value', y='y_value', color='legend', title=plot.title, height=self.HEIGHT)
        else:
            raise NotImplementedError("Plot type %d is not implemented." % plot.type)
        fig.update_layout(hovermode='x')
        return fig.to_html(include_plotlyjs=True)
