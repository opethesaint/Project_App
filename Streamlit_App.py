
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




    

#st.progress(70)  
#with st.spinner("Loading analysis..."):
#    time.sleep(2)




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
st.sidebar.markdown(
    """ <div style="padding:25px; border-radius:10px; margin:12px; width:247px; background:#1e1e1e; color:#ffffff; ">  
        <h3 style="margin:0;">👤 User Profile</h3>
        <p style="margin:0;">Name: Rotimi</p>
        <p style="margin:0;">Role: Data Analyst</p>
    </div>
    """,
    unsafe_allow_html=True
)



#st.sidebar.title("")
#img = Image.open("project_app/images4.jpg")
#img = img.resize((260, 120)) # width=200, height=300   
#st.sidebar.image(img)

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


#Q1 Which Incident are associated with the highest number of deaths?
st.subheader("Question 1:: Which Incident are associated with the highest number of deaths?")

top_titles = df.groupby("Incident")["Number of deaths"].sum().nlargest(10)

# Create a bigger pie chart with bold labels
fig6, ax6 = plt.subplots(figsize=(28, 18))

ax6.pie(
    top_titles,
    labels=top_titles.index,
    autopct='%1.1f%%',
    startangle=90,
    textprops={'fontsize': 18, 'fontweight': 'bold'},   # Bigger and bold labels
    wedgeprops={'linewidth': 2, 'edgecolor': 'white'}    # Cleaner slice separation
)

ax6.set_title("Deaths by Incident (Top 10)", fontsize=24, fontweight='bold', pad=40)
ax6.axis('equal')  # Makes sure the pie is perfectly circular

st.pyplot(fig6)

# ====================== SUMMARY TEXT (HTML Design) ======================
summary_text = (
    "<strong>INSIGHT::</strong>&nbsp;&nbsp;&nbsp; "
    "The top two categories — Auto Crashes and Banditry — together account for over "
    "half (50.5%) of all incidents, showing they dominate compared to other causes."
)

st.markdown(f"""
<div style="text-align: center; margin-top: 0.5px; margin-bottom: 25px;">
    <div style="
        display: inline-block;
        padding: 20px 35px;
        background-color: #fff9e6;
        border-radius: 12px;
        border: 1px solid #f0d68a;
        font-size: 16px;
        line-height: 1.6;
        color: #003366;
        font-weight: bold;
        max-width: 90%;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    ">
        {summary_text}
    </div>
</div>
""", unsafe_allow_html=True)





#Q2 How does the number of deaths vary across different States, using top 10 states?
st.subheader("Question 2:: How does the number of deaths vary across different States, using top 10 states?")

top_states = df.groupby("State")["Number of deaths"].sum().nlargest(10).index
df_top = df[df["State"].isin(top_states)]

fig = sns.catplot(data=df_top, x='State', y='Number of deaths', kind='violin',
                  inner='quartile', height=6, aspect=1.5, palette="viridis")

sns.stripplot(data=df_top, x='State', y='Number of deaths', color='white',
              size=3, alpha=0.6, ax=fig.ax)

fig.set_xticklabels(rotation=45, ha="right")
fig.fig.suptitle("Distribution of Number of Deaths by Top 10 States", fontsize=16, y=1.02)

st.pyplot(fig.fig)

# ====================== SUMMARY TEXT (HTML Design - Consistent) ======================
summary_text = (
    "<strong>INSIGHT::</strong>&nbsp;&nbsp;&nbsp; The states with the highest variability (Benue, Kaduna, Borno) experience "
    "unpredictable swings in death numbers, while Ogun and Lagos show more "
    "stable, consistent patterns."
)

st.markdown(f"""
<div style="text-align: center; margin-top: 0.5px; margin-bottom: 20px;">
    <div style="
        display: inline-block;
        padding: 18px 30px;
        background-color: #fff9e6;
        border-radius: 12px;
        border: 1px solid #f0d68a;
        font-size: 15px;
        line-height: 1.55;
        color: #003366;
        font-weight: bold;
        max-width: 88%;
        box-shadow: 0 3px 12px rgba(0,0,0,0.08);
    ">
        {summary_text}
    </div>
</div>
""", unsafe_allow_html=True)




#3 What is the monthly distribution of incidents?
st.subheader("Question 3:: What is the monthly distribution of incidents?")

df['Month'] = df['Start date'].dt.month_name()

fig, ax = plt.subplots(figsize=(14, 8))
sns.countplot(data=df, x='Month', palette='tab20',
              order=['January','February','March','April','May','June','July',
                     'August','September','October','November','December'], ax=ax)

# Annotate bar counts
for p in ax.patches:
    ax.annotate(f'{p.get_height()}', 
                (p.get_x() + p.get_width()/2., p.get_height()),
                ha='center', va='bottom', 
                fontsize=10, color='black', 
                xytext=(0,5), textcoords='offset points')

ax.set_title('Number of Incidents by Month', fontsize=20, fontweight='bold', color='darkblue')
ax.set_xlabel("Month", fontsize=14)
ax.set_ylabel("Number of Incidents", fontsize=14)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
sns.despine()

st.pyplot(fig)

# ====================== SUMMARY TEXT (HTML Design - Consistent) ======================
summary_text = (
    "<strong>INSIGHT::</strong>&nbsp;&nbsp;&nbsp; Incident counts fluctuate throughout the year, with noticeable peaks in January."
    "July, and October, and dips in May, April, and November. "
    "Overall, the average is about 624 incidents per month.")

st.markdown(f"""
<div style="text-align: center; margin-top: 0.5px; margin-bottom: 20px;">
    <div style="
        display: inline-block;
        padding: 18px 30px;
        background-color: #fff9e6;
        border-radius: 12px;
        border: 1px solid #f0d68a;
        font-size: 15px;
        line-height: 1.55;
        color: #003366;
        font-weight: bold;
        max-width: 88%;
        box-shadow: 0 3px 12px rgba(0,0,0,0.08);
    ">
        {summary_text}
    </div>
</div>
""", unsafe_allow_html=True)





# Q4: How does the number of deaths vary across different states?
st.subheader("Question 4:: How does the number of deaths vary across different states?")

chart = alt.Chart(df).mark_boxplot(size=50).encode(
    x=alt.X('State:N', sort='-y'),
    y='Number of deaths:Q',
    color=alt.Color('State:N', legend=None)
).properties(
    width=700, 
    height=500, 
    title='Deaths by State (Boxplot)'
)

st.altair_chart(chart, use_container_width=True)

# ====================== SUMMARY TEXT (HTML Design - Consistent) ======================
summary_text = (
    "<strong>INSIGHT::</strong>&nbsp;&nbsp;&nbsp; Borno and Zamfara stand out with both higher median deaths and wider variability, "
    "while Abuja, Imo, and Lagos show relatively stable and lower death counts."
)

st.markdown(f"""
<div style="text-align: center; margin-top: 0.5px; margin-bottom: 20px;">
    <div style="
        display: inline-block;
        padding: 18px 30px;
        background-color: #fff9e6;
        border-radius: 12px;
        border: 1px solid #f0d68a;
        font-size: 15px;
        line-height: 1.55;
        color: #003366;
        font-weight: bold;
        max-width: 88%;
        box-shadow: 0 3px 12px rgba(0,0,0,0.08);
    ">
        {summary_text}
    </div>
</div>
""", unsafe_allow_html=True)



# Q5: Has the frequency or severity of fatal incidents increased or decreased year-over-year?
st.subheader("Question 5:: Has the frequency or severity of fatal incidents increased or decreased year-over-year?")

line_chart = alt.Chart(df).mark_line(point=True).encode(
    x='year(Start date):O',
    y='sum(Number of deaths):Q',
    tooltip=['year(Start date)', 'sum(Number of deaths)']
).properties(
    width=700, 
    height=500,
    title='Total Deaths by Year (Trend)'
)

st.altair_chart(line_chart, use_container_width=True)

# ====================== SUMMARY TEXT (Closer to the chart) ======================
summary_text = (
    "<strong>INSIGHT::</strong>&nbsp;&nbsp;&nbsp; From 1970 to 2022, there’s a sharp rise, reaching about 8,000 deaths. "
    "The numbers continue climbing in 2023 and 2024, peaking at around 12,000 deaths. "
   
)

# Closer version - reduced top margin
st.markdown(f"""
<div style="text-align: center; margin-top: 0.5px; margin-bottom: 20px;">
    <div style="
        display: inline-block;
        padding: 16px 28px;
        background-color: #fff9e6;
        border-radius: 12px;
        border: 1px solid #f0d68a;
        font-size: 15px;
        line-height: 1.55;
        color: #003366;
        font-weight: bold;
        max-width: 88%;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    ">
        {summary_text}
    </div>
</div>
""", unsafe_allow_html=True)


# Q6: Top 8 states have the highest cumulative death toll?
st.subheader("Question 6:: Which states have the highest cumulative death toll?")

state_data = df.groupby('State')['Number of deaths'].sum().nlargest(8).reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=state_data, x='Number of deaths', y='State', palette='tab20', ax=ax)
ax.set_title("Top 8 States by Total Deaths", fontsize=16)

# Optional improvements
ax.set_xlabel("Total Number of Deaths", fontsize=12)
ax.set_ylabel("State", fontsize=12)

st.pyplot(fig)

# ====================== SUMMARY TEXT (HTML Design - Consistent) ======================
summary_text = (
    "<strong>INSIGHT::</strong>&nbsp;&nbsp;&nbsp; The key takeaway is that Borno stands out with a dramatically higher death toll "
    "compared to the rest, while Lagos records the lowest."
)

st.markdown(f"""
<div style="text-align: center; margin-top: 0.5px; margin-bottom: 20px;">
    <div style="
        display: inline-block;
        padding: 18px 30px;
        background-color: #fff9e6;
        border-radius: 12px;
        border: 1px solid #f0d68a;
        font-size: 15px;
        line-height: 1.55;
        color: #003366;
        font-weight: bold;
        max-width: 88%;
        box-shadow: 0 3px 12px rgba(0,0,0,0.08);
    ">
        {summary_text}
    </div>
</div>
""", unsafe_allow_html=True)


# Q7: Which months are the "deadliest" across the historical record?
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
).properties(
    title="Total Deaths by Month", 
    width=900, 
    height=450
)

st.altair_chart(month_chart, use_container_width=True)

# ====================== SUMMARY TEXT (HTML Design - Consistent) ======================
summary_text = (
    "<strong>INSIGHT::</strong>&nbsp;&nbsp;&nbsp; Mortality is strongly seasonal, with a sharp spike in January and a dip in June, "
    "while the rest of the year remains relatively steady."
)

st.markdown(f"""
<div style="text-align: center; margin-top: 12px; margin-bottom: 20px;">
    <div style="
        display: inline-block;
        padding: 18px 30px;
        background-color: #fff9e6;
        border-radius: 12px;
        border: 1px solid #f0d68a;
        font-size: 15px;
        line-height: 1.55;
        color: #003366;
        font-weight: bold;
        max-width: 88%;
        box-shadow: 0 3px 12px rgba(0,0,0,0.08);
    ">
        {summary_text}
    </div>
</div>
""", unsafe_allow_html=True)



#st.info(random.choice(facts))

st.markdown("### 💡 Did You Know?")

st.success("""
- Over 7.3 million Nigerians require humanitarian assistance in 2026.
- In the northeast (Borno, Adamawa, Yobe), 5.9 million people face severe to extreme needs due to conflict, displacement, and food insecurity.
- Non-state armed groups (NSAGs) have intensified attacks on both military and civilians.
""")




# ... my app content ...
st.divider()  # I added a horizontal rule with some HTML code
st.markdown(
    "<h3 style='text-align: center;'>Thank you for visiting! 😊</h3>",
    unsafe_allow_html=True
)



##### LAST WORK

import streamlit as st

# This always works in any Streamlit environment
st.markdown("""
    <div style="position: fixed; bottom: 50px; right: 20px;">
        <a href="https://wa.me/message/J37UJJHFVN2WO1" target="_blank" 
           style="background: #25D366; color: white; padding: 12px 20px; 
                  border-radius: 50px; text-decoration: none; font-weight: bold;">
            💬 WhatsApp Chat
        </a>
    </div>
""", unsafe_allow_html=True)









##
#### feedback form
st.text_area("💬 Leave your feedback here:")
if st.button("Submit Feedback"):
    st.success("Thanks for your feedback!")


#####
st.markdown(
    """
    <div style="text-align:center; margin-top:20px;">
        <a href="https://twitter.com" target="_blank">🐦 Twitter</a> |
        <a href="https://linkedin.com" target="_blank">💼 LinkedIn</a> |
        <a href="https://github.com" target="_blank">💻 GitHub</a>
    </div>
    """,
    unsafe_allow_html=True
)




