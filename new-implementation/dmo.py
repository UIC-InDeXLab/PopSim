import pandas as pd
import qgrid
import ipywidgets as widgets
from IPython.display import display

# Create a Pandas DataFrame
data = {
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'gender': ['Female', 'Male', 'Male']
}
df = pd.DataFrame(data)

# Create a QGrid widget
grid = qgrid.show_grid(df)

# Create an output widget to display the selected row
output = widgets.Output()

# Create a callback function for row clicks
def on_row_click(event, grid_widget, widget):
    # Get the clicked row index
    index = grid_widget.get_selected_rows()[0]
    
    # Get the row data
    row = grid_widget.get_df().iloc[index]
    
    # Do something with the row data (e.g. display it)
    with widget:
        widget.clear_output()
        print(row.to_dict())

# Add a click event listener to the grid widget
grid.on('selection_changed', lambda event: on_row_click(event, grid, output))

# Display the widgets
display(grid, output)
