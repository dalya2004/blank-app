import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data
df = pd.read_csv("inddata.csv")

# Show the page title
st.header("📊 Department for Transport: School Travel Insights (2019)")
st.caption("Explore how students travel to school across different regions and schools.")

school_names = df['School Name'].dropna().unique()
selected_school = st.selectbox("Select a School", sorted(school_names))

filtered_df = df[df['School Name'] == selected_school]

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
