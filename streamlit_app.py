import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data
df = pd.read_csv("inddata.csv")

# Show the page title
st.header("📊 School Travel Insights")
st.subheader(" Explore How Students Travel Across the UK")
st.caption("Explore how students travel to school across different regions and schools.")

school_names = df['School Name'].dropna().unique()
selected_school = st.selectbox("Select a School", sorted(school_names))

filtered_df = df[df['School Name'] == selected_school]

# transport columns
travel_columns = [
    'Bus (type not known)', 'Car Share', 'Car/Van', 'Cycle',
    'Dedicated School Bus', 'Public Bus Service', 'Taxi', 'Train', 'Walk'
]

# Show the data
if not filtered_df.empty:
    travel_counts = filtered_df[travel_columns].iloc[0].dropna()
    total_students = int(travel_counts.sum())

    if not travel_counts.empty:
        top_mode = travel_counts.idxmax()
        top_value = int(travel_counts.max())

        # displaying two side-by-side metric boxes
        col1, col2 = st.columns(2)
        col1.metric("Total Students", f"{total_students}")
        col2.metric("Top Transport Mode", f"{top_mode}", f"{top_value} students")
    else:
        st.warning("No transport data available for this school.")
else:
    st.warning("Selected school not found.")

# different types of travel in the dataset 
travel_columns = [
    'Bus (type not known)', 'Car Share', 'Car/Van', 'Cycle',
    'Dedicated School Bus', 'Public Bus Service', 'Taxi', 'Train', 'Walk'
]

# Extract values for the selected school
if not filtered_df.empty:
    travel_counts = filtered_df[travel_columns].iloc[0].dropna()

    if not travel_counts.empty:
        top_mode = travel_counts.idxmax()
        top_value = int(travel_counts.max())
        st.success(f" Top mode of transport for {selected_school}: **{top_mode}** with **{top_value}** students")
    else:
        st.warning("No transport data available for this school.")
else:
    st.warning("Selected school not found.")

st.subheader(f"Travel Data for {selected_school}")
st.write(filtered_df)


chart_type = st.radio("Select chart type:", ['Bar Chart', 'Pie Chart'])
travel_columns = [
    'Bus (type not known)', 'Car Share', 'Car/Van', 'Cycle',
    'Dedicated School Bus', 'Public Bus', 'Taxi', 'Train', 'Walk'
]

existing_columns = [col for col in travel_columns if col in filtered_df.columns]

if existing_columns:
    travel_counts = filtered_df[existing_columns].sum().sort_values(ascending=False)

    if chart_type == "Bar Chart":
        st.subheader("Student Travel - Bar Chart")
        st.bar_chart(travel_counts)

    elif chart_type == "Pie Chart":
        st.subheader("Student Travel - Pie Chart")

        # Calculate percentages
        total = travel_counts.sum()
        percentages = (travel_counts / total) * 100

        # Keep main categories > 2%
        main_slices = travel_counts[percentages > 2]
        other = travel_counts[percentages <= 2].sum()

        if other > 0:
            main_slices["Other"] = other

        if len(main_slices) < 2:
            st.warning("Not enough data to display a pie chart. Try another school.")
        else:
            fig, ax = plt.subplots()
            ax.pie(
                main_slices,
                labels=main_slices.index,
                autopct='%1.1f%%',
                startangle=90,
                textprops={'fontsize': 10},
                labeldistance=1.1,         # Push labels out
                pctdistance=0.7,           # Pull %s in a bit
                wedgeprops={'width': 0.95} # Slice spacing
            )
            ax.axis('equal')
            st.pyplot(fig)
