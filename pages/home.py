import pandas as pd
from dash import html, dcc, Input, Output, State, callback, no_update, register_page, callback_context
import dash_mantine_components as dmc
import dash_chart_editor as dce
import plotly.express as px
from constants import client
from utils import generate_cache_key, get_cached_response, set_cached_response
import diskcache
import hashlib
import utils
import json
import numpy as np 
import base64
import io
from dash import html, dcc, callback_context, no_update
from dash.dependencies import Input, Output, State, ALL, MATCH

from PIL import Image

register_page(__name__, path="/")


layout = dmc.Stack(
    [
        
       

        html.Div(
            id="chart-editor-container",
            
            children=[
                dmc.Text(
                    "Upload a dataset to start visualizing your data.",
                    c="dimmed",
                    size=30,  
                    fw=600,  
                    style={"textAlign": "center", "padding": "10px","lineHeight": "1.8","height": "22vh"},
                )
            ],
            style={"maxWidth": "600px", "margin": "0 auto","margin-top": "50px;"},
        ),

        
        html.Div(
            id="input-box-container",
            children=[
                html.Div(
                    [
                       
                        dmc.ActionIcon(
                            "＋",
                            id="open-upload-modal",
                            variant="gradient",
                            gradient={"from": "indigo", "to": "cyan", "deg": 45},
                            size="xl",
                            radius="xl",
                            style={"marginRight": "15px"},
                        ),
                        
                        dmc.Textarea(
                            id="question",
                            placeholder="Ask me anything about your dataset...",
                            autosize=True,
                            minRows=2,
                            maxRows=6,
                            
                            radius="xl",
                            style={
                                
                                "paddingRight": "90px",  
                                "width": "100%",
                                
                                "fontSize": "18px",        
                                "lineHeight": "1.5",
                                "boxShadow": "0 2px 6px rgba(0,0,0,0)",  
                  
                            },
                            
                            disabled=True,
                        ),
                        dmc.Button(
                            "→",
                            id="chat-submit",
                            disabled=True,
                            variant="gradient",
                            gradient={"from": "indigo", "to": "cyan"},
                            size="lg",
                            radius="md",
                            style={
                                "position": "absolute",
                                "right": "18px",  
                                "top": "50%",
                                "transform": "translateY(-50%)",
                            },
                        ),
                    ],
                    style={
                        "display": "flex",
                        "alignItems": "center",
                        "maxWidth": "900px",  
                        "margin": "0 auto",
                        "position": "relative",
                    },
                ),
                dmc.LoadingOverlay(
            id="loading-page",
            loaderProps={"variant": "bars", "color": "indigo", "size": "xl"},
            overlayProps={"color": "#eef2ff", "opacity": 0.6, "blur": 5},
            style={"position": "fixed", "top": 0, "left": 0, "width": "100vw", "height": "100vh", "zIndex": 2000},
            visible=False,
        ),
            ],
            style={
                "transition": "all 0.3s ease",
                "margin": "20px auto",
                "width": "100%",
                "maxWidth": "700px",  
                "textAlign": "center",
                "background": "#ffffff",
            },
        ),

        
html.Div(
    id="suggestion-container",
    children=[
        dmc.Group(
            [
                
                dmc.Paper(
                    html.Div(
                        "What charts can I use?",
                        id="suggestion-1",
                        n_clicks=0,  
                        style={"cursor": "pointer", "textAlign": "center"}
                    ),
                    radius="xl",
                    shadow="sm",
                    p="md",
                    style={
                        "border": "2px solid",
                        "borderImage": "linear-gradient(45deg, indigo, cyan) 1",
                        "width": "260px",
                        "transition": "transform 0.2s ease, box-shadow 0.2s ease",
                        "font-size": "15px",
                        "borderRadius": "20px",
                         "border": "2px solid transparent",
                    },
                    withBorder=True,
                ),

                
                dmc.Paper(
                    html.Div(
                        "What are the key trends in my dataset?",
                        id="suggestion-2",
                        n_clicks=0,
                        style={"cursor": "pointer", "textAlign": "center"}
                    ),
                    radius="xl",
                    shadow="sm",
                    p="md",
                    style={
                        "border": "2px solid",
                        "borderImage": "linear-gradient(45deg, indigo, cyan) 1",
                        "width": "260px",
                        "transition": "transform 0.2s ease, box-shadow 0.2s ease",
                        "font-size": "15px",
                        "borderRadius": "20px",
                         "border": "2px solid transparent",
                    },
                    withBorder=True,
                ),

                
                dmc.Paper(
                    html.Div(
                        "Can you summarize my data?",
                        id="suggestion-3",
                        n_clicks=0,
                        style={"cursor": "pointer", "textAlign": "center"}
                    ),
                    radius="xl",
                    shadow="sm",
                    p="md",
                    style={
                        "border": "2px solid",
                        "borderImage": "linear-gradient(45deg, indigo, cyan) 1",
                        "width": "260px",
                        "transition": "transform 0.2s ease, box-shadow 0.2s ease",
                        "font-size": "15px",
                        "borderRadius": "20px",
                         "border": "2px solid transparent",
                    },
                    withBorder=True,
                ),
            ],
            justify="center",
            gap="sm",
            style={
                "maxWidth": "900px",
                "margin": "10px auto",
                "width": "100%",
            },
        )
    ],
    style={"display": "block"},
),

       
        html.Div(
            id="dataset-status",
            style={
                "fontSize": "14px",
                "color": "#555",
                "textAlign": "center",
                "margin": "2px auto",
                "maxWidth": "800px",
            },
        ),

        
        html.Div(
            id="chat-output",
            style={
                "padding": "15px",
                "minHeight": "150px",
               
                "margin": "10px auto",
                "maxWidth": "1000px",
                "display": "none",
            },
        ),

        
        html.Div(
            id="current-charts",
            style={
                "width": "calc(100vw - 40px)",  
                "padding": "0 20px",  
                "margin": "20px auto",
                "display": "flex",
                "flexDirection": "column",
            },
        ),

        
        utils.upload_modal(),

        
        dcc.Store(id="uploaded-data"),
        
        dcc.Store(id="input-box-state", data={"is_fixed": False}),
        # At the bottom of your layout Stack, before the closing ]
        dmc.Modal(
            id="drill-modal",
            opened=False,          # starts closed
            title="Subset Analysis",
            children=[],           # will be filled dynamically by callback
            size="xl",             # optional: make modal wider
            overlayProps={"blur": 3, "opacity": 0.5},  # optional styling
        )

    ],
    gap="lg",
    p="lg",
    style={
        "minHeight": "100vh",
        "paddingBottom": "200px",
        "width": "100%",
        "maxWidth": "none",
        "overflowX": "hidden",
        
    },
)


@callback(
    Output("upload-modal", "opened", allow_duplicate=True),
    Input("open-upload-modal", "n_clicks"),
    prevent_initial_call=True,
)
def open_upload_modal(n_clicks):
    return bool(n_clicks)


@callback(
    [
        Output("uploaded-data", "data", allow_duplicate=True),
        Output("dataset-status", "children", allow_duplicate=True),
        Output("chart-editor-container", "children", allow_duplicate=True),
        Output("question", "disabled", allow_duplicate=True),
        Output("chat-submit", "disabled", allow_duplicate=True),
    ],
    Input("upload-data", "contents"),
    prevent_initial_call=True,
)
def handle_upload(contents):
    if not contents:
        return [no_update] * 5

    # contents is a list, even for a single file
    content_string_full = contents[0]  # <-- get first item

    content_type, content_string = content_string_full.split(",")
    decoded = base64.b64decode(content_string)

    # CSV
    if "csv" in content_type:
        df, error = utils.parse_csv(content_string_full)  # pass the full contents string to your parser
        if error:
            return no_update, dmc.Text(f"Error loading CSV: {error}", c="red"), no_update, True, True
        if df.empty:
            return no_update, dmc.Text("Uploaded CSV is empty.", c="red"), no_update, True, True

        data_dict = df.to_dict("list")
        chart_editor = dce.DashChartEditor(
            id="chart-editor",
            dataSources=data_dict,
            style={"display": "block"}
        )

        return data_dict, dmc.Text(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns", c="green"), chart_editor, False, False

    # IMAGE
    elif "image" in content_type:
        try:
            image = Image.open(io.BytesIO(decoded))
            # Store image in uploaded-data (you can store as bytes or base64)
            data_dict = {"image": content_string}  # or decoded bytes
            chart_editor = html.Div()  # empty chart editor for now
            return data_dict, dmc.Text("Image uploaded. AI analysis will run.", c="blue"), chart_editor, False, False
        except Exception as e:
            return no_update, dmc.Text(f"Error loading image: {e}", c="red"), no_update, True, True


    # OTHER
    else:
        return no_update, dmc.Text("Unsupported file type.", c="red"), no_update, True, True


@callback(
    [
        Output("current-charts", "children", allow_duplicate=True),
        Output("chat-output", "children", allow_duplicate=True),
        Output("chat-output", "style", allow_duplicate=True),
        Output("question", "value", allow_duplicate=True),
        Output("input-box-state", "data", allow_duplicate=True),
    ],
    [
        Input("chat-submit", "n_clicks"),
        Input("suggestion-1", "n_clicks"),
        Input("suggestion-2", "n_clicks"),
        Input("suggestion-3", "n_clicks"),
    ],
    [
        State("question", "value"),
        State("uploaded-data", "data"),
        State("chat-output", "style"),
        State("input-box-state", "data"),
    ],
    prevent_initial_call=True,
)
def handle_chat(chat_clicks, s1, s2, s3, question_value, uploaded_data, cur_chat_style, input_box_state):
    ctx = callback_context
    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

    suggestions = {
        "suggestion-1": "What charts can I use?",
        "suggestion-2": "What are the key trends in my dataset?",
        "suggestion-3": "Can you summarize my data?",
    }

    if triggered_id in suggestions:
        question_value = suggestions[triggered_id]

    updated_charts = []
    updated_chat = []
    updated_chat_style = cur_chat_style or {"display": "none"}
    input_state = input_box_state or {"is_fixed": False}

    

    if not uploaded_data:
        return [], [dcc.Markdown("Please upload a dataset first.")], updated_chat_style, question_value, input_state
    
    

    df = pd.DataFrame(uploaded_data)

    if not (chat_clicks or triggered_id in suggestions):
        return [], [], updated_chat_style, question_value, input_state

    # -----------------------------
    # CACHE CHECK WITH FALLBACK
    # -----------------------------
    try:
        cache_key = generate_cache_key(df, question_value)
        cached = get_cached_response(cache_key)
    except:
        cached = None

    try:
        if cached:
            chart_blocks, global_summary, chart_plan = cached
        else:
            # -----------------------------
            # 1) HIGH-LEVEL DATA SUMMARY
            # -----------------------------
            numeric_stats = df.describe(include='all', percentiles=[0.25, 0.5, 0.75]).fillna("").to_dict()
            col_dtypes = {col: str(df[col].dtype) for col in df.columns}
            col_uniques = {col: df[col].nunique() for col in df.columns}

            global_summary_prompt = f"""
You are an expert data analyst.

You are given a dataset summary:
- Column data types: {json.dumps(col_dtypes, indent=2)}
- Unique values per column: {json.dumps(col_uniques, indent=2)}
- Numeric statistics (min, max, mean, std, quartiles): {json.dumps(numeric_stats, indent=2)}

User question:
"{question_value}"

Your job is to write a **direct, focused answer to the user's question**.

RULES:
- DO NOT write a generic dataset summary.
- ONLY discuss items that relate to the user's actual question.
- Base everything on the statistics provided.
- If the user asks about a specific field (example: salary, role, project), focus only on those.
- If the question is broad, give a high-level cross-column analysis.
- If the question is specific, give a narrow deep analysis.
- DO NOT invent data.
- DO NOT guess missing values.

Your output should be:
### Key Insights Related to the Question
<analysis here>
"""
            global_summary = client.generate_content(global_summary_prompt).text.strip()

            summary_block = dmc.Paper(
                dcc.Markdown(f"### 📊 Overall Dataset Summary\n{global_summary}"),
                radius="md",
                shadow="sm",
                p="lg",
                style={"marginBottom": "25px", "background": "#eef2ff"},
            )

            # -----------------------------
            # 2) GET CHART PLAN
            # -----------------------------
            light_df_sample = df.head(7).to_dict(orient="records")
            chart_request_prompt = f"""
You are a visualization expert.

Dataset preview:
{json.dumps(light_df_sample, indent=2)}

User question: "{question_value}"

Return ONLY JSON describing suggested charts:
{{
  "charts": [
    {{"type": "bar" | "line" | "pie" | "scatter" | "histogram",
      "x": "column",
      "y": "column (optional)",
      "names": "column (for pie)",
      "values": "column (for pie)"
    }}
  ]
}}
No extra text.
"""
            resp = client.generate_content(chart_request_prompt).text.strip()
            try:
                parsed = json.loads(resp[resp.find("{"): resp.rfind("}") + 1])
            except:
                parsed = {"charts": []}

            chart_plan = parsed.get("charts", [])
            chart_funcs = {"bar": px.bar, "line": px.line, "pie": px.pie, "scatter": px.scatter, "histogram": px.histogram}
            chart_blocks = [summary_block]
            chart_index = 0

            # -----------------------------
            # 3) BUILD EACH CHART + DEEP INSIGHT
            # -----------------------------
            for cfg in chart_plan:
                ctype = cfg.get("type")
                func = chart_funcs.get(ctype)
                if not func:
                    continue

                fig = None
                seq_colors = px.colors.sequential.Plasma
                cat_colors = px.colors.qualitative.Bold

                if ctype == "pie":
                    names = cfg.get("names")
                    values = cfg.get("values")
                    grouped = df.groupby(names)[values].sum().to_dict()
                    fig = func(df, names=names, values=values, color=names, color_discrete_sequence=cat_colors)
                    stats_payload = {"type": ctype, "group_totals": grouped}

                else:
                    x = cfg.get("x")
                    y = cfg.get("y")
                    if y:
                        grouped = df.groupby(x)[y].agg(["mean", "min", "max", "std"]).fillna("").to_dict()
                        fig = func(df, x=x, y=y, color=y, color_continuous_scale=seq_colors)
                    else:
                        grouped = {}
                        fig = func(df, x=x, y=y)

                    stats_payload = {"type": ctype, "stats": grouped, "x": x, "y": y}

                fig.update_layout(
                    height=350,
                    margin=dict(l=20, r=20, t=40, b=20),
                    template="plotly_white"
                )

                insight_prompt = f"""
            You are an expert statistical analyst.

            Analyze ONLY using this exact numeric summary for a chart:
            {json.dumps(stats_payload, indent=2)}

            Produce **very concise insights (3–5 bullet points max)**:
            - Each bullet MUST be factual and based only on provided numbers.
            - Highlight only the strongest pattern, biggest difference, or main anomaly.
            - No storytelling, no fluff, no long paragraphs.
            - No rephrasing of the chart type.

            STRICT RULES:
            • Only use the provided stats.
            • Do not guess missing values.
            • Keep bullets short, direct, and quantitative.
            """
                insight = client.generate_content(insight_prompt).text.strip()

                # append each chart INSIDE the loop
                chart_blocks.append(
                    html.Div(
                        [
                            dcc.Graph(
                                id={"type": "chart", "index": chart_index},
                                figure=fig,
                                style={"width": "100%"}
                            ),
                            dmc.Paper(
                                dcc.Markdown(f"### Insight for this chart\n{insight}"),
                                radius="md",
                                shadow="sm",
                                p="md",
                                style={"marginTop": "12px", "background": "#f8fafc"},
                            ),
                            html.Div(
                                id={"type": "drill-output", "index": chart_index},
                                style={"marginTop": "20px"}
                            ),
                        ],
                        style={"marginBottom": "40px", "padding": "10px", "border": "1px solid #eee", "borderRadius": "8px"},
                    )
                )

                chart_index += 1

            # -----------------------------
            # SAVE TO CACHE (wrapped in try)
            # -----------------------------
            try:
                set_cached_response(cache_key, (chart_blocks, global_summary, chart_plan))
            except:
                pass

        # -----------------------------
        # FINAL UI RETURNS
        # -----------------------------
        updated_chat = [
            html.Div(
                dmc.Paper(
                    [
                        dcc.Markdown(f"### ❓ User Question"),
                        dcc.Markdown(f"{question_value}"),
                        dcc.Markdown(f"**Generated {len(chart_plan)} chart(s).**"),
                    ],
                    radius="lg",
                    shadow="md",
                    p="md",
                    style={
                        "background": "#f1f5ff",
                        "borderRadius": "12px",
                        "border": "1px solid #d0d7ff",
                        "width": "280px",
                        "marginLeft": "845px",
                    },
                )
            )
        ]

        updated_chat_style["display"] = "block"
        input_state["is_fixed"] = True

        return chart_blocks, updated_chat, updated_chat_style, None, input_state

    except Exception as e:
        return [], [dcc.Markdown(f"Error: {str(e)}")], updated_chat_style, question_value, input_state

@callback(
    [
        Output("input-box-container", "style", allow_duplicate=True),
        Output("suggestion-container", "style", allow_duplicate=True),
    ],
    Input("input-box-state", "data"),
    prevent_initial_call=True,
)
def update_input_box_position(input_box_state):
    suggestion_style = {"display": "block"}
    if input_box_state.get("is_fixed", False):
        suggestion_style = {"display": "none"}
        return {
            "position": "fixed",
            "bottom": "0",
            "width": "100vw !important",
            "background": "#ffffff",
            "padding": "10px 0",
            "zIndex": "1000",
            "transition": "all 0.3s ease",
            "display": "flex",
            "justifyContent": "center",
            "overflowX": "hidden",
        }, suggestion_style
    return {
        "margin": "20px auto",
        "width": "100%",
        "maxWidth": "700px",
        "textAlign": "center",
        "background": "#ffffff",
        "transition": "all 0.3s ease",
        "display": "block",
    }, suggestion_style

@callback(
    Output("question", "value", allow_duplicate=True),
    [
        Input("suggestion-1", "n_clicks"),
        Input("suggestion-2", "n_clicks"),
        Input("suggestion-3", "n_clicks"),
    ],
    prevent_initial_call=True,
)
def handle_suggestion_click(s1_clicks, s2_clicks, s3_clicks):
    ctx = callback_context
    if not ctx.triggered:
        return no_update
    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]
    suggestions = {
        "suggestion-1": "What charts can I use for my data?",
        "suggestion-2": "What are the key trends in my dataset?",
        "suggestion-3": "Can you summarize my data?",
    }
    return suggestions.get(triggered_id, no_update)  

from dash import html, dcc
import dash_mantine_components as dmc
import plotly.express as px

# Store the modal open state
dmc.Modal(id="drill-modal", opened=False, title="Subset Analysis", children=[])

# Drilldown callback
@callback(
    Output("drill-modal", "opened"),
    Output("drill-modal", "children"),
    Input({"type": "chart", "index": ALL}, "clickData"),
    State("uploaded-data", "data"),
    prevent_initial_call=True
)
def open_drill_modal(all_clicks, uploaded_data):
    if not uploaded_data:
        return False, no_update

    ctx = callback_context
    if not ctx.triggered:
        return False, no_update

    clickData = ctx.triggered[0]["value"]
    if not clickData or "points" not in clickData or not clickData["points"]:
        return False, dmc.Text("No data for this chart.", c="red")

    df = pd.DataFrame(uploaded_data)
    point = clickData["points"][0]
    clicked_x = point.get("x") or point.get("label") or point.get("customdata")
    clicked_x_str = str(clicked_x)

    # Find the column containing the clicked value
    filter_col = None
    for col in df.columns:
        if clicked_x_str in df[col].astype(str).values:
            filter_col = col
            break

    if filter_col is None:
        return False, dmc.Text("Could not determine column to filter.", c="red")

    subset = df[df[filter_col].astype(str) == clicked_x_str]
    if subset.empty:
        return False, dmc.Text("No records found for this category.", c="red")

    # Generate charts with error handling
    try:
        subset_charts = generate_subset_charts(subset)
        if not subset_charts:
            raise ValueError("No charts generated for this subset.")
    except Exception as e:
        return False, dmc.Text(f"Chart generation failed: {str(e)}", c="red")

    # Modal content: header + charts
    modal_content = dmc.Stack(
            [dmc.Text(
        f"📌 Drilldown Analysis: {filter_col} = {clicked_x_str}",
        fz="lg",   # font size
        fw=700     # font weight
    )
        ]
        + subset_charts,
        gap="md"
    )

    return True, modal_content

def generate_subset_charts(df_subset):
    charts = []

    sample = df_subset.head(7).to_dict("records")

    # Ask AI for new chart plan
    plan_prompt = f"""
    You are a visualization expert.
    Dataset subset:
    {json.dumps(sample, indent=2)}
    Return ONLY JSON:
    {{
      "charts": [
        {{"type": "...", "x": "...", "y": "...", "names": "...", "values": "..."}}
      ]
    }}
    """

    resp = client.generate_content(plan_prompt).text.strip()

    # Robust JSON parsing
    try:
        parsed = json.loads(resp[resp.find("{"): resp.rfind("}") + 1])
    except Exception as e:
        return [dmc.Text(f"Chart plan error: {str(e)}", c="red")]

    chart_plan = parsed.get("charts", [])
    funcs = {
        "bar": px.bar,
        "line": px.line,
        "pie": px.pie,
        "scatter": px.scatter,
        "histogram": px.histogram
    }

    for cfg in chart_plan:
        t = cfg.get("type")
        f = funcs.get(t)
        if not f:
            continue

        try:
            if t == "pie":
                fig = f(df_subset, names=cfg.get("names"), values=cfg.get("values"))
            else:
                fig = f(df_subset, x=cfg.get("x"), y=cfg.get("y"))

            fig.update_layout(
                height=350,
                margin=dict(l=20, r=20, t=40, b=20),
                template="plotly_white"
            )

            charts.append(
                dmc.Paper(
                    dcc.Graph(figure=fig),
                    radius="md",
                    shadow="sm",
                    p="md",
                    style={"marginBottom": "20px"}
                )
            )
        except Exception as e:
            charts.append(dmc.Text(f"Chart generation error: {str(e)}", c="red"))

    return charts
