import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# Function to wrap and truncate text for display on chart
def truncate_label(text, max_characters=20):
    if len(text) > max_characters:
        text = text[:max_characters] + "..."  # Truncate and add "..."
    
    # Wrapping the text into lines
    words = text.split(' ')
    wrapped_text = ""
    line = ""

    for word in words:
        if len(line) + len(word) + 1 > max_characters:  # +1 for the space
            wrapped_text += line + '<br>'  # Start a new line
            line = word  # Start new line with the current word
        else:
            if line:
                line += ' ' + word
            else:
                line = word

    wrapped_text += line  # Add any remaining text
    return wrapped_text

# Custom HTML for styling
st.markdown("""
    <h1 style='font-size:40px; color:green;'>Vận trình Năng lượng</h1>
    <p style='font-size:20px; color:green;'>Copyright By Ocdaomayvacay.vn</p>
    """, unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    year_of_birth = st.number_input('Năm sinh', step=1, value=2000)
with col2:
    moon_phase_start = st.number_input('Ngày sinh âm lịch', min_value=0, max_value=30, value=7)
with col3:
    current_year = st.number_input('Năm hiện tại', step=1, value=2024)
with col4:
    num_points = st.number_input('Sự kiện (max 20)', min_value=1, max_value=20, value=10)

# The moon phase energy pattern (values from -8 to 7)
moon_phase_pattern = [-8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 
                      6, 5, 4, 3, 2, 1, 0, -1, -2, -3, -4, -5, -6, -7, -8]

# Extend the moon phase pattern for 60 years, starting from the given moon phase start
years_to_extend = 80
extended_moon_phases = []

# Cycle through the moon phase pattern for 60 years
for i in range(years_to_extend):
    phase_index = (moon_phase_start + i) % len(moon_phase_pattern)
    extended_moon_phases.append(moon_phase_pattern[phase_index])

# Map the years to the extended moon phases
years_moon = [year_of_birth + i for i in range(years_to_extend)]

years = []
energy_levels = []
original_labels = []
truncated_labels = []

# Input fields for dynamic number of data points (based on user's choice)
for i in range(1, num_points + 1):
    st.subheader(f'Mốc sự kiện {i}')
    col1, col2 = st.columns(2)
    with col1:
        year = st.number_input(f'Năm {i}', step=1, value=2000 + i)  # Default to year 2000, 2001, etc.
    with col2:
        energy = st.slider(f'Mức năng lượng {i}', min_value=-8, max_value=8, value=0)
    label = st.text_input(f'Ý nghĩa {i}', value=f'Ý nghĩa {i}')
    
    years.append(year)
    energy_levels.append(energy)
    original_labels.append(label)  # Keep the original label for DataFrame
    truncated_labels.append(truncate_label(label, max_characters=20))  # Truncate for display on chart

# Calculate sum of moon phase energy and user energy levels
combined_energy = []
for i in range(len(years)):
    # Align the years between the moon phase and user input years
    moon_index = years_moon.index(years[i]) if years[i] in years_moon else -1
    if moon_index != -1:
        combined_energy.append(extended_moon_phases[moon_index] + energy_levels[i])
    else:
        combined_energy.append(energy_levels[i])  # Default to user input energy if no moon phase found

# Create tickvals and customize the ticktext for x-axis, highlighting user input years
tickvals = years_moon
ticktext = [str(year) for year in years_moon]

# Add annotations to highlight user input years
annotations = []
for year in years:
    annotations.append(
        dict(
            x=year,
            y=-13,  # Position below the plot
            xref="x",
            yref="y",
            text=f"<b>{year}</b>",  # Bold the year
            showarrow=False,
            font=dict(size=14, color="red"),  # Customize the size and color
            xanchor='center',
            yanchor='top'
        )
    )

# Add the "You are here" annotation
annotations.append(
    dict(
        x=current_year, 
        y=8,  # Place it at the top of the y-axis range
        text="Năm hiện tại", 
        showarrow=False, 
        font=dict(size=15, color="black"),  # Black font to match the line
        xanchor='center', 
        yanchor='bottom',
        xref="x",
        yref="y"
    )
)

# Plotly chart
if st.button('Tạo sơ đồ năng lượng'):
    fig = go.Figure()

    # First line: Moon phase energy over time with a smooth curve
    fig.add_trace(go.Scatter(
        x=years_moon, 
        y=extended_moon_phases, 
        mode='lines+markers',
        name='Năng lượng Pha Trăng',
        line=dict(shape='spline', color='#ffdbaa', dash='solid', width=6),  # Smooth curved line for moon phases
        marker=dict(size=4, color='orange'),
        hoverinfo='x+y'
    ))

    # Second line: Energy levels from user input
    fig.add_trace(go.Scatter(
        x=years, 
        y=energy_levels, 
        mode='lines+markers+text',  # Adding `+text` to ensure text labels are shown
        name='Năng lượng Transit',
        line_shape='spline',  # Smooth curve for user energy levels
        hoverinfo='x+y',
        marker=dict(size=4),
        text=truncated_labels,  # Use the truncated labels for the chart
        textposition='top center',  # Position the labels on top of the points
        textfont=dict(size=10, color="black")
    ))

    # Add the sum line (in red)
    fig.add_trace(go.Scatter(
        x=years, 
        y=combined_energy, 
        mode='lines+markers',
        name='Năng Lượng tổng',
        line=dict(shape='spline', color='red', width=3),  # Smooth curved line for combined energy
        marker=dict(size=6, color='red'),
        hoverinfo='x+y'
    ))

    # Highlight background for y > 0 with light green
    fig.add_shape(
        type="rect",
        x0=min(years_moon) - 1, x1=max(years_moon) + 1, y0=0, y1=12,  # Adjusted for moon phase y range
        fillcolor="#C8DBBE",  # Light green
        line=dict(width=0),
        layer="below"
    )

    # Highlight background for y < 0 with light red (for user energy levels)
    fig.add_shape(
        type="rect",
        x0=min(years_moon) - 1, x1=max(years_moon) + 1, y0=-12, y1=0,  # Adjusted for energy levels
        fillcolor="#EDE4E0",  # Light red
        line=dict(width=0),
        layer="below"
    )

    # Add vertical line for the current year
    fig.add_shape(
        type="line",
        x0=current_year, x1=current_year, y0=-8, y1=8,  # Full vertical line across chart
        line=dict(color="black", width=1)
    )

    # Add annotations (labels) after all other elements so they appear on top
    for i, year in enumerate(years):
        fig.add_annotation(
            x=year,
            y=-12.5,  # Position the labels below the chart (slightly outside the plot)
            text=truncated_labels[i],  # Use the truncated label for chart display
            showarrow=False,
            xanchor='center',
            yanchor='top',
            font=dict(size=14, color='black')
        )

    # Add the "You are here" annotation last to ensure it's also on top
    annotations.append(
        dict(
            x=current_year, 
            y=8,  # Place it at the top of the y-axis range
            text="Năm hiện tại", 
            showarrow=False, 
            font=dict(size=15, color="black"),  # Black font to match the line
            xanchor='center', 
            yanchor='bottom',
            xref="x",
            yref="y"
        )
    )

    # Set titles and labels, include every year on the x-axis and add vertical grid lines
    fig.update_layout(
        title='Sơ đồ Năng lượng - Vận trình Cuộc đời',
        xaxis_title='Năm',
        yaxis_title='Mức Năng Lượng',
        xaxis=dict(
            range=[min(years_moon) - 1, max(years_moon) + 1],  # Include moon years range with padding
            tickmode='linear',  # Ensure every x-value (year) is displayed
            tickvals=tickvals,  # Apply custom tick values (years)
            ticktext=ticktext,  # Regular tick text
            dtick=1,  # Show every year as a tick
            showgrid=True,  # Show vertical grid lines
            gridcolor='#F4EEEE'  # Grid line color
        ),
        yaxis=dict(
            range=[-12, 12],  # Adjust for both energy levels and moon phases
            showgrid=True,  # Show horizontal grid lines
            gridcolor='#F4EEEE'  # Grid line color
        ),
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),  # Move legend to the bottom
        annotations=annotations  # Add all the annotations including user input years and "You are here"
    )

    # Show plot
    st.plotly_chart(fig)

    # Show the data as a dataframe with original labels
    df = pd.DataFrame({
        'Năm': years,
        'Năng lượng tổng': combined_energy,
        'Sự kiện': original_labels  # Show the original labels in the dataframe
    })
    st.dataframe(df, width=1000)
