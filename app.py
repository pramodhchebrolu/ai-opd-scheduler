import streamlit as st
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

st.title("AI-Powered OPD Appointment Scheduler")

st.markdown("""
This tool uses clustering to suggest optimal OPD appointment times based on patient load patterns.
""")

# Simulated historical OPD data
data = pd.DataFrame({
    'Hour': np.random.choice(range(9, 17), 100),
    'Day': np.random.choice(range(1, 6), 100)  # 1: Monday, 5: Friday
})

# Clustering
kmeans = KMeans(n_clusters=4, random_state=42)
kmeans.fit(data)
data['Cluster'] = kmeans.labels_

# Show cluster chart
fig, ax = plt.subplots()
for i in range(4):
    cluster_data = data[data['Cluster'] == i]
    ax.scatter(cluster_data['Hour'], cluster_data['Day'], label=f'Cluster {i}')
ax.set_xlabel("Hour")
ax.set_ylabel("Day")
ax.set_title("OPD Appointment Clustering")
ax.legend()
st.pyplot(fig)

# Booking simulator
st.subheader("Book an Appointment")
name = st.text_input("Patient Name")
hour = st.selectbox("Preferred Hour", range(9, 17))
day = st.selectbox("Preferred Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])

if st.button("Book Appointment"):
    st.success(f"Appointment booked for {name} on {day} at {hour}:00")