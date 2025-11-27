Interactive Data Dashboard — README.md
Overview

An interactive, AI-powered analytics dashboard built using Dash, Plotly, and Dash Mantine Components.
Users can upload any dataset (CSV/Excel), automatically generate visualizations, explore drill-down analytics, and get AI-generated chart insights with Text-to-Speech (TTS).

The system includes caching, a chart editor, and click-based data exploration for a complete data-analysis workflow.

✨ Features
🔹 1. Upload & Explore Datasets

Upload CSV/Excel files and instantly visualize data with automatically generated charts.

🔹 2. Auto Chart Generator

The app inspects column types and chooses suitable visualizations such as:

Bar charts

Line charts

Pie charts

Histograms

Scatter plots

🔹 3. Drill-Down Analytics

Every chart is clickable:

Click any bar, point, or category

A modal opens showing filtered data for that clicked item

Includes a mini auto-generated chart for the subset

🔹 4. Chart Insights (AI-Generated)

Each chart comes with automatically generated insights powered by an LLM.
Examples:

Trend summaries

Outlier detection

Category comparisons

Data patterns

🔹 5. Text-to-Speech (TTS) Support

Every insight can be read aloud using built-in TTS.
Perfect for accessibility and presentations.

🔹 6. Response Caching

LLM responses are cached using:

diskcache

Hash-based keys for prompt+data
This makes insights fast and avoids unnecessary API calls.

🔹 7. Chart Editor (Dash Chart Editor)

Users can customize charts with:

Axis settings

Encodings

Styles

Chart types

🔹 8. Clean, Responsive UI

Powered by Dash Mantine Components with a modern layout and smooth user experience.

🛠️ Tech Stack
Component	Technology
Frontend	Dash + Dash Mantine Components
Charts	Plotly, Dash Chart Editor
AI Insights	Gemini / OpenAI models
Caching	Diskcache
TTS	Built-in browser TTS
Data	Pandas
