import dash_mantine_components as dmc
from dash import html, dcc
import base64
import io
import pandas as pd
import hashlib
from constants import cache

def generate_cache_key(df, question):
    df_str = df.to_json()
    return hashlib.sha256((df_str + question).encode("utf-8")).hexdigest()

def get_cached_response(key):
    return cache.get(key)

def set_cached_response(key, value, expire=3600):
    cache.set(key, value, expire=expire)
def jumbotron():
    return dmc.Group([
         
    ])

def upload_modal():
    return dmc.Modal(
        title="Upload CSV File",
        id="upload-modal",
        children=[
            dcc.Upload(
                id="upload-data",
                children=dmc.Button("Select CSV File"),
                multiple=False
            ),
            html.Div(id="upload-status")
        ]
    )


def generate_prompt(df: pd.DataFrame, question: str) -> str:
    """
    Generate a concise prompt for Gemini based on dataset columns and user question.
    """
   
    columns_preview = list(df.columns)[:20]
    return (
        f"Dataset columns: {columns_preview}\n"
        f"Question: {question}\n"
        "Provide a concise answer or suggest a chart."
    )

def parse_csv(contents: str) -> tuple[pd.DataFrame | None, str | None]:
    """
    Parse uploaded CSV file from base64 content.
    Returns: (DataFrame, error_message)
    """
    try:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        if df.empty:
            return None, "Uploaded file is empty."
        return df, None
    except Exception as e:
        return None, f"Error parsing CSV: {str(e)}"

        
def generate_prompt(df, question):
    
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    categorical_cols = df.select_dtypes(exclude="number").columns.tolist()

    
    context = f"""
    You are analyzing a dataset with the following columns:
    Numeric columns: {', '.join(numeric_cols) if numeric_cols else 'None'}
    Categorical columns: {', '.join(categorical_cols) if categorical_cols else 'None'}

    The user asked: "{question}"

    If the question asks for charts, suggest the most relevant chart types based on the dataset.
    - For categorical vs numeric: Bar chart or Pie chart.
    - For numeric vs numeric: Scatter plot or Line chart.
    - For single numeric column: Histogram.
    - If user says "all possible charts", suggest all relevant chart types.
    - Avoid using columns like names, IDs, or codes unless explicitly requested.
    - Respond in plain text, describing the insights and chart types.
    """
    return context