import pandas as pd
from dash import Dash, dcc, html, Input, Output
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

# Read the data into pandas dataframe
spacex_df = pd.read_csv("dashboard_app\spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Get Launch Sites for dropdown
launch_sites = list(spacex_df['Launch Site'].unique())
launch_sites.append('All')

# Create a dash application
app = Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                dcc.Dropdown(launch_sites, 'All', id='site-dropdown'),
                                html.Br(),
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),
                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(min=min_payload, max=max_payload, step=1, value=[0,max_payload], id='payload-slider'),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# add callback decorator
@app.callback( Output(component_id='success-pie-chart', component_property='figure'),
               Input(component_id='site-dropdown', component_property='value'))

# Add computation to callback function and return graph
def get_success_graph(launch_site):
    # Select 2019 data
    if launch_site == 'All':
        df = spacex_df
        success_sum_df = df.groupby('Launch Site')['class'].sum().reset_index()
        return px.pie(success_sum_df, values='class', names='Launch Site', title='Successful Launch Locations')

    else:
        df = spacex_df[spacex_df['Launch Site']==launch_site]
         
        success_fail_df = df.groupby('class', as_index=False).count()
        success_fail_df['class'].replace([0,1],['Failed', 'Success'], inplace=True)
        return px.pie(success_fail_df, values='Launch Site', names='class', title='Population of European continent')
    
    # Group the data by Month and compute average over arrival delay time.

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
# add callback decorator
@app.callback( Output(component_id='success-payload-scatter-chart', component_property='figure'),
               [Input(component_id='payload-slider', component_property='value'),
               Input(component_id='site-dropdown', component_property='value')])

# Add computation to callback function and return graph
def get_payload_graph(min_max_payload, launch_site):
    # Select 2019 data
    df =  spacex_df[
        (spacex_df['Payload Mass (kg)']>=int(min_max_payload[0])) 
        & (spacex_df['Payload Mass (kg)']<=int(min_max_payload[1]))
    ]
    if launch_site != 'All':
        df = df[df['Launch Site']==launch_site]
    
    # Group the data by Month and compute average over arrival delay time.
    # line_data = df.groupby('Month')['ArrDelay'].mean().reset_index()

    return px.scatter(df, x='Payload Mass (kg)', y='class', title='Population of European continent')


# Run the app
if __name__ == '__main__':
    app.run_server()
