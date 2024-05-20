# SelectSampler package
This package allows you to fetch the dataset samples from the holoviews scatterplot as a dataframe. It only  works in Jupyter notebook environment. An example usage is the following:
   ```ipython
import numpy as np
sampler = ScatterSampler()
# Arbitrary datasets for demonstration
mat = np.random.randint(0, 100, (100, 2))
df = pd.DataFrame(mat, columns=['x', 'y'])
sampler.setup_holoviews()
sampler.setup_scatter(df, 'x', 'y')
scatter_chart = sampler.show_scatter_chart()
scatter_chart
```
```ipython
sampler.extract_df()
```

# Steps:
1. Run sampler.setup_holoviews() first to ensure you have the bokeh extension installed. 
2. Then run sampler.setup_scatter(df, 'x', 'y') to setup the scatter plot.
3.  Run sampler.show_scatter_chart() to display the scatter plot. You can select the samples on the sidebars of the scatter plot.
4. Finally, run sampler.extract_df() to get the selected samples in a dataframe (you need to run this in the separate cell).