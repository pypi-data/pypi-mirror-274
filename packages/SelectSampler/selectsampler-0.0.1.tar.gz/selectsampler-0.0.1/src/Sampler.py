import pandas as pd
import panel as pn
import hvplot.pandas
import holoviews as hv


class ScatterSampler:
    def __init__(self, use_auto_setup=True):
        self.use_auto_setup = use_auto_setup
        if self.use_auto_setup:
            self.setup_holoviews()
        else:
            print("Please pip install bokeh manually.")
        
    def setup_holoviews(self):
        try:
            import bokeh
            hv.extension('bokeh')
        except ImportError:
            print("Bokeh is not installed. Please install bokeh using pip install bokeh.")
            
    def setup_scatter(self, df: pd.DataFrame, x_var: str, y_var: str):
        self.df = df
        self.x_var = x_var
        self.y_var = y_var
        self.scatter = df.hvplot.scatter(x_var, y_var, hover_cols=['index']).opts(tools=['hover', 'box_select',  'lasso_select', 'poly_select', 'tap'])
        self.select = hv.streams.Selection1D(source=self.scatter)
        
    def show_scatter_chart(self) -> hvplot:
        return self.scatter
    
    def extract_df(self) -> pd.DataFrame:
        return self.df.iloc[self.select.index]