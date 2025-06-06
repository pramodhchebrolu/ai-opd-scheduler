import streamlit as st
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="AI OPD Scheduler", layout="centered")

st.title("🧠 AI-Powered OPD Appointment Scheduler")

st.markdown("""
This tool uses AI clustering to suggest optimal OPD appointment times and lets you book appointments smartly.
""")

# ==========================
# Simulated historical OPD data
# ==========================
data = pd.DataFrame({
    'Hour': np.random.choice(range(9, 17), 100),
    'Day': np.random.choice(range(1, 6), 100)  # 1: Monday, 5: Friday
})

# ==========================
# KMeans Clustering
# ==========================
kmeans = KMeans(n_clusters=4, random_state=42)
kmeans.fit(data)
data['Cluster'] = kmeans.labels_

# ==========================
# Plotting the Clusters
# ==========================
st.subheader("📊 OPD Load Clustering Pattern")
fig, ax = plt.subplots()
for i in range(4):
    cluster_data = data[data['Cluster'] == i]
    ax.scatter(cluster_data['Hour'], cluster_data['Day'], label=f'Cluster {i}')
ax.set_xlabel("Hour")
ax.set_ylabel("Day (1=Mon, 5=Fri)")
ax.set_title("OPD Patient Load")
ax.legend()
st.pyplot(fig)

# ==========================
# Booking Section
# ==========================
st.subheader("📝 Book an Appointment")

# CSV file to store appointments
APPOINTMENTS_FILE = "appointments.csv"

# Load existing appointments
if os.path.exists(APPOINTMENTS_FILE):
    appointments_df = pd.read_csv(APPOINTMENTS_FILE)
else:
    appointments_df = pd.DataFrame(columns=["Name", "Day", "Hour"])

name = st.text_input("Patient Name")
hour = st.selectbox("Preferred Hour", range(9, 17))
day = st.selectbox("Preferred Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])

# Convert Day to number
day_number = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"].index(day) + 1

# Booking Button
if st.button("📅 Book Appointment"):
    if name.strip() == "":
        st.warning("Please enter patient name.")
    else:
        # Check for duplicate booking
        if ((appointments_df["Hour"] == hour) & (appointments_df["Day"] == day_number)).any():
            st.error("❌ This slot is already booked. Please choose another time.")
        else:
            # Save appointment
            new_appointment = pd.DataFrame([[name, day_number, hour]], columns=["Name", "Day", "Hour"])
            appointments_df = pd.concat([appointments_df, new_appointment], ignore_index=True)
            appointments_df.to_csv(APPOINTMENTS_FILE, index=False)
            st.success(f"✅ Appointment booked for {name} on {day} at {hour}:00")

# ==========================
# Show all appointments
# ==========================
st.subheader("📋 View Booked Appointments")

if not appointments_df.empty:
    # Convert Day number back to text
    appointments_df["Day"] = appointments_df["Day"].map({
        1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday"
    })
    st.dataframe(appointments_df)
else:
    st.info("No appointments booked yet.")
