import json
import pickle
import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import dcc, html
from google.genai import types

from constants import redis_instance, client  

dash.register_page(__name__)

def layout(layout_id=None):
    
    layout_data = redis_instance.get(layout_id)
    if not layout_data:
        return dmc.Text("No saved layout found.", c="red")

    layout_data = pickle.loads(layout_data)

   
    figures = [i["props"]["children"][0]["props"]["figure"] for i in layout_data[1:]]

 
    question = (
        "Summarize these charts with trends, outliers, and insights. "
        f"There are {len(figures)} charts:\n\n"
    )

    try:
        response = client.generate_content(question + json.dumps(figures)[0:3900])
        ai_summary = response.text if response.text else "Gemini did not return a valid summary."
    except Exception as e:
        ai_summary = f"Error calling Gemini: {str(e)}"

    return dmc.LoadingOverlay(
        [
            dbc.Button("Home", href="/", style={"background-color": "#238BE6", "margin": "10px"}),
            html.Div([dcc.Markdown(ai_summary), html.Div(layout_data[1:])], style={"padding": "40px"}),
        ]
    )