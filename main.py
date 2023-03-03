import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

import configparser
from configparser import *

from jupyter_dash import JupyterDash
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

config = configparser.ConfigParser()
config.read('config.ini')
mapbox_token = config['mapbox']['secret_token']

mono_dark1 = 'mapbox://styles/lomska/cle4k9abk002101qge1oscl16'

href1 = 'https://qz.com/1183992/why-europe-was-overrun-by-witch-hunts-in-early-modern-history'
href2 = 'http://emiguel.econ.berkeley.edu/assets/miguel_research/45/_Paper__Poverty_and_Witch_Killing.pdf'
href3 = 'https://www.journals.uchicago.edu/doi/10.1086/674900'
href4 = 'https://scholarsarchive.byu.edu/cgi/viewcontent.cgi?article=1889'
href5 = 'https://oll.libertyfund.org/title/roper-the-crisis-of-the-seventeenth-century'
href6 = 'https://en.wikipedia.org/wiki/W%C3%BCrzburg_witch_trials'

all_scatter = pd.read_csv('app_data/data_scattermapbox.csv', index_col=['decade', 'place'])
all_scatter_total = pd.read_csv('app_data/data_scattermapbox_total.csv', index_col='place')
trials_net = pd.read_csv('app_data/data_scattertimeline.csv')
treemap = pd.read_csv('app_data/data_treemap.csv')

colorscale = [[0.0, "#0F3A49"], [0.1, "#0F3A49"], [0.1, "#1E3A44"], [0.2, "#1E3A44"], [0.2, "#2C3940"],
              [0.3, "#2C3940"], [0.3, "#3B393B"], [0.4, "#3B393B"], [0.4, "#493836"], [0.5, "#493836"],
              [0.5, "#583832"], [0.6, "#583832"], [0.6, "#66372D"], [0.7, "#66372D"], [0.7, "#753728"],
              [0.8, "#753728"], [0.8, "#833624"], [0.9, "#833624"], [0.9, "#92361F"], [1.0, "#92361F"]]

app = JupyterDash(__name__,
                  suppress_callback_exceptions=True,
                  external_stylesheets=[dbc.themes.LUX,
                                        dbc.icons.FONT_AWESOME]
                  )

server = app.server

df = all_scatter

index_list = df.index.levels[0].tolist()

n_frames = len(index_list)

fig = go.Figure(
    go.Scattermapbox(
        lat=df.xs(1620)[df.xs(1620)['event'] == 'battle']['lat'],
        lon=df.xs(1620)[df.xs(1620)['event'] == 'battle']['lon'],
        mode='markers',
        marker=dict(
            size=4.5,
            color='#701F92',
            opacity=1,
        ),
        customdata=np.stack(
            (
                df.xs(1620)[df.xs(1620)['event'] == 'battle']['battle'],
                df.xs(1620)[df.xs(1620)['event'] == 'battle']['country'],
                df.xs(1620)[df.xs(1620)['event'] == 'battle']['war']
            ), axis=-1
        ),
        hovertemplate='<extra></extra><b>%{customdata[0]}</b>\
        <br><br>%{customdata[2]}<br>%{customdata[1]}',
        name='RELIGIOUS BATTLE'
    )
)

fig.add_scattermapbox(
    lat=df.xs(1620)[df.xs(1620)['event'] == 'trial']['lat'],
    lon=df.xs(1620)[df.xs(1620)['event'] == 'trial']['lon'],
    mode='markers',
    marker=dict(
        size=df.xs(1620)[df.xs(1620)['event'] == 'trial']['size_1'] * 3,
        color=df.xs(1620)[df.xs(1620)['event'] == 'trial']['mortality'],
        opacity=0.9,
        showscale=False,
        colorscale=colorscale
    ),
    hoverinfo='none',
    name='PEOPLE TRIED FOR WITCHCRAFT:<br>SIZE = NUMBER OF TRIED | COLOR = % OF EXECUTED'
)

fig.add_scattermapbox(
    lat=df.xs(1620)[df.xs(1620)['event'] == 'trial']['lat'],
    lon=df.xs(1620)[df.xs(1620)['event'] == 'trial']['lon'],
    mode='markers',
    marker=dict(
        size=3,
        color='#ffffff',
        opacity=1),
    hoverinfo='none',
    name='WITCH TRIALS PLACE'
)

fig.add_scattermapbox(
    lat=df.xs(1620)[df.xs(1620)['event'] == 'trial']['lat'],
    lon=df.xs(1620)[df.xs(1620)['event'] == 'trial']['lon'],
    mode='markers',
    marker=dict(
        size=df.xs(1620)[df.xs(1620)['event'] == 'trial']['size_1'] * 3,
        color=df.xs(1620)[df.xs(1620)['event'] == 'trial']['mortality'],
        opacity=0,
        showscale=True,
        colorscale=colorscale,
        colorbar={'title': {'text': '% OF EXECUTED AMONG THE TRIED',
                            'font': {'family': 'Palatino', 'size': 10, 'color': '#B2B297'}},
                  'tickfont': {'family': 'Palatino', 'size': 10, 'color': '#B2B297'},
                  'x': 0.815,
                  'y': 0.858,
                  'orientation': 'h',
                  'tickformat': ',.0%',
                  'thicknessmode': 'pixels',
                  'title_side': 'top',
                  'thickness': 12,
                  'lenmode': 'pixels',
                  'len': 300,
                  'ticks': 'inside',
                  'ticklen': 15,
                  'tickwidth': 2,
                  'tickcolor': '#1e201e',
                  'outlinecolor': '#1e201e',
                  'outlinewidth': 2,
                  'nticks': 11,
                  'ticklabelstep': 10
                  },
        cmin=0,
        cmax=1
    ),
    customdata=np.stack(
        (
            df.xs(1620)[df.xs(1620)['event'] == 'trial']['decade_hov'],
            df.xs(1620)[df.xs(1620)['event'] == 'trial'].index,
            df.xs(1620)[df.xs(1620)['event'] == 'trial']['country'],
            df.xs(1620)[df.xs(1620)['event'] == 'trial']['tried'],
            df.xs(1620)[df.xs(1620)['event'] == 'trial']['executed'],
            df.xs(1620)[df.xs(1620)['event'] == 'trial']['mortality']
        ), axis=-1
    ),
    hovertemplate='<extra></extra><b>%{customdata[0]}, %{customdata[1]}, %{customdata[2]}:</b>\
    <br><br><b>%{customdata[3]:,.0f}</b> people were tried for witchcraft\
    <br><b>%{customdata[4]:,.0f}</b> of them were killed (<b>%{customdata[5]:,.0%}</b>)',
    name='NUMBER OF PEOPLE TRIED'
)

frames = []

for i in range(n_frames):
    decade = index_list[i]
    frames.append(
        go.Frame(
            data=[
                go.Scattermapbox(
                    lat=df.xs(decade)[df.xs(decade)['event'] == 'battle']['lat'],
                    lon=df.xs(decade)[df.xs(decade)['event'] == 'battle']['lon'],
                    customdata=np.stack((df.xs(decade)[df.xs(decade)['event'] == 'battle']['battle'],
                                         df.xs(decade)[df.xs(decade)['event'] == 'battle']['country'],
                                         df.xs(decade)[df.xs(decade)['event'] == 'battle']['war']
                                         ), axis=-1
                                        ),
                ),
                go.Scattermapbox(
                    lat=df.xs(decade)[df.xs(decade)['event'] == 'trial']['lat'],
                    lon=df.xs(decade)[df.xs(decade)['event'] == 'trial']['lon'],
                    marker=dict(size=df.xs(decade)[df.xs(decade)['event'] == 'trial']['size_1'] * 3,
                                color=df.xs(decade)[df.xs(decade)['event'] == 'trial']['mortality']
                                )
                ),
                go.Scattermapbox(
                    lat=df.xs(decade)[df.xs(decade)['event'] == 'trial']['lat'],
                    lon=df.xs(decade)[df.xs(decade)['event'] == 'trial']['lon']
                ),
                go.Scattermapbox(
                    lat=df.xs(decade)[df.xs(decade)['event'] == 'trial']['lat'],
                    lon=df.xs(decade)[df.xs(decade)['event'] == 'trial']['lon'],
                    marker=dict(size=df.xs(decade)[df.xs(decade)['event'] == 'trial']['size_1'] * 3,
                                color=df.xs(decade)[df.xs(decade)['event'] == 'trial']['mortality']),
                    customdata=np.stack((df.xs(decade)[df.xs(decade)['event'] == 'trial']['decade_hov'],
                                         df.xs(decade)[df.xs(decade)['event'] == 'trial'].index,
                                         df.xs(decade)[df.xs(decade)['event'] == 'trial']['country'],
                                         df.xs(decade)[df.xs(decade)['event'] == 'trial']['tried'],
                                         df.xs(decade)[df.xs(decade)['event'] == 'trial']['executed'],
                                         df.xs(decade)[df.xs(decade)['event'] == 'trial']['mortality']
                                         ), axis=-1
                                        )
                )
            ],
            traces=[0, 1, 2, 3],
            name=f"fr{i}",
            layout=dict(
                mapbox=go.layout.Mapbox(
                    style=mono_dark1)
            )
        )
    )

fig.update(frames=frames)

steps = []
for i in range(n_frames):
    decade = index_list[i]
    step = dict(
        label=decade,
        method='animate',
        args=[
            [f'fr{i}'],
            dict(mode='immediate',
                 frame=dict(duration=1000,
                            redraw=True),
                 transition=dict(duration=500)
                 )
        ]
    )
    steps.append(step)

sliders = [
    dict(
        transition=dict(duration=0),
        x=0.055,
        y=0.17,
        len=0.89,
        currentvalue=dict(
            visible=True,
            font={'color': '#B2B297', 'family': 'Palatino', 'size': 18},
            offset=10,
            suffix='s  ', xanchor='right'
        ),
        steps=steps,
        active=32,
        bgcolor='#B2B297',
        bordercolor='#1e201e',
        borderwidth=4,
        activebgcolor='#1e201e',
        font=dict(color='#040609', family='Palatino', size=1),
        ticklen=5,
        tickcolor='#B2B297'
    )
]

play_buttons = [{
    'type': 'buttons',
    'showactive': False,
    'bgcolor': '#040609',
    'bordercolor': '#B2B297',
    'font': {'color': '#B2B297', 'family': 'Palatino', 'size': 12},
    'direction': 'left',
    "pad": {"r": 10, "t": 87},
    'x': 0.155,
    'y': 0.28,
    'buttons':
        [
            {
                'label': '▶',
                'method': 'animate',
                'args':
                    [
                        None,
                        {
                            'frame': {'duration': 1000, 'redraw': True},
                            'transition': {'duration': 500},
                            'fromcurrent': True,
                            'mode': 'immediate',
                        }
                    ]
            },
            {
                'label': '◼',
                'method': 'animate',
                'args':
                    [
                        [None],
                        {
                            'frame': {'duration': 0, 'redraw': False},
                            'transition': {'duration': 0},
                            'mode': 'immediate',
                        }
                    ]
            }
        ]
}]

fig.add_shape(
    type='rect',
    xref='x', yref='y',
    x0=1300, y0=5,
    x1=1300, y1=5,
    line_color='rgba(0,0,0,0)',
    fillcolor='rgba(0,0,0,0)',
)

t = 1300
for n in range(12):
    fig.add_annotation(
        x=t,
        y=0.2,
        text=t,
        showarrow=False,
        font=dict(color='#B2B297', family='Palatino', size=12),
        align='center'
    )
    t += 50

fig['data'][3]['showlegend'] = False

fig.update_layout(
    sliders=sliders,
    updatemenus=play_buttons,
    height=650,
    width=920,
    margin={'r': 0, 'l': 0, 't': 0, 'b': 0},
    plot_bgcolor='#040609',
    paper_bgcolor='#040609',
    yaxis={'visible': False, 'range': [0, 10]},
    xaxis={'visible': False, 'range': [1260, 1890]},
    mapbox=dict(
        accesstoken=mapbox_token,
        style=mono_dark1,
        zoom=4.2,
        pitch=45,
        center={'lat': 50, 'lon': 5},
        bounds={'west': -50, 'east': 40, 'south': 35, 'north': 65}
    ),
    legend={'title': 'TURN ANY LEVEL OFF/ON BY TAPPING IT:',
            'title_font': {'family': 'Book Antiqua', 'size': 10, 'color': '#B2B297'},
            'bgcolor': 'rgba(0,0,0,0)',
            'xanchor': 'left',
            'yanchor': 'middle',
            'x': 0.02,
            'y': 0.897,
            'font': {'family': 'Palatino', 'size': 10, 'color': '#B2B297'},
            'itemsizing': 'constant',
            'traceorder': 'reversed'},
    hoverlabel={'font': {'family': 'Palatino', 'size': 12, 'color': '#ffffff'}}
)

index_list = trials_net.decade.sort_values().unique().tolist()[:-1]

n_frames = len(index_list)

df = all_scatter_total

fig0 = go.Figure(
    go.Scattermapbox(
        lat=df[df['event'] == 'battle']['lat'],
        lon=df[df['event'] == 'battle']['lon'],
        mode='markers',
        marker=dict(
            size=4,
            color='#701F92',
            opacity=1,
        ),
        customdata=np.stack((df[df['event'] == 'battle']['battle'],
                             df[df['event'] == 'battle']['country']), axis=-1),
        hovertemplate='<extra></extra><b>%{customdata[0]}</b><br><br>%{customdata[1]}',
        name='RELIGIOUS BATTLE'
    )
)

fig0.add_scattermapbox(
    lat=df[df['event'] == 'trial']['lat'],
    lon=df[df['event'] == 'trial']['lon'],
    mode='markers',
    marker=dict(
        size=df[df['event'] == 'trial']['size'] * 2,
        color=df[df['event'] == 'trial']['mortality'],
        opacity=0.9,
        showscale=False,
        colorscale=colorscale
    ),
    hoverinfo='none',
    name='PEOPLE TRIED FOR WITCHCRAFT:<br>SIZE = NUMBER OF TRIED | COLOR = % OF EXECUTED'
)

fig0.add_scattermapbox(
    lat=df[df['event'] == 'trial']['lat'],
    lon=df[df['event'] == 'trial']['lon'],
    mode='markers',
    marker=dict(
        size=3,
        color='#ffffff',
        opacity=1),
    hoverinfo='none',
    name='WITCH TRIAL PLACE'
)

fig0.add_scattermapbox(
    lat=df[df['event'] == 'trial']['lat'],
    lon=df[df['event'] == 'trial']['lon'],
    mode='markers',
    marker=dict(
        size=df[df['event'] == 'trial']['size'] * 2,
        color=df[df['event'] == 'trial']['mortality'],
        opacity=0,
        showscale=True,
        colorscale=colorscale,
        colorbar={'title': {'text': '% OF EXECUTED AMONG THE TRIED',
                            'font': {'family': 'Book Antiqua', 'size': 10, 'color': '#B2B297'}},
                  'tickfont': {'family': 'Book Antiqua', 'size': 10, 'color': '#B2B297'},
                  'x': 0.815,
                  'y': 0.858,
                  'orientation': 'h',
                  'tickformat': ',.0%',
                  'thicknessmode': 'pixels',
                  'title_side': 'top',
                  'thickness': 12,
                  'lenmode': 'pixels',
                  'len': 300,
                  'ticks': 'inside',
                  'ticklen': 15,
                  'tickwidth': 2,
                  'tickcolor': '#1e201e',
                  'outlinecolor': '#1e201e',
                  'outlinewidth': 2,
                  'nticks': 11,
                  'ticklabelstep': 10
                  },
        cmin=0,
        cmax=1
    ),
    customdata=np.stack((df[df['event'] == 'trial']['min_decade'],
                         df[df['event'] == 'trial']['max_decade'],
                         df[df['event'] == 'trial'].index,
                         df[df['event'] == 'trial']['country'],
                         df[df['event'] == 'trial']['tried'],
                         df[df['event'] == 'trial']['executed'],
                         df[df['event'] == 'trial']['mortality']), axis=-1),
    hovertemplate='<extra></extra><b>%{customdata[2]}, %{customdata[3]}:</b>\
    <br><br>First trial: %{customdata[0]} | Last trial: %{customdata[1]}\
    <br><br><b>%{customdata[4]:,.0f}</b> people were tried for witchcraft\
    <br><b>%{customdata[5]:,.0f}</b> of them were killed (<b>%{customdata[6]:,.0%}</b>)',
    name='NUMBER OF PEOPLE TRIED'
)

fig0['data'][3]['showlegend'] = False

fig0.update_layout(
    height=650,
    width=920,
    margin={'r': 0, 'l': 0, 't': 0, 'b': 0},
    plot_bgcolor='#040609',
    paper_bgcolor='#040609',
    yaxis={'visible': False, 'range': [0, 10]},
    xaxis={'visible': False, 'range': [1290, 1860]},
    mapbox=dict(
        accesstoken=mapbox_token,
        style=mono_dark1,
        zoom=4.2,
        pitch=45,
        center={'lat': 50, 'lon': 5},
        bounds={'west': -50, 'east': 40, 'south': 35, 'north': 65}
    ),
    legend={'title': 'TURN ANY LEVEL OFF/ON BY TAPPING IT:',
            'title_font': {'family': 'Book Antiqua', 'size': 10, 'color': '#B2B297'},
            'bgcolor': 'rgba(0,0,0,0)',
            'xanchor': 'left',
            'yanchor': 'middle',
            'x': 0.02,
            'y': 0.897,
            'font': {'family': 'Book Antiqua', 'size': 10, 'color': '#B2B297'},
            'itemsizing': 'constant',
            'traceorder': 'reversed'},
    hoverlabel={'font': {'family': 'Book Antiqua', 'size': 12, 'color': '#ffffff'}}
)

fig1 = go.Figure(
    go.Scatter(
        x=trials_net['decade'],
        y=trials_net['country'],
        mode='markers',
        marker={'size': trials_net['size_1'] * 1.7,
                'color': trials_net['mortality'],
                'line_color': '#B2B297',
                'line_width': 0,
                'opacity': 0.8,
                'colorscale': colorscale,
                'showscale': True,
                'colorbar': {'title': {'text': '% OF EXECUTED AMONG THE TRIED',
                                       'font': {'family': 'Palatino',
                                                'size': 10,
                                                'color': '#B2B297'}},
                             'tickfont': {'family': 'Palatino',
                                          'size': 10,
                                          'color': '#B2B297'},
                             'x': 0.83,
                             'y': 0.93,
                             'orientation': 'h',
                             'tickformat': ',.0%',
                             'thicknessmode': 'pixels',
                             'title_side': 'top',
                             'thickness': 12,
                             'lenmode': 'pixels',
                             'len': 300,
                             'ticks': 'inside',
                             'ticklen': 15,
                             'tickwidth': 2,
                             'tickcolor': '#040609',
                             'outlinecolor': '#040609',
                             'outlinewidth': 2,
                             'nticks': 11,
                             'ticklabelstep': 10
                             },
                'cmin': 0,
                'cmax': 1
                },
        hoverinfo='none',
        name='Number of People Tried'
    )
)

fig1.add_trace(
    go.Scatter(
        x=trials_net[
            (trials_net['decade'] == 1900) & (~trials_net['country'].isin(['line_1',
                                                                           'line_2',
                                                                           'line_3',
                                                                           'line_4',
                                                                           'line_5',
                                                                           'line_6',
                                                                           'Decade'])
                                              )]['decade'],
        y=trials_net[
            (trials_net['decade'] == 1900) & (~trials_net['country'].isin(['line_1',
                                                                           'line_2',
                                                                           'line_3',
                                                                           'line_4',
                                                                           'line_5',
                                                                           'line_6',
                                                                           'Decade'])
                                              )]['country'],
        mode='markers+text',
        marker={'size': 0.1,
                'color': '#040609',
                'opacity': 0},
        text=trials_net[
            (trials_net['decade'] == 1900) & (~trials_net['country'].isin(['line_1',
                                                                           'line_2',
                                                                           'line_3',
                                                                           'line_4',
                                                                           'line_5',
                                                                           'line_6',
                                                                           'Decade'])
                                              )]['text_country'],
        textposition='middle left',
        textfont={'size': 12,
                  'family': 'Palatino',
                  'color': '#B2B297'},
        hoverinfo='none',
        name='Decades with Trials Text'
    )
)

fig1.add_trace(
    go.Scatter(
        x=trials_net[
            (trials_net['decade'] == 1900) & (~trials_net['country'].isin(['line_1',
                                                                           'line_2',
                                                                           'line_3',
                                                                           'line_4',
                                                                           'line_5',
                                                                           'line_6',
                                                                           'Decade'])
                                              )]['decade'],
        y=trials_net[
            (trials_net['decade'] == 1900) & (~trials_net['country'].isin(['line_1',
                                                                           'line_2',
                                                                           'line_3',
                                                                           'line_4',
                                                                           'line_5',
                                                                           'line_6',
                                                                           'Decade'])
                                              )]['country'],
        mode='markers',
        marker={'size': trials_net[
                            (trials_net['decade'] == 1900) & (~trials_net['country'].isin(['line_1',
                                                                                           'line_2',
                                                                                           'line_3',
                                                                                           'line_4',
                                                                                           'line_5',
                                                                                           'line_6',
                                                                                           'Decade'])
                                                              )]['size_1'] * 1.7,
                'color': trials_net[
                    (trials_net['decade'] == 1900) & (~trials_net['country'].isin(['line_1',
                                                                                   'line_2',
                                                                                   'line_3',
                                                                                   'line_4',
                                                                                   'line_5',
                                                                                   'line_6',
                                                                                   'Decade'])
                                                      )]['mortality'],
                'opacity': 0.2,
                'line_color': '#ffffff',
                'line_width': 0.3,
                'colorscale': colorscale},
        hoverinfo='none',
        name='Trace to highlight Country Totals'
    )
)

fig1.add_trace(
    go.Scatter(
        x=trials_net[trials_net['decade'] == 1420]['decade'],
        y=trials_net[trials_net['decade'] == 1420]['country'],
        mode='lines',
        line={'color': '#777777',
              'width': 0.3},
        hoverinfo='none',
        name='Decade Line'
    )
)

fig1.add_trace(
    go.Scatter(
        x=trials_net['decade'],
        y=trials_net['country'],
        mode='markers',
        marker={'size': trials_net['size_2'],
                'color': '#ffffff',
                'line_color': '#ffffff',
                'line_width': 0,
                'opacity': 0.9},
        hoverinfo='none',
        name='Decades with Trials'
    )
)

fig1.add_trace(
    go.Scatter(
        x=trials_net[trials_net['decade'] == 1420]['decade'],
        y=trials_net[trials_net['decade'] == 1420]['country'],
        mode='markers',
        marker={'size': trials_net[trials_net['decade'] == 1420]['size_1'] * 1.7,
                'color': trials_net[trials_net['decade'] == 1420]['mortality'],
                'opacity': 0.9,
                'line_color': '#777777',
                'line_width': 0.3,
                'colorscale': colorscale},
        hoverinfo='none',
        name='Number of People Tried During the Chosen Decade'
    )
)

fig1.add_trace(
    go.Scatter(
        x=trials_net[trials_net['decade'] == 1420]['decade'],
        y=trials_net[trials_net['decade'] == 1420]['country'],
        mode='markers',
        marker={'size': trials_net[trials_net['decade'] == 1420]['size_2'] * 1.5,
                'color': '#ffffff',
                'line_color': '#ffffff',
                'line_width': 0,
                'opacity': 1},
        hoverinfo='none',
        name='Decade Chosen'
    )
)

fig1.add_trace(
    go.Scatter(
        x=trials_net[
            (trials_net['decade'] == 1420) & (trials_net['country'] == 'Europe')]['decade'],
        y=trials_net[
            (trials_net['decade'] == 1420) & (trials_net['country'] == 'Europe')]['country'],
        mode='markers+text',
        marker={'size': 0.1,
                'color': '#040609',
                'line_width': 0,
                'opacity': 0.9},
        text=trials_net[
            (trials_net['decade'] == 1420) & (trials_net['country'] == 'Europe')]['text_decade'],
        textposition='top center',
        textfont={'size': 12,
                  'family': 'Palatino',
                  'color': '#B2B297'},
        hoverinfo='none',
        name='Decade Chosen Text'
    )
)

fig1.add_trace(
    go.Scatter(
        x=trials_net[
            (trials_net['country'] == 'Decade') & (trials_net['decade'] == 1420)]['decade'],
        y=trials_net[
            (trials_net['country'] == 'Decade') & (trials_net['decade'] == 1420)]['country'],
        mode='markers+text',
        marker={'size': 0.1,
                'color': '#040609',
                'line_width': 0,
                'opacity': 0},
        text=trials_net[
            (trials_net['country'] == 'Decade') & (trials_net['decade'] == 1420)]['decade_t'],
        textposition='middle center',
        textfont={'size': 14,
                  'family': 'Palatino',
                  'color': '#e4e3bf'},
        hoverinfo='none',
        name='Moving Decade'
    )
)

fig1.add_trace(
    go.Scatter(
        x=trials_net['decade_hov'],
        y=trials_net['country_hov'],
        mode='markers',
        marker={'size': trials_net['size_1'] * 1.7,
                'color': trials_net['mortal_hov'],
                'colorscale': colorscale,
                'opacity': 0},
        customdata=np.stack((trials_net['decade_name_hov'],
                             trials_net['country_hov'],
                             trials_net['tried_hov'],
                             trials_net['executed_hov'],
                             trials_net['mortal_hov']
                             ), axis=-1
                            ),
        hovertemplate='<b>%{customdata[0]}, %{customdata[1]}:</b><br><br>\
        <b>%{customdata[2]:,.0f}</b> people were tried for witchcraft<br>\
        <b>%{customdata[3]:,.0f}</b> of them were killed (<b>%{customdata[4]:,.0%}</b>)',
        name=''
    )
)

frames = []

for i in range(n_frames):
    decade = index_list[i]
    frames.append(
        go.Frame(
            data=[
                go.Scatter(),
                go.Scatter(),
                go.Scatter(),
                go.Scatter(x=trials_net[trials_net['decade'] == decade]['decade'],
                           y=trials_net[trials_net['decade'] == decade]['country']
                           ),
                go.Scatter(),
                go.Scatter(
                    x=trials_net[trials_net['decade'] == decade]['decade'],
                    y=trials_net[trials_net['decade'] == decade]['country'],
                    marker={'size': trials_net[trials_net['decade'] == decade]['size_1'] * 1.7,
                            'color': trials_net[trials_net['decade'] == decade]['mortality']}
                ),
                go.Scatter(
                    x=trials_net[trials_net['decade'] == decade]['decade'],
                    y=trials_net[trials_net['decade'] == decade]['country'],
                    marker={'size': trials_net[trials_net['decade'] == decade]['size_2'] * 1.5}
                ),
                go.Scatter(
                    x=trials_net[
                        (trials_net['decade'] == decade) & (trials_net['country'] == 'Europe')]['decade'],
                    y=trials_net[
                        (trials_net['decade'] == decade) & (trials_net['country'] == 'Europe')]['country'],
                    text=trials_net[
                        (trials_net['decade'] == decade) & (trials_net['country'] == 'Europe')]['text_decade']
                ),
                go.Scatter(
                    x=trials_net[
                        (trials_net['country'] == 'Decade') & (trials_net['decade'] == decade)]['decade'],
                    y=trials_net[
                        (trials_net['country'] == 'Decade') & (trials_net['decade'] == decade)]['country'],
                    text=trials_net[
                        (trials_net['country'] == 'Decade') & (trials_net['decade'] == decade)]['decade_t']
                ),
                go.Scatter()
            ],
            traces=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            name=f'fr{i}'
        )
    )

fig1.update(frames=frames)

steps = []
for i in range(n_frames):
    decade = index_list[i]
    step = dict(
        label=decade,
        method='animate',
        args=[
            [f'fr{i}'],
            dict(mode='immediate',
                 frame=dict(duration=1000,
                            redraw=False
                            ),
                 transition=dict(duration=500)
                 )
        ]
    )
    steps.append(step)

sliders = [
    dict(
        transition=dict(duration=0, easing='exp-in-out'),
        x=0.094,
        y=0.08,
        len=0.839,
        currentvalue=dict(visible=False),
        steps=steps,
        active=12,
        bgcolor='#B2B297',
        bordercolor='#040609',
        borderwidth=4,
        activebgcolor='#040609',
        font=dict(color='#040609', family='Palatino', size=1),
        ticklen=5,
        tickcolor='#B2B297'
    )
]

play_buttons = [{
    'type': 'buttons',
    'showactive': False,
    'bgcolor': '#040609',
    'bordercolor': '#B2B297',
    'font': {'color': '#B2B297', 'family': 'Palatino', 'size': 12},
    'direction': 'left',
    'pad': {'r': 10, 't': 87},
    'x': 0.085,
    'y': 0.17,
    'buttons':
        [
            {
                'label': '▶',
                'method': 'animate',
                'args':
                    [
                        None,
                        {
                            'frame': {'duration': 1000, 'redraw': False},
                            'transition': {'duration': 500},
                            'fromcurrent': True,
                            'mode': 'immediate',
                        }
                    ]
            },
            {
                'label': '◼',
                'method': 'animate',
                'args':
                    [
                        [None],
                        {
                            'frame': {'duration': 0, 'redraw': False},
                            'transition': {'duration': 0},
                            'mode': 'immediate',
                        }
                    ]
            }
        ]
}]

fig1.add_annotation(
    xref='paper',
    yref='paper',
    x=0.001,
    y=1.02,
    text='CIRCLES ARE SIZED BY<br>THE NUMBER OF PEOPLE TRIED',
    showarrow=False,
    font=dict(color='#B2B297', family='Palatino', size=10),
    align='left'
)

fig1.update_layout(
    sliders=sliders,
    updatemenus=play_buttons,
    margin={'t': 50, 'b': 0, 'r': 0, 'l': 0},
    width=920,
    height=750,
    plot_bgcolor='#040609',
    paper_bgcolor='#040609',
    showlegend=False,
    xaxis={'range': [1230, 1901],
           'tickvals': [1300, 1350, 1400, 1450, 1500, 1550, 1600, 1650, 1700, 1750, 1800, 1850],
           'showgrid': False,
           'tickfont': {'family': 'Palatino',
                        'size': 14,
                        'color': '#B2B297'}},
    yaxis={'range': [-1, 30],
           'tickvals': ['Sweden', 'Denmark', 'Norway', 'Estonia', 'Finland', 'Hungary',
                        'Luxembourg', 'Poland', 'Spain', 'Belgium', 'Czechia',
                        'Switzerland', 'Netherlands', 'Ireland', 'Italy', 'Austria',
                        'UK', 'France', 'Germany', 'Europe'],
           'title': None,
           'tickfont': {'family': 'Palatino',
                        'size': 14,
                        'color': '#B2B297'},
           'zeroline': False,
           'showgrid': False,
           'anchor': 'free',
           'position': 0,
           'side': 'right'},
    hoverlabel={'font': {'family': 'Palatino', 'size': 12, 'color': '#ffffff'}}
)

fig2 = px.treemap(
    treemap,
    path=[px.Constant('Europe'), 'country', 'region_map', 'city'],
    values='tried',
    color='mortality',
    color_continuous_scale=colorscale,
    custom_data=np.stack(
        ('country', 'city', 'tried', 'executed', 'mortality', 'perc_of_total'), axis=-1)
)

fig2.add_annotation(
    x=0.005,
    y=1.125,
    text='SECTORS ARE SIZED BY<br>THE NUMBER OF PEOPLE TRIED',
    showarrow=False,
    font=dict(color='#B2B297', family='Palatino', size=10),
    align='left')

fig2.update_layout(
    height=600,
    width=920,
    margin=dict(l=0, r=0, t=0, b=0),
    font={'family': 'Palatino', 'size': 10, 'color': '#e4e3bf'},
    plot_bgcolor='#040609',
    paper_bgcolor='#040609',
    coloraxis={'showscale': True},
    coloraxis_colorbar={'title': {'text': '% OF EXECUTED AMONG THE TRIED',
                                  'font': {'family': 'Palatino',
                                           'size': 10,
                                           'color': '#B2B297'}},
                        'tickfont': {'family': 'Palatino',
                                     'size': 10,
                                     'color': '#B2B297'},
                        'x': 0.83,
                        'y': 0.999,
                        'orientation': 'h',
                        'tickformat': ',.0%',
                        'thicknessmode': 'pixels',
                        'title_side': 'top',
                        'thickness': 12,
                        'lenmode': 'pixels',
                        'len': 300,
                        'ticks': 'inside',
                        'ticklen': 15,
                        'tickwidth': 2,
                        'tickcolor': '#040609',
                        'outlinecolor': '#040609',
                        'outlinewidth': 2,
                        'nticks': 11,
                        'ticklabelstep': 10
                        },
    hoverlabel={'font': {'family': 'Palatino',
                         'size': 12,
                         'color': '#ffffff'}}
)

fig2.data[0].customdata[-1][0] = 'Total'
fig2.data[0].customdata[-1][1] = 'Europe'
fig2.data[0].customdata[-1][3] = treemap['executed'].sum()
fig2.data[0].customdata[-1][5] = treemap['executed'].sum() / treemap['executed'].sum()
fig2.data[0]['marker_line_width'] = 0.3

for i in range(-20, -1):
    fig2.data[0].customdata[i][0] = 'Total'
    fig2.data[0].customdata[i][1] = fig2.data[0]['labels'][i]
    fig2.data[0].customdata[i][3] = treemap[
        treemap['country'] == fig2.data[0]['labels'][i]]['executed'].sum()
    fig2.data[0].customdata[i][5] = treemap[
                                        treemap['country'] == fig2.data[0]['labels'][i]]['executed'].sum() / treemap[
                                        'executed'].sum()

for i in range(-194, -20):
    fig2.data[0].customdata[i][1] = fig2.data[0]['labels'][i]
    fig2.data[0].customdata[i][3] = treemap[
        (treemap['region_map'] == fig2.data[0]['labels'][i]) &
        (treemap['country'] == fig2.data[0]['parents'][i].split('/')[1])]['executed'].sum()
    fig2.data[0].customdata[i][5] = treemap[
                                        (treemap['region_map'] == fig2.data[0]['labels'][i]) &
                                        (treemap['country'] == fig2.data[0]['parents'][i].split('/')[1])
                                        ]['executed'].sum() / treemap['executed'].sum()

for i in range(-1198, -194):
    fig2.data[0].customdata[i][0] = fig2.data[0]['parents'][i].split('/')[2]

fig2.update_traces(
    hovertemplate='<b>%{customdata[1]}, %{customdata[0]}</b><br><br>\
    <b>%{customdata[2]:,.0f}</b> people were tried<br><br>\
    <b>%{customdata[3]:,.0f}</b> people were killed, which is:<br><br>\
    <b>%{customdata[4]:,.1%}</b> of all tried in %{customdata[1]} <br>\
    <b>%{customdata[5]:,.1%}</b> of all killed in Europe<br>',
    marker_line_width=0.5
)

app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(width=3),
            dbc.Col(
                [
                    html.H6(
                        '550 years', style={'color': '#e4e3bf',
                                            'font-family': 'Palatino',
                                            'font-size': 85,
                                            'margin-top': 85,
                                            'margin-bottom': 0,
                                            'text-align': 'center'}
                    ),
                    html.Hr(
                        style={'color': '#92361f',
                               'margin-top': 0,
                               'margin-right': 30,
                               'margin-left': 30}
                    ),
                    html.H6(
                        'Of Witch Hunt in Europe', style={'color': '#92361f',
                                                          'font-family': 'Palatino',
                                                          'font-size': 27,
                                                          'margin-top': 0,
                                                          'margin-bottom': 85,
                                                          'text-align': 'center'}
                    )
                ], width=6),
            dbc.Col(width=3)
        ]),
        dbc.Row([
            dbc.Col(
                [
                    html.H6(
                        'Tens of thousands were accused and killed', className="display-3",
                        style={'color': '#e4e3bf',
                               'font-family': 'Palatino',
                               'font-size': 17,
                               'margin-left': 70,
                               'margin-right': 25}
                    ),
                    html.Hr(
                        style={'color': '#e4e3bf',
                               'margin-top': 10,
                               'margin-bottom': 10,
                               'margin-left': 70,
                               'margin-right': 25}
                    )
                ], width=8),
            dbc.Col([
                html.H6(
                    'The data', className="display-3",
                    style={'color': '#e4e3bf',
                           'font-family': 'Palatino',
                           'font-size': 17,
                           'margin-left': 15,
                           'margin-right': 70}
                ),
                html.Hr(
                    style={'color': '#e4e3bf',
                           'margin-top': 10,
                           'margin-bottom': 10,
                           'margin-left': 15,
                           'margin-right': 70}
                )
            ], width=4)
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    html.P("According to historians' consensus, up to 110,000 Europeans were "
                           "accused of witchcraft between "
                           "1400 and 1750; about half of them were consequently killed. The "
                           "overwhelming majority of all "
                           "trials and executions were carried out between 1550 and 1700.",
                           style={'color': '#e4e3bf',
                                  'font-family': 'Palatino',
                                  'font-size': 14,
                                  'text-align': 'left',
                                  'margin-left': 70,
                                  'margin-right': 0}
                           )
                ], style={'backgroundColor': '#040609'})
            ], width=4),
            dbc.Col([
                dbc.Card([
                    html.P('The scholars are still arguing about the reason for that surge in '
                           'brutality. Among the possible '
                           'triggers are crop failures and famine, a lack of governance, and '
                           'the shaken position of '
                           'Catholicism. Either way, witches became scapegoats who were supposed '
                           'to pay for all the hardships.',
                           style={'color': '#e4e3bf',
                                  'font-family': 'Palatino',
                                  'font-size': 14,
                                  'text-align': 'left',
                                  'margin-left': 15,
                                  'margin-right': 25}
                           )
                ], style={'backgroundColor': '#040609'})
            ], width=4),
            dbc.Col([
                dbc.Card([
                    html.P("This dashboard illustrates the data on 43,000 people who were tried for "
                           "witchcraft between 1300 "
                           "and 1850 in 21 European countries, aggregated by Peter T. Leeson and "
                           "Jacob W. Russ from George "
                           "Mason University for their economic research.",
                           style={'color': '#e4e3bf',
                                  'font-family': 'Palatino',
                                  'font-size': 14,
                                  'text-align': 'left',
                                  'margin-left': 15,
                                  'margin-right': 70}
                           )
                ], style={'backgroundColor': '#040609'})
            ], width=4)
        ], style={'margin-bottom': 0}),
        dbc.Row([
            dbc.Col([
                html.Div([
                    dbc.Row([
                        dbc.Col(width=3),
                        dbc.Col([
                            html.H6('Charts to Explore:', style={'color': '#e4e3bf',
                                                                 'font-family': 'Palatino',
                                                                 'font-size': 21,
                                                                 'text-align': 'center'}
                                    )
                        ], width=6),
                        dbc.Col(width=3)
                    ], style={'margin-bottom': 10}),
                    dbc.Row([
                        dbc.Col(
                            html.Div(
                                [
                                    html.H6("Interactive Map", className='display-3',
                                            style={'color': "#0f3a49",
                                                   'font-family': 'Palatino',
                                                   'font-size': 17,
                                                   'font-weight': 'bold'}),
                                    html.Hr(className='my-2'),
                                    html.P(
                                        'Navigate the map of the witch trials of 1300–1850.',
                                        style={'color': '#e4e3bf',
                                               'font-family': 'Palatino',
                                               'font-size': 13}
                                    ),
                                    dbc.Button(
                                        [
                                            'Explore ',
                                            html.I(className='fas fa-angle-double-down',
                                                   style={'display': 'inline-block'}
                                                   )
                                        ],
                                        href='#explore1',
                                        external_link=True,
                                        style={'background-color': '#0f3a49',
                                               'font-family': 'Palatino',
                                               'color': '#e4e3bf',
                                               'border': 'rounded-3'},
                                        outline=True
                                    )
                                ],
                                className='h-100 p-3 text-white rounded-3'
                            ), md=4
                        ),
                        dbc.Col(
                            html.Div(
                                [
                                    html.H6('Timeline', className='display-3',
                                            style={'color': "#0f3a49",
                                                   'font-family': 'Palatino',
                                                   'font-size': 17,
                                                   'font-weight': 'bold'}
                                            ),
                                    html.Hr(className='my-2'),
                                    html.P(
                                        "Navigate the witch trials' timeline for 21 countries.",
                                        style={'color': '#e4e3bf',
                                               'font-family': 'Palatino',
                                               'font-size': 13}
                                    ),
                                    dbc.Button(
                                        [
                                            'Explore ',
                                            html.I(className='fas fa-angle-double-down',
                                                   style={'display': 'inline-block'}
                                                   )
                                        ],
                                        href='#explore2',
                                        external_link=True,
                                        style={'background-color': '#0f3a49',
                                               'font-family': 'Palatino',
                                               'color': '#e4e3bf',
                                               'border': 'rounded-3'},
                                        outline=True)
                                ],
                                className='h-100 p-3 text-white rounded-3'
                            ), md=4
                        ),
                        dbc.Col(
                            html.Div(
                                [
                                    html.H6('Regions&Cities', className='display-3',
                                            style={'color': "#0f3a49",
                                                   'font-family': 'Palatino',
                                                   'font-size': 17,
                                                   'font-weight': 'bold'}
                                            ),
                                    html.Hr(className='my-2'),
                                    html.P(
                                        'Find the place with the most and the least deadly trials.',
                                        style={'color': '#e4e3bf',
                                               'font-family': 'Palatino',
                                               'font-size': 13}
                                    ),
                                    dbc.Button(['Explore ',
                                                html.I(className='fas fa-angle-double-down',
                                                       style={'display': 'inline-block'})
                                                ],
                                               href='#explore3',
                                               external_link=True,
                                               style={'background-color': '#0f3a49',
                                                      'font-family': 'Palatino',
                                                      'color': '#e4e3bf',
                                                      'border': 'rounded-3'},
                                               outline=True
                                               )
                                ], className='h-100 p-3 text-white rounded-3'
                            ), md=4
                        )
                    ], style={'margin-bottom': 20}),
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                dbc.Button(
                                    "What's on the photo?",
                                    id='fade-button',
                                    className='mb-3',
                                    n_clicks=0,
                                    style={'background-color': '#e4e3bf',
                                           'font-family': 'Palatino',
                                           'color': '#263724',
                                           'border': 'rounded-3'}
                                )
                            ], style={'text-align': 'left',
                                      'margin-left': 20})
                        ], width=4),
                        dbc.Col([
                            html.Div([
                                dbc.Fade(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                html.P(
                                                    [
                                                        html.A(
                                                            'Vaud',
                                                            href='https://en.wikipedia.org/wiki/Vaud',
                                                            target='_blank',
                                                            style={'color': '#ba9c30'}
                                                        ),
                                                        ' was the most brutal place for witchcraft '
                                                        'suspects: 3,378 of them were killed in this '
                                                        'Swiss canton, '
                                                        'which makes up 21% of '
                                                        'all European executions.'
                                                    ], className='card-text'
                                                ),
                                                html.P(
                                                    [
                                                        'Photo by ',
                                                        html.A(
                                                            'Joanna Wesniuk',
                                                            href='https://unsplash.com/@the_minimalist',
                                                            target='_blank',
                                                            style={'color': '#ba9c30'}
                                                        ),
                                                        ' on ',
                                                        html.A('Unsplash',
                                                               href='https://unsplash.com/',
                                                               target='_blank',
                                                               style={'color': '#ba9c30'}
                                                               ),
                                                        ' (colors are edited).'
                                                    ], className='card-text'
                                                )
                                            ], style={'background-color': '#040609',
                                                      'font-family': 'Palatino',
                                                      'font-size': 13,
                                                      'color': '#e4e3bf'}
                                        )
                                    ),
                                    id='fade',
                                    is_in=False,
                                    appear=False,
                                    style={'margin-right': 10}
                                )
                            ])
                        ], width=8)
                    ])
                ], className='h-100 p-5 text-white border rounded-3',
                    style={'margin-left': 70,
                           'margin-right': 70,
                           'background-image': 'url("/assets/backgr.png")'}
                )
            ], width=12)
        ], style={'margin-top': 30,
                  'margin-bottom': 90}),
        html.A(id='explore1'),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(
                        [
                            html.H6('TRIALS MAP',
                                    style={'color': '#e4e3bf',
                                           'font-family': 'Palatino',
                                           'font-size': 17}
                                    ),
                            html.Hr(className='my-2',
                                    style={'margin-bottom': 0,
                                           'color': '#e4e3bf'}
                                    )
                        ]
                    )
                ], style={'backgroundColor': '#040609',
                          'margin-right': 50,
                          'margin-left': 50}
                )
            ])
        ], style={'margin-top': 40,
                  'margin-bottom': 0}
        ),
        dbc.Row([
            dbc.Col([
                dbc.RadioItems(
                    id='radios',
                    className='btn-group',
                    inputClassName='btn-check',
                    labelClassName='btn btn-outline-primary',
                    labelCheckedClassName='active',
                    options=[
                        {'label': 'By Decade', 'value': 1},
                        {'label': '\u00A0\u00A0\u00A0Total\u00A0\u00A0\u00A0', 'value': 2}
                    ],
                    value=1
                ),
            ], style={'margin-left': 70})
        ], style={'margin-bottom': 0,
                  'margin-top': 0}
        ),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody(
                        [
                            dcc.Graph(id='map', figure={})
                        ]
                    )
                ], style={'backgroundColor': '#040609'})
            ], style={'margin-left': 75})
        ], style={'margin-bottom': 0,
                  'margin-top': 0}
        ),
        dbc.Row([
            dbc.Col([
                html.Div([
                    dbc.Button(
                        html.I(className='fas fa-angle-double-up',
                               style={'display': 'inline-block'}
                               ),
                        href='#',
                        external_link=True,
                        style={'background-color': '#040609',
                               'border-color': '#B2B297',
                               'border-width': 0.5,
                               'font-family': 'Palatino',
                               'color': '#B2B297'},
                        outline=True
                    )
                ], style={'text-align': 'right',
                          'margin-right': 95}
                )
            ], width=12)
        ], style={'margin-top': 3,
                  'margin-bottom': 20}
        ),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(
                        [
                            html.H6('Why did this happen? Theories',
                                    style={'color': '#e4e3bf',
                                           'font-family': 'Palatino',
                                           'font-size': 17}
                                    ),
                            html.Hr(className='my-2',
                                    style={'margin-bottom': 0,
                                           'color': '#e4e3bf'}
                                    )
                        ])
                ], style={'backgroundColor': '#040609',
                          'margin-right': 50,
                          'margin-left': 50})
            ], width=12)
        ], style={'margin-bottom': 0,
                  'margin-top': 0}
        ),
        dbc.Row([
            dbc.Col([
                html.Div(
                    dbc.Accordion(
                        [
                            dbc.AccordionItem(
                                [
                                    html.P(
                                        '"Across Europe, weather suddenly got wetter and colder—a '
                                        'phenomenon known as the Little Ice '
                                        'Age that pelted villages with freak frosts, floods, '
                                        'hailstorms, and plagues of mice '
                                        'and caterpillars. Witch hunts tended to correspond with '
                                        'ecological disasters and '
                                        'crop failures, along with the accompanying problems of '
                                        'famine, inflation, and '
                                        'disease. When the going got tough, witches made for a '
                                        'convenient scapegoat."',
                                        style={'color': '#B2B297',
                                               'font-family': 'Palatino',
                                               'font-size': 13}
                                    ),
                                    html.P(
                                        [
                                            'Gwynn Guilford, ',
                                            html.A('QUARTZ',
                                                   href=href1,
                                                   target='blank_',
                                                   style={'color': '#ba9c30',
                                                          'font-family': 'Palatino',
                                                          'font-size': 13}
                                                   )
                                        ],
                                        style={'color': '#B2B297',
                                               'font-family': 'Palatino',
                                               'font-size': 13,
                                               'margin-bottom': 20}
                                    ),
                                    html.P(
                                        '"Extreme rainfall—resulting in drought or floods—is exogenous '
                                        'and is associated with '
                                        'poor harvests and near-famine conditions in the region, and a large '
                                        'increase in the '
                                        'murder of "witches": there are twice as many witch murders in years '
                                        'of extreme '
                                        'rainfall as in other years. The victims are nearly all elderly '
                                        'women, typically '
                                        'killed by relatives."',
                                        style={'color': '#B2B297',
                                               'font-family': 'Palatino',
                                               'font-size': 13}
                                    ),
                                    html.P(
                                        [
                                            'Edward Miguel, ',
                                            html.A('Review of Economic Studies',
                                                   href=href2,
                                                   target='blank_',
                                                   style={'color': '#ba9c30',
                                                          'font-family': 'Palatino',
                                                          'font-size': 13}
                                                   )
                                        ],
                                        style={'color': '#B2B297',
                                               'font-family': 'Palatino',
                                               'font-size': 13,
                                               'margin-bottom': 20}
                                    )
                                ],
                                title='Bad Weather & Income Shocks',
                                className='h-50 rounded-3',
                                style={'border': 'none'}
                            ),
                            dbc.AccordionItem(
                                [
                                    html.P(
                                        '"<...> Witches were most likely to be tried and convicted in '
                                        'regions where magistrates '
                                        'departed from established legal statutes. We argue that '
                                        'collecting taxes required '
                                        'standardized and properly enforced judicial procedures. Hence '
                                        'as the fiscal '
                                        'demands on the state rose, central governments had an '
                                        'incentive to reorganize and '
                                        'coordinate the enforcement of judicial rules. Our hypothesis '
                                        'is that, as they did '
                                        'so, witch trials went down. Witch trials were, as the opening '
                                        'quote from Alfred '
                                        'Soman indicates, symptomatic of weak legal institutions."',
                                        style={'color': "#B2B297",
                                               'font-family': 'Palatino',
                                               'font-size': 13}
                                    ),
                                    html.P(
                                        [
                                            'Noel Johnson and Mark Koyama, ',
                                            html.A(
                                                'The Journal of Law and Economics',
                                                href=href3,
                                                target='blank_',
                                                style={'color': '#ba9c30',
                                                       'font-family': 'Palatino',
                                                       'font-size': 13}
                                            )
                                        ],
                                        style={'color': '#B2B297',
                                               'font-family': 'Palatino',
                                               'font-size': 13}
                                    )
                                ],
                                title='Weak Government',
                                className='h-50 rounded-3',
                                style={'border': 'none'}
                            ),
                            dbc.AccordionItem(
                                [
                                    html.P(
                                        '"Similar to how contemporary Republican and Democrat candidates '
                                        'focus campaign activity '
                                        'in political battlegrounds during elections to attract the loyalty '
                                        'of undecided voters, '
                                        'historical Catholic and Protestant officials focused witch-trial '
                                        'activity in '
                                        'confessional battlegrounds during the Reformation and '
                                        'Counter-Reformation to attract '
                                        'the loyalty of undecided Christians. Throughout Europe before '
                                        'Reformation and where '
                                        'Protestantism never gained ground after it, there was little '
                                        'need for witch trials, '
                                        'since religious-market contestation was minimal."',
                                        style={'color': "#B2B297",
                                               'font-family': 'Palatino',
                                               'font-size': 13}
                                    ),
                                    html.P(
                                        [
                                            'Peter T. Leeson and Jacob W. Russ, ',
                                            html.A(
                                                'The Economic Journal of the Royal Economic Society',
                                                href='https://www.peterleeson.com/Witch_Trials.pdf',
                                                target='blank_',
                                                style={'color': '#ba9c30',
                                                       'font-family': 'Palatino',
                                                       'font-size': 13}
                                            )
                                        ],
                                        style={'color': '#B2B297',
                                               'font-family': 'Palatino',
                                               'font-size': 13}
                                    )
                                ],
                                title='Competition Between Churches',
                                className='h-50 rounded-3',
                                style={'border': 'none'}
                            ),
                        ], className='h-50 bg-dark border-dark rounded-3'
                    )
                )
            ])
        ], style={'margin-top': 20,
                  'margin-bottom': 70,
                  'margin-left': 80,
                  'margin-right': 80}
        ),
        html.A(id='explore2'),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(
                        [
                            html.H6('Trials timeline',
                                    style={'color': '#e4e3bf',
                                           'font-family': 'Palatino',
                                           'font-size': 17}
                                    ),
                            html.Hr(className='my-2',
                                    style={'margin-bottom': 0,
                                           'color': '#e4e3bf'}
                                    )
                        ], style={'margin-bottom': 0,
                                  'margin-left': 50}
                    ),
                    dbc.CardBody(
                        [
                            dcc.Graph(figure=fig1)
                        ], style={'margin-left': 70}
                    )
                ], style={'backgroundColor': '#040609',
                          'margin-right': 50}
                )
            ], width=12)
        ], style={'margin-bottom': 0,
                  'margin-top': 0}
        ),
        dbc.Row([
            dbc.Col([
                html.Div([
                    dbc.Button(
                        html.I(className='fas fa-angle-double-up',
                               style={'display': 'inline-block'}
                               ),
                        href="#",
                        external_link=True,
                        style={'background-color': '#040609',
                               'border-color': '#B2B297',
                               'border-width': 0.5,
                               'font-family': 'Palatino',
                               'color': '#B2B297'},
                        outline=True
                    )
                ], style={'text-align': 'right',
                          'margin-right': 95}
                )
            ], width=12)
        ], style={'margin-top': 3,
                  'margin-bottom': 23}
        ),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H6('The deadliest trials of the time',
                                style={'color': '#e4e3bf',
                                       'font-family': 'Palatino',
                                       'font-size': 17}),
                        html.Hr(className='my-2', style={'margin-bottom': 0,
                                                         'color': '#e4e3bf'})
                    ])
                ], style={'backgroundColor': '#040609',
                          'margin-right': 50,
                          'margin-left': 50})
            ], width=12)
        ], style={'margin-bottom': 20, 'margin-top': 0}),
        dbc.Row([
            dbc.Col([
                html.Div(
                    dbc.Accordion(
                        [
                            dbc.AccordionItem(
                                [
                                    html.P(
                                        'The Region Was: Protestant',
                                        style={'color': '#B2B297',
                                               'font-family': 'Palatino',
                                               'font-weight': 'bold',
                                               'font-size': 13}),
                                    html.P(
                                        '"The pays de Vaud or Vaud (Waadt) region suffered from the most '
                                        'severe witch persecutions of any area of Switzerland in terms of '
                                        'numbers. In fact, it was "one of the most heavily afflicted regions '
                                        'of Western Europe." Also, "many more witches were executed in Vaud '
                                        'than in the rest of French Switzerland combined." <...> The "evidence '
                                        'suggests a generally harsher treatment of accused witches in the '
                                        'Protestant zones of French Switzerland. Witch-hunting usually started '
                                        'sooner in the Protestant regions than in the Catholic, and it '
                                        'remained harsher after 1600 in the Protestant areas."',
                                        style={"color": "#B2B297",
                                               'font-family': 'Palatino',
                                               'font-size': 13}
                                    ),
                                    html.P(
                                        [
                                            'Albert Winkler, ',
                                            html.A('Judicial Murder: The Witch-Craze '
                                                   'in Germany and Switzerland',
                                                   href=href4,
                                                   target='blank_',
                                                   style={'color': '#ba9c30',
                                                          'font-family': 'Palatino',
                                                          'font-size': 13}
                                                   )
                                        ],
                                        style={'color': '#B2B297',
                                               'font-family': 'Palatino',
                                               'font-size': 13,
                                               'margin-bottom': 20}
                                    ),
                                ],
                                title='Vaud, Switzerland | 3,378 killed',
                                className='h-50 rounded-3',
                                style={'border': 'none'}
                            ),
                            dbc.AccordionItem(
                                [
                                    html.P(
                                        'The Region Was: Catholic',
                                        style={'color': '#B2B297',
                                               'font-family': 'Palatino',
                                               'font-weight': 'bold',
                                               'font-size': 13}),
                                    html.P(
                                        '"Among prince-bishops, Philipp Adolf von Ehrenberg of Würzburg '
                                        'was particularly active: in his reign of eight years (1623–31) '
                                        'he burnt 900 persons, including his own nephew, nineteen Catholic '
                                        'priests, and children of seven who were said to have had '
                                        'intercourse with demons."',
                                        style={'color': '#B2B297',
                                               'font-family': 'Palatino',
                                               'font-size': 13}
                                    ),
                                    html.P(
                                        ['Hugh Trevor-Roper, ',
                                         html.A(
                                             'The Crisis of the Seventeenth Century',
                                             href=href5,
                                             target='blank_',
                                             style={'color': '#ba9c30',
                                                    'font-family': 'Palatino',
                                                    'font-size': 13}
                                         )
                                         ],
                                        style={'color': '#B2B297',
                                               'font-family': 'Palatino',
                                               'font-size': 13}
                                    ),
                                    html.P(
                                        '"A contemporary letter from 1629 describes how people of all '
                                        'ages and classes were arrested every day. A third of the '
                                        "population was suspected of having attended the Witches' Sabbath "
                                        'and being noted in the black book of Satan that the authorities '
                                        'were searching for. People from all walks of life were arrested '
                                        'and charged, regardless of age, profession, or sex, for reasons '
                                        'ranging from murder and satanism to humming a song including the '
                                        'name of the Devil, or simply for being vagrants and unable to give '
                                        'a satisfactory explanation of why they were passing through town."',
                                        style={'color': '#B2B297',
                                               'font-family': 'Palatino',
                                               'font-size': 13}
                                    ),
                                    html.P(
                                        html.A(
                                            'Wikipedia',
                                            href=href6,
                                            target='blank_',
                                            style={'color': '#ba9c30',
                                                   'font-family': 'Palatino',
                                                   'font-size': 13}
                                        ),
                                        style={'color': '#B2B297',
                                               'font-family': 'Palatino',
                                               'font-size': 13}
                                    )
                                ],
                                title='Würzburg, Germany | 1,119 killed',
                                className='h-50 rounded-3',
                                style={'border': 'none'}
                            ),
                            dbc.AccordionItem(
                                [
                                    html.P(
                                        'The Region Was: Catholic',
                                        style={'color': '#B2B297',
                                               'font-family': 'Palatino',
                                               'font-weight': 'bold',
                                               'font-size': 13}),
                                    html.P(
                                        '"But the worst persecution of all, in those years, was '
                                        'probably at Bamberg. There the prince-bishop was Johann Georg '
                                        'II Fuchs von Dornheim, known as the Hexenbischof or "Witch-bishop."'
                                        ' He built a "witch-house," complete with torture-chamber adorned '
                                        'with appropriate biblical texts, and in his ten-year reign '
                                        '(1623–33) he is said to have burnt 600 witches. He, too, had '
                                        'his Court-prophet, his suffragan, Bishop Forner, who wrote a '
                                        'learned book on the subject. '
                                        "One of their victims was the bishop's chancellor, Dr. Haan, "
                                        'burnt as a witch for showing suspicious leniency as a judge. '
                                        'Under torture he confessed to having seen five burgomasters of '
                                        'Bamberg at the sabbat, and they too were duly burnt."',
                                        style={"color": "#B2B297", 'font-family': 'Palatino', 'font-size': 13}
                                    ),
                                    html.P(
                                        ['Hugh Trevor-Roper, ',
                                         html.A(
                                             'The Crisis of the Seventeenth Century',
                                             href=href5,
                                             target='blank_',
                                             style={'color': '#ba9c30',
                                                    'font-family': 'Palatino',
                                                    'font-size': 13}
                                         )
                                         ],
                                        style={'color': '#B2B297',
                                               'font-family': 'Palatino',
                                               'font-size': 13}
                                    )
                                ],
                                title='Bamberg, Germany | ~1,000 killed',
                                className='h-50 rounded-3',
                                style={'border': 'none'}
                            ),
                            dbc.AccordionItem(
                                [
                                    html.P(
                                        'The Region Was: Catholic',
                                        style={'color': '#B2B297',
                                               'font-family': 'Palatino',
                                               'font-weight': 'bold',
                                               'font-size': 13}),
                                    html.P(
                                        '"Johann von Schöneburg began his reign in 1581. "Wonderfully addicted"'
                                        ' to the Jesuits, for whom he built and endowed a splendid college, '
                                        'he showed his devotion in militant fashion too. First he rooted out '
                                        'the Protestants, then the Jews, then the witches: three stereotypes '
                                        'of nonconformity. Thanks to his patronage the campaign of Trier was '
                                        '"of an importance quite unique in the history of witchcraft." In '
                                        'twenty-two villages 368 witches were burnt between 1587 and 1593, '
                                        'and two villages, in 1585, were left with only one female inhabitant '
                                        'apiece.',
                                        style={'color': '#B2B297',
                                               'font-family': 'Palatino',
                                               'font-size': 13}
                                    ),
                                    html.P(
                                        'Among the victims were men, women and children of noble '
                                        'birth and public position. Such was Dietrich Flade, rector of the '
                                        'university and chief judge of the electoral court. Unconvinced '
                                        'by the confessions which had been extracted by torture, he judged '
                                        'the victims leniently. Consequently the prince-archbishop had him '
                                        'arrested, accused of witchcraft himself, tortured till he confessed '
                                        'whatever was put to him, strangled and burnt."',
                                        style={'color': '#B2B297', 'font-family': 'Palatino', 'font-size': 13}
                                    ),
                                    html.P(
                                        ['Hugh Trevor-Roper, ',
                                         html.A(
                                             'The Crisis of the Seventeenth Century',
                                             href=href5,
                                             target='blank_',
                                             style={'color': '#ba9c30',
                                                    'font-family': 'Palatino',
                                                    'font-size': 13}
                                         )
                                         ],
                                        style={'color': '#B2B297',
                                               'font-family': 'Palatino',
                                               'font-size': 13}
                                    )
                                ],
                                title='Trier, Germany | ~1,000 killed',
                                className='h-50 rounded-3',
                                style={'border': 'none'}
                            )
                        ],
                        className='h-50 bg-dark border-dark rounded-3'
                    )
                )
            ])
        ], style={'margin-top': 20,
                  'margin-bottom': 70,
                  'margin-left': 80,
                  'margin-right': 80}),
        html.A(id='explore3'),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(
                        [
                            html.H6('Regions&cities',
                                    style={'color': '#e4e3bf',
                                           'font-family': 'Palatino',
                                           'font-size': 17}
                                    ),
                            html.Hr(className='my-2',
                                    style={'margin-bottom': 0,
                                           'color': '#e4e3bf'}
                                    )
                        ], style={'margin-right': 50,
                                  'margin-left': 50, 
                                  'margin-bottom': 0}
                    ),
                    dbc.CardBody(
                        [
                            dcc.Graph(figure=fig2)
                        ], style={'margin-left': 75, 'margin-top': 0}
                    )
                ], style={'backgroundColor': '#040609'})
            ], width=12)
        ], style={'margin-bottom': 0,
                  'margin-top': 50}
        ),
        dbc.Row([
            dbc.Col([
                html.Div(
                    [
                        dbc.Button(html.I(className='fas fa-angle-double-up',
                                          style={'display': 'inline-block'}
                                          ),
                                   href='#',
                                   external_link=True,
                                   style={'background-color': '#040609',
                                          'border-color': '#B2B297',
                                          'border-width': 0.1,
                                          'font-family': 'Palatino',
                                          'color': '#B2B297'},
                                   outline=True
                                   )
                    ], style={'text-align': 'right',
                              'margin-right': 95}
                )
            ], width=12)
        ], style={'margin-top': 3,
                  'margin-bottom': 3}
        ),
        dbc.Row(
            [
                dbc.Col(width=4),
                dbc.Col(
                    [
                        dbc.Nav(
                            [
                                dbc.NavItem(dbc.NavLink('ABOUT:',
                                                        disabled=True,
                                                        style={'color': '#e4e3bf',
                                                               'font-family': 'Palatino',
                                                               'font-size': 13,
                                                               'padding-left': 100,
                                                               'padding-right': 0}
                                                        )
                                            ),
                                dbc.NavLink(html.I(className='fa-brands fa-github'),
                                            href='https://github.com/lomska/plotly-dash-datavizes-witch-hunt-history',
                                            target='_blank',
                                            style={'color': '#e4e3bf',
                                                   'font-family': 'Palatino',
                                                   'font-size': 17,
                                                   'padding-left': 0}
                                            ),
                                dbc.NavLink(html.I(className='fa-brands fa-kaggle'),
                                            href='https://github.com/lomska/plotly-dash-datavizes-witch-hunt-history',
                                            target='_blank',
                                            style={'color': '#e4e3bf',
                                                   'font-family': 'Palatino',
                                                   'font-size': 17}
                                            )
                            ], pills=True
                        )
                    ], width=4),
                dbc.Col(width=4)
            ], style={'margin-top': 0}
        ),
        dbc.Row(style={'margin-top': 10})
    ], fluid=True,
        className="border border-secondary p-3 mb-5 rounded",
        style={'width': '1140px',
               'backgroundColor': '#040609',
               'margin-top': 50,
               'margin-bottom': 50}
    )
], style={'align-items': 'center'}
)


@app.callback(
    Output('fade', 'is_in'),
    [Input('fade-button', 'n_clicks')],
    [State('fade', 'is_in')],
)
def toggle_fade(n, is_in):
    if not n:
        return False
    return not is_in


@app.callback(
    Output('map', 'figure'),
    [Input('radios', 'value')])
def update_map(button):
    if button == 1:
        fig_map = fig
    if button == 2:
        fig_map = fig0
    return fig_map


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)