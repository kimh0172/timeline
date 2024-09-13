import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# Define a password for the app
PASSWORD = "2024"

# Create a password input field
password = st.text_input("Enter Password:", type="password")

# Check if the password is correct
if password != PASSWORD:
    st.error("Incorrect password. Please try again.")
else:
    # Proceed with the rest of the app only if the password is correct
    
    # Function to wrap and truncate text for display on chart
    def wrap_text_for_plotly(text, max_characters_per_line=10):
        words = text.split(' ')
        wrapped_text = ""
        line = ""
    
        for word in words:
            if len(line) + len(word) + 1 > max_characters_per_line:  # +1 for the space
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
        <h1 style='font-size:40px; color:green;'>Vận trình năng lượng</h1>
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
    moon_phase_pattern = [-7.5, -6.5, -5.5, -4.5, -3.5, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 
                          6.5, 5.5, 4.5, 3.5, 2.5, 1.5, 0.5, -0.5, -1.5, -2.5, -3.5, -4.5, -5.5, -6.5]
    
    # Extend the moon phase pattern for 80 years, starting from the given moon phase start
    years_to_extend = 80
    extended_moon_phases = []
    
    # Cycle through the moon phase pattern for 80 years
    for i in range(years_to_extend):
        phase_index = (moon_phase_start + i) % len(moon_phase_pattern)
        extended_moon_phases.append(moon_phase_pattern[phase_index])
    
    # Map the years to the extended moon phases
    years_moon = [year_of_birth + i for i in range(years_to_extend)]
    
    years = []
    months = []
    energy_levels = []
    original_labels = []
    truncated_labels = []

    # Option for user to upload an Excel file
    st.write("Bạn có thể tải lên tệp Excel hoặc nhập thủ công:")
    st.write("Tham khảo format tại link: https://docs.google.com/spreadsheets/d/1iNvnAH-oCojCng_Uu-VhH0cdlSTyYsqLr51oqMxo6xo/edit?usp=sharing")
    uploaded_file = st.file_uploader("Chọn file Excel để nhập liệu (tùy chọn)", type="xlsx")
    
    if uploaded_file:
        # Read the Excel file into a DataFrame
        df = pd.read_excel(uploaded_file)
        
        # Validate the structure of the uploaded data
        if not all(col in df.columns for col in ["Năm", "Tháng", "Mức Năng Lượng", "Ý Nghĩa"]):
            st.error("File Excel phải chứa các cột: Năm, Tháng, Mức Năng Lượng, Ý Nghĩa")
        else:
            years = df['Năm'].tolist()
            months = df['Tháng'].tolist()
            energy_levels = df['Mức Năng Lượng'].tolist()
            original_labels = df['Ý Nghĩa'].tolist()
            truncated_labels = [wrap_text_for_plotly(label, max_characters_per_line=10) for label in original_labels]
            st.success("Dữ liệu từ Excel đã được tải lên thành công!")
    else:
    
        # Input fields for dynamic number of data points (based on user's choice)
        for i in range(1, num_points + 1):
            st.subheader(f'Mốc sự kiện {i}')
            col1, col2, col3 = st.columns(3)
            
            with col1:
                year = st.number_input(f'Năm {i}', step=1, value=2000 + i)  # Default to year 2000, 2001, etc.
            with col2:
                month = st.selectbox(f'Tháng {i} (có thể bỏ qua)', options=["N/A"] + list(range(1, 13)), index=0)  # Month dropdown (1-12) with "N/A"
            with col3:
                energy = st.slider(f'Mức năng lượng {i}', min_value=-8, max_value=8, value=0)
                
            label = st.text_input(f'Ý nghĩa {i}', value=f'Ý nghĩa {i}')
            
            years.append(year)
            
            # If "N/A" is selected for the month, append None or a placeholder
            if month == "N/A":
                months.append(None)  # You can use None or any placeholder like 0
            else:
                months.append(month)
            
            energy_levels.append(energy)
            original_labels.append(label)
            truncated_labels.append(wrap_text_for_plotly(label, max_characters_per_line=10))
    
    # Calculate sum of moon phase energy and user energy levels
    combined_energy = []
    for i in range(len(years)):
        moon_index = years_moon.index(years[i]) if years[i] in years_moon else -1
        if moon_index != -1:
            combined_energy.append(extended_moon_phases[moon_index] + energy_levels[i])
        else:
            combined_energy.append(energy_levels[i])
    
    # Rearrange data points (if desired by user)
    st.subheader('Cấu hình sơ đồ năng lượng')
    rearranged_years = st.multiselect("Chọn lại thứ tự các năm:", years, default=years)
    
    # Rearranged labels, energy, and months based on new years order
    rearranged_labels = [original_labels[years.index(year)] for year in rearranged_years]
    rearranged_energy = [energy_levels[years.index(year)] for year in rearranged_years]
    rearranged_months = [months[years.index(year)] for year in rearranged_years]
    
    # Correct combined energy for rearranged years
    rearranged_combined_energy = []
    for year in rearranged_years:
        moon_index = years_moon.index(year) if year in years_moon else -1
        energy_idx = rearranged_years.index(year)
        if moon_index != -1:
            rearranged_combined_energy.append(extended_moon_phases[moon_index] + rearranged_energy[energy_idx])
        else:
            rearranged_combined_energy.append(rearranged_energy[energy_idx])
    
    # Create a list of unique labels for the chart (only display the first label for a year on the chart)
    unique_year_labels = {}
    for year, label in zip(rearranged_years, rearranged_labels):
        if year not in unique_year_labels:
            unique_year_labels[year] = label  # Store the first occurrence of the label for a year
    
    # Create a list of unique labels, ensuring labels appear only once for annotations
    annotation_labels = [wrap_text_for_plotly(unique_year_labels.get(year, ""), max_characters_per_line=10) for year in rearranged_years]
    
    # Input fields for selecting start and end year for the view
    st.write('Chọn khoảng thời gian hiển thị')
    col1, col2, col3 = st.columns(3)
    with col1:
        start_year = st.number_input('Năm bắt đầu', min_value=min(years_moon), max_value=max(years_moon), value=min(years_moon))
    with col2:
        end_year = st.number_input('Năm kết thúc', min_value=min(years_moon), max_value=max(years_moon), value=max(years_moon))
    with col3:
        # Option to switch between the two views
        view_option = st.selectbox("Chọn view timeline:", ["Từng năm", "Mỗi 3 năm", "Năm nổi bật"])
    
    # Filter the data based on the selected year range
    filtered_years_moon = [year for year in years_moon if start_year <= year <= end_year]
    filtered_extended_moon_phases = [extended_moon_phases[years_moon.index(year)] for year in filtered_years_moon]
    filtered_rearranged_years = [year for year in rearranged_years if start_year <= year <= end_year]
    filtered_combined_energy = [rearranged_combined_energy[rearranged_years.index(year)] for year in filtered_rearranged_years]
    filtered_rearranged_energy = [rearranged_energy[rearranged_years.index(year)] for year in filtered_rearranged_years]
    filtered_annotation_labels = [annotation_labels[rearranged_years.index(year)] for year in filtered_rearranged_years]
    
    
    # Plotly chart
    if st.button('Tạo sơ đồ năng lượng'):
        fig = go.Figure()
    
        # Add moon phase energy line
        fig.add_trace(go.Scatter(
            x=filtered_years_moon, 
            y=filtered_extended_moon_phases, 
            mode='lines+markers',
            name='Năng lượng pha trăng',
            line=dict(shape='spline', color='#ffdbaa', dash='solid', width=6),
            marker=dict(size=4, color='orange'),
            hoverinfo='x+y'
        ))
    
        # Add combined energy line
        fig.add_trace(go.Scatter(
            x=filtered_rearranged_years, 
            y=filtered_combined_energy, 
            mode='lines+markers',
            name='Năng lượng tổng',
            line=dict(shape='spline', color='darkgrey', width=3),
            marker=dict(size=6, color='darkgrey'),
            hoverinfo='x+y'
        ))
    
        # Add user energy line with unique labels in annotations
        fig.add_trace(go.Scatter(
            x=filtered_rearranged_years, 
            y=filtered_rearranged_energy, 
            mode='lines+markers+text',
            name='Năng lượng Transit',
            line=dict(shape='spline', color='#98fb98', width=3),
            hoverinfo='x+y',
            marker=dict(size=6, color='lightgreen'),
            text=[f"{year}<br>{label}" for year, label in zip(filtered_rearranged_years, filtered_annotation_labels)],
            textposition='top center',
            textfont=dict(size=10, color="black")
        ))
    
        # Highlight background for y > 0 with light green
        fig.add_shape(
            type="rect",
            x0=min(filtered_years_moon) - 1, x1=max(filtered_years_moon) + 1, y0=0, y1=16,
            fillcolor="#C8DBBE",
            line=dict(width=0),
            layer="below"
        )
    
        # Highlight background for y < 0 with light red (for user energy levels)
        fig.add_shape(
            type="rect",
            x0=min(filtered_years_moon) - 1, x1=max(filtered_years_moon) + 1, y0=-16, y1=0,
            fillcolor="#EDE4E0",
            line=dict(width=0),
            layer="below"
        )
    
        # Add vertical line for the current year
        fig.add_shape(
            type="line",
            x0=current_year, x1=current_year, y0=-16, y1=16,
            line=dict(color="red", width=0.5)
        )
    
        # Add horizontal lines at y = -4 and y = 3
        fig.add_shape(
            type="line",
            x0=min(filtered_years_moon) - 1, x1=max(filtered_years_moon) + 1, y0=-3.75, y1=-3.75,
            line=dict(color="orange", width=1, dash="dash"),
            layer="below"
        )
    
        fig.add_shape(
            type="line",
            x0=min(filtered_years_moon) - 1, x1=max(filtered_years_moon) + 1, y0=3.75, y1=3.75,
            line=dict(color="orange", width=1, dash="dash"),
            layer="below"
        )
    
        # Add the "You are here" annotation
        fig.add_annotation(
            x=current_year,
            y=16,
            text="Năm hiện tại",
            showarrow=False,
            font=dict(size=12, color="black"),
            xanchor='center',
            yanchor='bottom'
        )
    
        # Set titles and labels based on the selected view option
        if view_option == "Từng năm":
            fig.update_layout(
                title='Sơ đồ Năng lượng - Vận trình Cuộc đời',
                xaxis_title='Năm',
                yaxis_title='Mức Năng Lượng',
                height=600,
                xaxis=dict(
                    dtick=1,  # Show every year
                    showgrid=True,
                    gridcolor='#F4EEEE'
                ),
                yaxis=dict(
                    range=[-16, 16],
                    showgrid=True,
                    gridcolor='#F4EEEE'
                ),
                legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
            )
        elif view_option == "Mỗi 3 năm":
            fig.update_layout(
                title='Sơ đồ Năng lượng - Vận trình Cuộc đời',
                xaxis_title='Năm',
                yaxis_title='Mức Năng Lượng',
                height=600,
                xaxis=dict(
                    dtick=3,  # Show every 3 years
                    showgrid=True,
                    gridcolor='#F4EEEE'
                ),
                yaxis=dict(
                    range=[-16, 16],
                    showgrid=True,
                    gridcolor='#F4EEEE'
                ),
                legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
            )
        else:
            fig.update_layout(
                title='Sơ đồ Năng lượng - Vận trình Cuộc đời',
                xaxis_title='Năm',
                yaxis_title='Mức Năng Lượng',
                height=600,
                xaxis=dict(
                    tickvals=filtered_rearranged_years,  # Only show rearranged years
                    ticktext=[str(year) for year in filtered_rearranged_years],
                    showgrid=True,
                    gridcolor='#F4EEEE'
                ),
                yaxis=dict(
                    range=[-16, 16],
                    showgrid=True,
                    gridcolor='#F4EEEE'
                ),
                legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
            )
    
        # Show plot
        st.plotly_chart(fig, use_container_width=True)
    
        # Show the dataframe with all years, months, and labels (including duplicates for the same year)
        df = pd.DataFrame({
            'Tháng & Năm': [f'Tháng {month}, {year}' if month is not None else f'Năm {year}' for month, year in zip(months, years)],
            'Năng lượng tổng': combined_energy,
            'Sự kiện': original_labels  # Show all labels in dataframe
        })
        st.dataframe(df, width=800)
