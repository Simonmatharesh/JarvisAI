# Interactive Data Dashboard

## Overview
An interactive, AI-powered analytics dashboard built using **Dash**, **Plotly**, and **Dash Mantine Components**.  
Users can upload datasets (CSV/Excel), automatically generate visualizations, explore drill-down analytics, and receive **AI-generated chart insights with Text-to-Speech (TTS)**.

The system also includes **caching**, a **chart editor**, and **click-based data exploration** for a complete data-analysis workflow.

---

## Features

### 🔹 1. Upload & Explore Datasets
Upload CSV/Excel files and instantly visualize data with automatically generated charts.

### 🔹 2. Automatic Chart Generator
The app detects column types and selects suitable chart types like:
- Bar charts  
- Line charts  
- Pie charts  
- Histograms  
- Scatter plots  

### 🔹 3. Drill-Down Analytics
Every chart is interactive and clickable:
- Click any bar, point, or category  
- A modal opens showing filtered data for that specific value  
- Includes an automatically generated mini-chart of the subset  

### 🔹 4. AI-Generated Chart Insights
Each chart comes with insights powered by LLMs (Gemini / OpenAI).  
Examples include:
- Trend summaries  
- Outlier detection  
- Category comparisons  
- Data pattern explanations  

### 🔹 5. Text-to-Speech (TTS)
All insights can be read aloud using built-in browser TTS — ideal for accessibility and presentations.

### 🔹 6. Response Caching
LLM insight responses are cached using:
- **diskcache**
- **Hash-based keys** (prompt + dataset)

This makes repeated insights fast and reduces API calls.

### 🔹 7. Built-In Chart Editor
Using **Dash Chart Editor**, users can customize:
- Axis settings  
- Encodings  
- Styles  
- Chart types  

### 🔹 8. Clean & Responsive UI
Styled using **Dash Mantine Components** for a modern, responsive experience.

---

## Tech Stack

| Component  | Technology |
|-----------|------------|
| Frontend  | Dash + Dash Mantine Components |
| Charts    | Plotly, Dash Chart Editor |
| AI Insights | Gemini / OpenAI |
| Caching   | Diskcache |
| TTS       | Web Speech API (browser TTS) |
| Data      | Pandas |

---



