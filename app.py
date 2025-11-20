import os
import pickle
import uuid
from dotenv import load_dotenv
from flask import request
from dash import Dash, page_container, callback, Input, Output, State, no_update
import dash_mantine_components as dmc
import google.generativeai as genai

from constants import redis_instance
import utils


load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("❌ GEMINI_API_KEY not found in .env")


genai.configure(api_key=api_key)


app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    title="Data Dashboard",  
    use_pages=True,
)
server = app.server


def layout():
    return dmc.MantineProvider(
        [
            dmc.Box(
                [
                    dmc.Title(
                        "JarvisAI",
                        order=1,
                        style={
                            "color": "#F0F8FF",       
                            "fontWeight": 700,
                            "fontSize": "32px",
                            "textAlign": "left",
                            "marginBottom": "10px"
                        }
                    )
                ],
                style={
                    "backgroundColor": "#000000",   
                    "padding": "20px",            
                    "borderRadius": "8px"          
                }
            ),
            utils.jumbotron(),
            page_container,
        ]
    )

app.layout = layout


@callback(
    Output("save-clip", "content", allow_duplicate=True),
    Input("save-clip", "n_clicks"),
    State("current-charts", "children"),
    prevent_initial_call=True
)
def copy_link(n, current):
    if n and current:
        try:
            figure_id = str(uuid.uuid4())
            redis_instance.set(figure_id, pickle.dumps(current))
            return request.host_url.rstrip("/") + f"/view?layout={figure_id}"
        except Exception as e:
            return f"Error saving chart: {str(e)}"
    return no_update


if __name__ == "__main__":
    app.run(debug=True)