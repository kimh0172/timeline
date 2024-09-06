import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# Function to wrap text at a certain width
def wrap_label(text, max_characters=20):
    words = text.split(' ')
    wrapped_text = ""
    line = ""

    for word in words:
        if len(line) + len(word) + 1 > max_characters:  # +1 for the space
            wrapped_text += line + '<br>'  # Start new line
            line = word  # Start new line with current word
        else:
            if line:
                line += ' ' + word
            else:
                line = word

    wrapped_text += line  # Add any remaining text
    return wrapped_text

# Streamlit App
st.title('Time Series Chart: Energy Levels (Curve) with Highlighted Regions and Current Year Line')

# Allow the user to specify how many data points to enter (up to 20)
num_points = st.slider('Select the number of data points (max 20)', min_value=1, max_value=20, value=10)

# Placeholder for data
years = []
energy_levels = []
labels = []

# Input fields for dynamic number of data points (based on user's choice)
for i in range(1, num_points + 1):
    st.header(f'Data Point {i}')
    year = st.number_input(f'Year {i}', step=1, value=2000 + i)  # Default to year 2000, 2001, etc.
    energy = st.slider(f'Energy Level {i}', min_value=-10, max_value=10, value=0)
    label = st.text_input(f'Label {i}', value=f'Label {i}')
    
    # Append inputs to lists
    years.append(year)
    energy_levels.append(energy)
    
    # Wrap labels at 50% width, assuming around 20 characters as 50% width for each label
    labels.append(wrap_label(label, max_characters=20))

# Input for the current year to draw a vertical line
current_year = st.number_input('Enter the current year', step=1, value=2024)

# Calculate x-axis range with 10 years padding before and after
x_min = min(years) - 10
x_max = max(years) + 10

# Plotly time series curve chart
if st.button('Generate Time Series Chart'):
    fig = go.Figure()

    # Add smooth curve plot with labels displayed on points
    fig.add_trace(go.Scatter(
        x=years, 
        y=energy_levels, 
        mode='lines+markers+text', 
        line_shape='spline',  # Smooth the line into a curve
        text=labels,  # Display labels with wrapped text
        textposition='bottom center',  # Position labels at bottom center
        hoverinfo='text+y', 
        marker=dict(size=10),
        textfont=dict(size=10, color="black"),  # Set font size and text color to black
        texttemplate='%{text}',  # Ensures text is shown as intended
    ))

    # Highlight background for y > 0 with light green
    fig.add_shape(
        type="rect",
        x0=x_min, x1=x_max, y0=0, y1=15,  # Define the rectangle for y > 0
        fillcolor="rgba(144,238,144,0.3)",  # Light green color with 30% opacity
        line=dict(width=0),  # No border for the rectangle
        layer="below"  # Make sure it is behind the plot
    )

    # Highlight background for y < 0 with light red
    fig.add_shape(
        type="rect",
        x0=x_min, x1=x_max, y0=-15, y1=0,  # Define the rectangle for y < 0
        fillcolor="rgba(255,99,71,0.3)",  # Light red color with 30% opacity
        line=dict(width=0),  # No border for the rectangle
        layer="below"  # Make sure it is behind the plot
    )

    # Add vertical line for the current year
    fig.add_shape(
        type="line",
        x0=current_year, x1=current_year, y0=-15, y1=15,  # Full vertical line across the chart
        line=dict(color="red", width=2),  # Red vertical line
    )

    # Add annotation "You are here" at the top of the vertical line
    fig.add_annotation(
        x=current_year, 
        y=15,  # Place it at the top of the y-axis range
        text="You are here", 
        showarrow=False, 
        font=dict(size=15, color="red"),  # Red font to match the line
        xanchor='center', 
        yanchor='bottom'  # Ensure the text is just above the line
    )

    # Set titles and labels
    fig.update_layout(
        title='Energy Levels Over Time (Curve) with Highlighted Regions and Current Year Line',
        xaxis_title='Year',
        yaxis_title='Energy Level',
        xaxis=dict(range=[x_min, x_max]),  # Add 10 years before and after the data range
        yaxis=dict(range=[-15, 15]),  # Set y-axis range slightly larger than -10 to 10 to avoid cutting off points
    )

    # Show plot
    st.plotly_chart(fig)

    # Show the data as a dataframe
    df = pd.DataFrame({
        'Year': years,
        'Energy Level': energy_levels,
        'Label': [label.replace('<br>', ' ') for label in labels]  # Replace <br> with space for display
    })
    st.dataframe(df)
