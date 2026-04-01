
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import altair as alt
from PIL import Image
import time 
import random 


# Load dataset
df = pd.read_csv("project_app/victor.csv")



col1, col2 = st.tabs(["Overview", "Insights"])
with col1:
  st.title("Incidents Analysis Dashboard")

with col2:
    st.download_button("Download Data", df.to_csv().encode("utf-8"), "project_app/victor.csv")




    

st.progress(70)  
with st.spinner("Loading analysis..."):
    time.sleep(2)




# I applied custom CSS styling to set a gradient background 
# for the Streamlit app I used st.markdown with some HTML/CSS code
st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(to right, #1e3c72, #2a5298);
        }
    </style>
    """,
    unsafe_allow_html=True
)



# I configured Streamlit page layout and title, 
# I selected relevant columns from the dataframe, 
# and displayed an expandable incident table for quick review
st.set_page_config(layout="wide")
#st.title("Incidents Analysis Dashboard")
columns = ["Identifier","Incident","State","Start date","End date","Number of deaths"]
df = df[columns]
with st.expander("Click to check Incident Table", expanded=False):
    st.dataframe(df, width="stretch", height=200)



# Example: calculate total deaths
total_deaths = df["Number of deaths"].sum()

# I counted unique states
total_states = df["State"].nunique()

# I calculated total number of deaths
total_deaths = df["Number of deaths"].sum()

# I calculated total number of incidents
unique_incidents = df["Incident"].nunique()


# I created three columns for side-by-side display
col1, col2, col3 = st.columns(3)

with col1.popover("Show Total States"):
   st.write(f"{total_states} States including FCT Abuja")

with col2.popover("Show Total Deaths"):
    st.write(f"{total_deaths} Deaths Across Nigeria")

with col3.popover("Show Total Incidents"):
    st.write(f"{unique_incidents} Incidents")


# I added a sidebar to display an image (images4.jpg)
# with a fixed width of 200 pixels.
st.sidebar.title("")
img = Image.open("project_app/images4.jpg")
img = img.resize((260, 120)) # width=200, height=300   
st.sidebar.image(img)

# I used a Sidebar multiselect widget for filtering data by one or more states
states = st.sidebar.multiselect(
    "Select State(s)",
    options=sorted(df["State"].dropna().unique())
)


# I used a Sidebar date inputs for selecting start and end dates, 
# then I converted them to pandas datetime objects for filtering and analysis
start_date = st.sidebar.date_input("Start date")
end_date = st.sidebar.date_input("End date")

# I converted the start and end dates to pandas datetime
start_date = pd.to_datetime(start_date)
end_date   = pd.to_datetime(end_date)


# I used a sidebar select box for choosing a specific incident 
# with a default "Choose option" placeholder at the top
incident_options = ["Choose option"] + df['Incident'].unique().tolist()
incident_option = st.sidebar.selectbox("Choose an Incident", options=incident_options)


# I added a Sidebar section
st.sidebar.header("Feedback")
if st.sidebar.button("Submit Feedback"):
    st.toast("Thank you for your feedback! ✨")


# I converted the start and end dates to pandas datetime
df["Start date"] = pd.to_datetime(df["Start date"])
df["End date"] = pd.to_datetime(df["End date"])
filtered_df = df[(df["State"].isin(states) if states else pd.Series(True, index=df.index)) &
                 (df["Start date"] >= start_date) &
                 (df["End date"] <= end_date)]



# I applied filters
mask = pd.Series(True, index=df.index)
if states: mask &= df["State"].isin(states)
mask &= df["Start date"] >= pd.to_datetime(start_date)
mask &= df["End date"] <= pd.to_datetime(end_date)
filtered_df = df[mask]



#Q1 Which incidents are associated with the highest number of deaths?
st.subheader("Question 1:: Which Incident are associated with the highest number of deaths?")
top_titles = df.groupby("Incident")["Number of deaths"].sum().nlargest(10)

# Increase figure size for a bigger pie chart
fig6, ax6 = plt.subplots(figsize=(24, 16))  

ax6.pie(
    top_titles,
    labels=top_titles.index,
    autopct='%1.1f%%',
    startangle=90,
    textprops={'fontsize': 16}
)
ax6.set_title("Deaths by Incident (Top 10)", fontsize=22)

# Reduce bottom margin significantly so there's less empty space
fig6.subplots_adjust(bottom=0.12)   # Changed from 0.20 → 0.12

# Add summary text — moved much closer to the chart
summary_text = (
    "The top two categories — Auto Crashes and Banditry —\n"
    "together account for over half (50.5%) of all incidents, "
    "showing they dominate the landscape compared to other causes."
)

fig6.text(
    0.5, 0.04,          # Changed from -0.01 → 0.04 (positive = closer to chart)
    summary_text,
    ha='center', 
    va='bottom',        # Changed to 'bottom' so text sits nicely above the line
    fontsize=18, 
    weight='bold', 
    color='darkblue',
    bbox=dict(boxstyle="round,pad=0.6", facecolor="lightyellow", alpha=0.6)
)

st.pyplot(fig6)


#Q2 How does the number of deaths vary across different States, using top 10 states?
st.subheader("Question 2:: How does the number of deaths vary across different States, using top 10 states?")
top_states = df.groupby("State")["Number of deaths"].sum().nlargest(10).index
df_top = df[df["State"].isin(top_states)]

fig = sns.catplot(
    data=df_top, 
    x='State', 
    y='Number of deaths', 
    kind='violin',
    inner='quartile', 
    height=6, 
    aspect=1.5, 
    palette="viridis"
)

# Add stripplot on the same axes
sns.stripplot(
    data=df_top, 
    x='State', 
    y='Number of deaths', 
    color='white',
    size=3, 
    alpha=0.6, 
    ax=fig.ax
)

# Rotate x labels
fig.set_xticklabels(rotation=45, ha="right")

# Main title
fig.fig.suptitle("Distribution of Number of Deaths by Top 10 States", 
                 fontsize=16, y=1.02)

# Summary text (with nice styling like your pie chart)
summary_text = (
    "The states with the highest variability (Benue, Kaduna, Borno) experience unpredictable swings in death numbers,\n"
    "while Ogun and Lagos show more stable, consistent patterns."
)

# Adjust bottom margin to make space but keep summary close
fig.fig.subplots_adjust(bottom=0.18)

# Add styled summary text - closer to the chart (just like you wanted)
fig.fig.text(
    0.5, 0.005,                    # Changed from -0.1 → 0.02  (much closer)
    summary_text,
    ha='center', 
    va='bottom',                  # Better alignment
    fontsize=14,                  # Slightly larger than original 12
    weight='bold', 
    color='darkblue',
    bbox=dict(
        boxstyle="round,pad=0.6", 
        facecolor="lightyellow", 
        alpha=0.65
    )
)

# Display in Streamlit
st.pyplot(fig.fig)



#3 What is the monthly distribution of incidents?
st.subheader("Question 3:: What is the monthly distribution of incidents?")
df['Month'] = df['Start date'].dt.month_name()
fig, ax = plt.subplots(figsize=(14, 8))

sns.countplot(
    data=df, x='Month', palette='tab20',
    order=['January','February','March','April','May','June','July',
           'August','September','October','November','December'], ax=ax
)

# Annotate bar counts
for p in ax.patches:
    ax.annotate(f'{p.get_height()}',
                (p.get_x()+p.get_width()/2., p.get_height()),
                ha='center', va='bottom', fontsize=10, color='black',
                xytext=(0,5), textcoords='offset points')

# Titles and labels
ax.set_title('Number of Incidents by Month', fontsize=20)
ax.set_xlabel("Month", fontsize=14)
ax.set_ylabel("Number of Incidents", fontsize=14)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
sns.despine()

# Add summary text below x-axis label
summary_text = ("Incident counts fluctuate throughout the year, with noticeable peaks "
                "in January, July, and October, and dips in May, April, and November.\n"
                "Overall, the average is about 624 incidents per month, showing seasonal "
                "variation—higher in winter and summer, lower in spring.")

fig.text(0.5, -0.05, summary_text,
         ha='center', va='top', fontsize=12, color='darkblue',
         bbox=dict(boxstyle="round,pad=0.5", facecolor="lightyellow", alpha=0.5))

st.pyplot(fig)




#Q4 How does the number of deaths vary across different states?
st.subheader("Question 4:: How does the number of deaths vary across different states?")
chart = alt.Chart(df).mark_boxplot(size=50).encode(
    x=alt.X('State:N', sort='-y'),
    y='Number of deaths:Q',
    color=alt.Color('State:N', legend=None)
).properties(width=700, height=500, title='Deaths by State (Boxplot)')
st.altair_chart(chart, use_container_width=True)


#Q5 Has the frequency or severity of fatal incidents increased or decreased year-over-year?
st.subheader("Question 5:: Has the frequency or severity of fatal incidents increased or decreased year-over-year?")
line_chart = alt.Chart(df).mark_line(point=True).encode(
    x='year(Start date):O',
    y='sum(Number of deaths):Q',
    tooltip=['year(Start date)', 'sum(Number of deaths)']
).properties(width=700)
st.altair_chart(line_chart, use_container_width=True)

#Q6 Top 8 states have the highest cumulative death toll?
st.subheader("Question 6:: Which states have the highest cumulative death toll?")
state_data = df.groupby('State')['Number of deaths'].sum().nlargest(8).reset_index()
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=state_data, x='Number of deaths', y='State', palette='tab20', ax=ax)
ax.set_title("Top 8 States by Total Deaths", fontsize=16)
st.pyplot(fig)


#Q7 Which months are the "deadliest" across the historical record?
st.subheader("Question 7:: Which months are the deadliest across the historical record?")
df = df.dropna(subset=['Start date']).copy()
df['Month'] = df['Start date'].dt.month_name()
month_chart = alt.Chart(df).mark_bar().encode(
    x=alt.X('Month:N', title='Month',
            sort=['January','February','March','April','May','June','July',
                  'August','September','October','November','December']),
    y=alt.Y('sum(Number of deaths):Q', title='Total Deaths'),
    color=alt.Color('Month:N', scale=alt.Scale(scheme='category20'), legend=None),
    tooltip=['Month', 'sum(Number of deaths):Q']
).properties(title="Total Deaths by Month", width=900, height=450)
st.altair_chart(month_chart, use_container_width=True)

facts = [
    "Banditry and kidnapping are the leading causes of violence in the northwest.",
]
facts2 = [
    "Communal clashes in Benue and Plateau often last several days, making them among the longest incidents."
]

#st.info(random.choice(facts))


st.markdown("### 💡 Did You Know?")
st.info(random.choice(facts))
st.info(random.choice(facts2))

#st.success("""
   # Lagos State is divided into 20 Local Government Areas (LGAs) and 
    #57 Local Council Development Areas (LCDAs) for effective administration 
   # and development.
  #  """)


# ... my app content ...
st.divider()  # I added a horizontal rule with some HTML code
st.markdown(
    "<h3 style='text-align: center;'>Thank you for visiting! 😊</h3>",
    unsafe_allow_html=True
)
