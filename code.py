# Load packages
import pandas as pd
import numpy as np
import plotly
import chart_studio
import plotly.graph_objects as go
import math

# Upload your data as a CSV and load as a DataFrame
df = pd.read_csv("likertscalevisualization\survey_results.csv")
df

# Check that the rows add up to 100
values = df.iloc[:, 1:6].values.tolist()
for v in values:
    if not sum(v) == 100:
        raise ValueError("There is a row that does not add up to 100%.")

        # ----------------------------------------------#
# Fill out steps 1-4 to customize your diagram: #
# ----------------------------------------------#

# 1. Set title text 
title = "Post-Conference Survey Results - Feb 2022"

# 2. (Optional) Set width and height
width = 900
height = 500

# 3. (Optional) Set colors for the...
background_color = "WhiteSmoke" # Background
colors = [
    "#488f31",  # "Strongly Agree" bars
    "#b2b264",  # "Agree" bars
    "#fbdbb1",  # "Neutral" bars
    "#ea936d",  # Disagree bar
    "#de425b",  # Strongly Disagree bars
]

# 4. (Optional) Customize font settings of plot annontations
title_font = dict(family="Helvetica", size=20, color="black")
questions_font = dict(family="Helvetica", size=14, color="black")
likert_scale_font = dict(family="Helvetica", size=14, color="black")
percent_font = dict(family="Helvetica", size=16, color="#434343")

# ------------------------------------------#
# Code to create stacked bar chart begins!  #
# ------------------------------------------#

# Define Likert scale labels with formatting
labels = [
    "<b>Strongly<br>agree<b>",
    "<b>Agree<b>",
    "<b>Neutral<b>",
    "<b>Disagree<b>",
    "<b>Strongly<br>disagree<b>",
]

# Add line breaks to questions after fifth word
questions = []
qs = df.iloc[:,0].tolist()
for q in qs:
    words = q.split()
    for w in range(1, int(math.ceil((len(words) / 5)))):
        words.insert(w * 5, "<br>")
    questions.append(" ".join(words))

# The following code was taken and modified from:
# https://plotly.com/python/horizontal-bar-charts/#color-palette-for-bar-chart

# Create a Plotly Graph object
fig = go.Figure()

# Create a bar for each question and label with the correct color
for i in range(0, len(values[0])):
    for xd, yd in zip(values, questions):
        fig.add_trace(
            go.Bar(
                x=[xd[i]],
                y=[yd],
                orientation="h",
                marker=dict(color=colors[i]),
            )
        )

# Create a horizontal stacked bar chart
fig.update_layout(
    title=title,
    title_font=title_font,
    width=width, 
    height=height,
    barmode="stack",
    paper_bgcolor=background_color,
    plot_bgcolor=background_color,
    margin=dict(l=120, r=10, t=140, b=80),
    showlegend=False,
    hovermode=False,
    xaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=False,
        zeroline=False,
        domain=[0.15, 1],
    ),
    yaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=False,
        zeroline=False,
    ),
)

# Create and add annotations to plot
annotations = []
for yd, xd in zip(questions, values):
    # Label the y-axis with the questions
    annotations.append(
        dict(
            xref="paper",
            yref="y",
            x=0.14,
            y=yd,
            xanchor="right",
            text=str(yd),
            font=questions_font,
            showarrow=False,
            align="right",
        )
    )
    # Label the first percentage of the questions on the x-axis
    annotations.append(
        dict(
            xref="x",
            yref="y",
            x=xd[0] / 2,
            y=yd,
            text=str(xd[0]) + "%",
            font=percent_font,
            showarrow=False,
        )
    )
    # Label the first Likert scale on the top
    if yd == questions[-1]:
        annotations.append(
            dict(
                xref="x",
                yref="paper",
                x=xd[0] / 2,
                y=1.15,
                text=labels[0],
                font=likert_scale_font,
                showarrow=False,
            )
        )
    space = xd[0]
    for i in range(1, len(xd)):
        # Label the rest of the percentages of the questions on the x-axis
        annotations.append(
            dict(
                xref="x",
                yref="y",
                x=space + (xd[i] / 2),
                y=yd,
                text=str(xd[i]) + "%",
                font=percent_font,
                showarrow=False,
            )
        )
        # Label the rest of the Likert scale on the top
        if yd == questions[-1]:
            annotations.append(
                dict(
                    xref="x",
                    yref="paper",
                    x=space + (xd[i] / 2),
                    y=1.15,
                    text=labels[i],
                    font=likert_scale_font,
                    showarrow=False,
                )
            )
        space += xd[i]
fig.update_layout(annotations=annotations)

# Show figure
fig.show()