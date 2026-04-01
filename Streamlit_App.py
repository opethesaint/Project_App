
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
    0.5, 0.0001,                    # Changed from -0.1 → 0.02  (much closer)
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
    data=df, 
    x='Month', 
    palette='tab20',
    order=['January','February','March','April','May','June','July',
           'August','September','October','November','December'], 
    ax=ax
)

# Annotate bar counts
for p in ax.patches:
    ax.annotate(f'{p.get_height():,.0f}',
                (p.get_x() + p.get_width()/2., p.get_height()),
                ha='center', va='bottom', 
                fontsize=11, color='black',
                xytext=(0, 6), textcoords='offset points')

# Titles and labels
ax.set_title('Number of Incidents by Month', fontsize=20, pad=20)
ax.set_xlabel("Month", fontsize=14)
ax.set_ylabel("Number of Incidents", fontsize=14)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

sns.despine()

# ====================== SUMMARY TEXT (Styled like your pie chart) ======================
summary_text = (
    "Incident counts fluctuate throughout the year, with noticeable peaks in "
    "January, July, and October, and dips in May, April, and November.\n"
    "Overall, the average is about 624 incidents per month, showing seasonal "
    "variation — higher in winter and summer, lower in spring."
)

# Make it look consistent with your previous summary
fig.subplots_adjust(bottom=0.28)   # Gives enough space below the chart

fig.text(
    0.5, -0.12,                    # Adjusted position (more negative = lower)
    summary_text,
    ha='center', 
    va='center',
    fontsize=14,                   # Slightly larger than before for better visibility
    weight='bold',
    color='darkblue',
    bbox=dict(boxstyle="round,pad=0.6", facecolor="lightyellow", alpha=0.6)
)

st.pyplot(fig)




#Q4 How does the number of deaths vary across different states?
st.subheader("Question 4:: How does the number of deaths vary across different states?")

chart = alt.Chart(df).mark_boxplot(size=50).encode(
    x=alt.X('State:N', sort='-y'),
    y='Number of deaths:Q',
    color=alt.Color('State:N', legend=None)
).properties(width=700, height=500, title='Deaths by State (Boxplot)')

st.altair_chart(chart, use_container_width=True)

# Consistent summary using matplotlib-style text box
summary_text = (
    "Borno and Zamfara stand out with both higher median deaths and wider variability, "
    "While Abuja, Imo, and Lagos show relatively stable and lower death counts."
)

# Create a dummy figure just for the text box
dummy_fig, dummy_ax = plt.subplots(figsize=(10, 1))
dummy_fig.subplots_adjust(bottom=0.1)

dummy_fig.text(
    0.5, 0.5,
    summary_text,
    ha='center', 
    va='center',
    fontsize=14,
    weight='bold',
    color='darkblue',
    bbox=dict(boxstyle="round,pad=0.8", facecolor="lightyellow", alpha=0.65)
)

plt.axis('off')
st.pyplot(dummy_fig, use_container_width=True)


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
    "From 1970 to 2022, there’s a sharp rise, reaching about 8,000 deaths. "
    "The numbers continue climbing in 2023 and 2024, peaking at around 12,000 deaths. "
    "In 2025, the trend reverses dramatically, showing a steep decline."
)

# Closer version - reduced top margin
st.markdown(f"""
<div style="text-align: center; margin-top: 10px; margin-bottom: 20px;">
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
    "The key takeaway is that Borno stands out with a dramatically higher death toll "
    "compared to the rest, while Lagos records the lowest."
)

st.markdown(f"""
<div style="text-align: center; margin-top: 15px; margin-bottom: 20px;">
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




top_titles = df.groupby("Incident")["Number of deaths"].sum().nlargest(10)
# Increase figure size for a bigger pie chart
fig6, ax6 = plt.subplots(figsize=(24, 16))
ax6.pie(     top_titles,     labels=top_titles.index,     autopct='%1.1f%%',     startangle=90,     textprops={'fontsize': 16} # slightly larger labels ) ax6.set_title("Deaths by Incident (Top 10)", fontsize=22)
# Adjust bottom margin so chart leaves space for summary
fig6.subplots_adjust(bottom=0.20)
# Add summary text (two lines)
summary_text = (     "The top two categories — Auto Crashes and Banditry —\n"     "together account for over half (50.5%) of all incidents, "     "showing they dominate the landscape compared to other causes." )
# Bold summary annotation closer to chart
fig6.text(     0.5, -0.01, summary_text, # moved closer (was -0.05)     ha='center', va='center',     fontsize=18, weight='bold', color='darkblue',     bbox=dict(boxstyle="round,pad=0.5", facecolor="lightyellow", alpha=0.5) )
st.pyplot(fig6) i want the summary to drop sbit to the chartHere's the corrected and improved version of your code. The main issue was that y = -0.01 in fig6.text() is too high (almost at the bottom edge of the figure), so the summary text appears too close to (or overlapping with) the pie chart.
To drop the summary further down (more space below the chart), you need to use a more negative y value.
Recommended Fix:
Python# ... your existing code up to creating the pie chart ...

# Increase bottom margin a bit more to give extra space
fig6.subplots_adjust(bottom=0.28)   # was 0.20 → increased

summary_text = (
    "The top two categories — Auto Crashes and Banditry —\n"
    "together account for over half (50.5%) of all incidents, "
    "showing they dominate the landscape compared to other causes."
)

# Move the text further down by making y more negative
fig6.text(
    0.5, -0.12,          # ← Changed from -0.01 to -0.12 (or try -0.10 to -0.15)
    summary_text,
    ha='center', 
    va='center',
    fontsize=18, 
    weight='bold', 
    color='darkblue',
    bbox=dict(boxstyle="round,pad=0.5", facecolor="lightyellow", alpha=0.5)
)

st.pyplot(fig6)
Quick Tuning Tips:

-0.10 → moderate drop
-0.12 → good balance (recommended starting point)
-0.15 → drops it further down

If it's still too close or gets cut off, try these adjustments together:
Pythonfig6.subplots_adjust(bottom=0.32)   # even more space at bottom
fig6.text(0.5, -0.15, summary_text, ...)   # more negative y
Would you like me to also make the text wrap better or add a bit more padding? Just let me know how much space you want between the pie chart and the summary.4.5sFastdf['Month'] = df['Start date'].dt.month_name()
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
st.pyplot(fig), design the summary table likev the previous commandHere's a clean and consistent version of your code with the summary text styled similarly to your previous pie chart command (bold, larger font, lightyellow box, darkblue text, and properly spaced below the chart).
Improved & Consistent Code:
Pythondf['Month'] = df['Start date'].dt.month_name()

fig, ax = plt.subplots(figsize=(14, 8))

sns.countplot(
    data=df, 
    x='Month', 
    palette='tab20',
    order=['January','February','March','April','May','June','July',
           'August','September','October','November','December'], 
    ax=ax
)

# Annotate bar counts
for p in ax.patches:
    ax.annotate(f'{p.get_height():,.0f}',
                (p.get_x() + p.get_width()/2., p.get_height()),
                ha='center', va='bottom', 
                fontsize=11, color='black',
                xytext=(0, 6), textcoords='offset points')

# Titles and labels
ax.set_title('Number of Incidents by Month', fontsize=20, pad=20)
ax.set_xlabel("Month", fontsize=14)
ax.set_ylabel("Number of Incidents", fontsize=14)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

sns.despine()

# ====================== SUMMARY TEXT (Styled like your pie chart) ======================
summary_text = (
    "Incident counts fluctuate throughout the year, with noticeable peaks in "
    "January, July, and October, and dips in May, April, and November.\n"
    "Overall, the average is about 624 incidents per month, showing seasonal "
    "variation — higher in winter and summer, lower in spring."
)

# Make it look consistent with your previous summary
fig.subplots_adjust(bottom=0.28)   # Gives enough space below the chart

fig.text(
    0.5, -0.12,                    # Adjusted position (more negative = lower)
    summary_text,
    ha='center', 
    va='center',
    fontsize=14,                   # Slightly larger than before for better visibility
    weight='bold',
    color='darkblue',
    bbox=dict(boxstyle="round,pad=0.6", facecolor="lightyellow", alpha=0.6)
)

st.pyplot(fig)
Key Improvements Made:

Used the same styling approach as your pie chart summary (fig.text(), bold, darkblue, lightyellow box).
Increased bottom margin to 0.28 and lowered y to -0.12 so the summary sits nicely below the x-axis without overlapping.
Made the font a bit larger (14) and added weight='bold' for emphasis.
Slightly improved annotation formatting (:,.0f for cleaner numbers).
Added pad=20 to the title for better spacing.

Would you like me to make the summary box even more prominent (bigger font, stronger border, etc.) or adjust the vertical position further? Just tell me how it looks when you run it.1.7sFastadd this, Borno and Zamfara stand out with both higher median deaths and wider variability, while Abuja, Imo, and Lagos show relatively stable and lower death counts to this code , st.subheader("Question 4:: How does the number of deaths vary across different states?")
chart = alt.Chart(df).mark_boxplot(size=50).encode(
    x=alt.X('State:N', sort='-y'),
    y='Number of deaths:Q',
    color=alt.Color('State:N', legend=None)
).properties(width=700, height=500, title='Deaths by State (Boxplot)')
st.altair_chart(chart, use_container_width=True)
 using the previous designHere's the updated code with your new summary text added, styled consistently with your previous charts (pie chart and monthly bar chart):
Pythonst.subheader("Question 4:: How does the number of deaths vary across different states?")

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

# ====================== SUMMARY TEXT (Consistent Design) ======================
summary_text = (
    "Borno and Zamfara stand out with both higher median deaths and wider variability, "
    "while Abuja, Imo, and Lagos show relatively stable and lower death counts."
)

# Add space below the chart and place the summary text
fig = chart.properties(width=700, height=500).interactive()  # This is just a trick to get a figure

# Since we're using Altair + Streamlit, we use st.markdown + HTML or fig.text workaround.
# Best clean approach for consistency:

st.markdown("---")  # Optional separator

# Use HTML for better control and consistent styling (recommended for Altair charts)
st.markdown(f"""
<div style="text-align: center; margin-top: 20px;">
    <div style="
        display: inline-block;
        padding: 18px 25px;
        background-color: #fff9e6;
        border-radius: 12px;
        border: 1px solid #f0d68a;
        font-size: 15px;
        line-height: 1.5;
        color: #003366;
        font-weight: bold;
        max-width: 85%;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    ">
        {summary_text}
    </div>
</div>
""", unsafe_allow_html=True)
Alternative Version (using fig.text style - if you prefer matplotlib-style positioning):
If you want it even closer to your previous fig.text() design, here's a version using a hidden matplotlib figure just for the annotation:
Pythonst.subheader("Question 4:: How does the number of deaths vary across different states?")

chart = alt.Chart(df).mark_boxplot(size=50).encode(
    x=alt.X('State:N', sort='-y'),
    y='Number of deaths:Q',
    color=alt.Color('State:N', legend=None)
).properties(width=700, height=500, title='Deaths by State (Boxplot)')

st.altair_chart(chart, use_container_width=True)

# Consistent summary using matplotlib-style text box
summary_text = (
    "Borno and Zamfara stand out with both higher median deaths and wider variability, "
    "while Abuja, Imo, and Lagos show relatively stable and lower death counts."
)

# Create a dummy figure just for the text box
dummy_fig, dummy_ax = plt.subplots(figsize=(10, 1))
dummy_fig.subplots_adjust(bottom=0.1)

dummy_fig.text(
    0.5, 0.5,
    summary_text,
    ha='center', 
    va='center',
    fontsize=14,
    weight='bold',
    color='darkblue',
    bbox=dict(boxstyle="round,pad=0.8", facecolor="lightyellow", alpha=0.65)
)

plt.axis('off')
st.pyplot(dummy_fig, use_container_width=True)
Recommendation: Use the HTML version — it looks cleaner with Altair charts and gives you better control over spacing and responsiveness.
Would you like me to make the box larger, change the colors, or adjust the padding? Just say how you want it to look.2sFasti want to add this summary, From 1970 to 2022, there’s a sharp rise, reaching about 8,000 deaths. The numbers continue climbing in 2023 and 2024, peaking at around 12,000 deaths.

In 2025, the trend reverses dramatically, showing a steep decline. to this code #Q5 Has the frequency or severity of fatal incidents increased or decreased year-over-year?
st.subheader("Question 5:: Has the frequency or severity of fatal incidents increased or decreased year-over-year?")
line_chart = alt.Chart(df).mark_line(point=True).encode(
    x='year(Start date):O',
    y='sum(Number of deaths):Q',
    tooltip=['year(Start date)', 'sum(Number of deaths)']
).properties(width=700)
st.altair_chart(line_chart, use_container_width=True) using previous design
Here's the clean and consistent version with your new summary added, styled similarly to your previous charts:
Python# Q5: Has the frequency or severity of fatal incidents increased or decreased year-over-year?
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

# ====================== SUMMARY TEXT (Consistent Design) ======================
summary_text = (
    "From 1970 to 2022, there’s a sharp rise, reaching about 8,000 deaths. "
    "The numbers continue climbing in 2023 and 2024, peaking at around 12,000 deaths.\n"
    "In 2025, the trend reverses dramatically, showing a steep decline."
)

# Clean HTML version (Recommended - looks best with Altair charts)
st.markdown("---")

st.markdown(f"""
<div style="text-align: center; margin: 25px 0 10px 0;">
    <div style="
        display: inline-block;
        padding: 18px 28px;
        background-color: #fff9e6;
        border-radius: 12px;
        border: 1px solid #f0d68a;
        font-size: 15px;
        line-height: 1.6;
        color: #003366;
        font-weight: bold;
        max-width: 90%;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
    ">
        {summary_text}
    </div>
</div>
""", unsafe_allow_html=True)
Alternative Version (Matplotlib-style text box - if you prefer the exact look of your earlier pie & bar charts):
Python# After st.altair_chart(...)

summary_text = (
    "From 1970 to 2022, there’s a sharp rise, reaching about 8,000 deaths. "
    "The numbers continue climbing in 2023 and 2024, peaking at around 12,000 deaths.\n"
    "In 2025, the trend reverses dramatically, showing a steep decline."
)

# Create a small matplotlib figure for consistent text box styling
fig_text, ax_text = plt.subplots(figsize=(12, 2.2))
fig_text.subplots_adjust(bottom=0.4)

fig_text.text(
    0.5, 0.55,
    summary_text,
    ha='center', 
    va='center',
    fontsize=14,
    weight='bold',
    color='darkblue',
    bbox=dict(boxstyle="round,pad=0.8", facecolor="lightyellow", alpha=0.65)
)

ax_text.axis('off')
st.pyplot(fig_text, use_container_width=True)
Recommendation:
I suggest using the HTML version for Altair charts because it gives better spacing control and responsiveness.
Would you like me to:

Make the summary box bigger / smaller?
Increase the font size?
Add bullet points instead of paragraph form?

Just tell me your preference and I’ll adjust it immediately.1.3sFasti want to add this summary: From 1970 to 2022, there’s a sharp rise, reaching about 8,000 deaths. The numbers continue climbing in 2023 and 2024, peaking at around 12,000 deaths. In 2025, the trend reverses dramatically, showing a steep decline. to this code using the previous design: line_chart = alt.Chart(df).mark_line(point=True).encode(     x='year(Start date):O',     y='sum(Number of deaths):Q',     tooltip=['year(Start date)', 'sum(Number of deaths)'] ).properties(width=700) st.altair_chart(line_chart, use_container_width=True)Here's the updated code with your summary added, using the consistent design from your previous charts (light yellow box, bold dark blue text, good spacing, and rounded style):
Python# Q5: Has the frequency or severity of fatal incidents increased or decreased year-over-year?
st.subheader("Question 5:: Has the frequency or severity of fatal incidents increased or decreased year-over-year?")

line_chart = alt.Chart(df).mark_line(point=True).encode(
    x='year(Start date):O',
    y='sum(Number of deaths):Q',
    tooltip=['year(Start date)', 'sum(Number of deaths)']
).properties(
    width=700, 
    height=500,                    # Added height for better proportion
    title='Total Deaths by Year (Trend)'
)

st.altair_chart(line_chart, use_container_width=True)

# ====================== SUMMARY TEXT (Consistent with previous charts) ======================
summary_text = (
    "From 1970 to 2022, there’s a sharp rise, reaching about 8,000 deaths. "
    "The numbers continue climbing in 2023 and 2024, peaking at around 12,000 deaths. "
    "In 2025, the trend reverses dramatically, showing a steep decline."
)

# Clean and consistent HTML box (recommended for Altair charts)
st.markdown(f"""
<div style="text-align: center; margin-top: 25px; margin-bottom: 15px;">
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
This matches the style you’ve been using:

Light yellow background
Dark blue bold text
Rounded box with subtle shadow
Good spacing below the chart

Would you like any small adjustments?

Bigger text?
More padding inside the box?
Add line breaks or bullet points?

Just let me know and I’ll tweak it right away.1.5sFast# Q5: Has the frequency or severity of fatal incidents increased or decreased year-over-year? st.subheader("Question 5:: Has the frequency or severity of fatal incidents increased or decreased year-over-year?")
line_chart = alt.Chart(df).mark_line(point=True).encode( x='year(Start date):O', y='sum(Number of deaths):Q', tooltip=['year(Start date)', 'sum(Number of deaths)'] ).properties( width=700, height=500, # Added height for better proportion title='Total Deaths by Year (Trend)' )
st.altair_chart(line_chart, use_container_width=True)
# ====================== SUMMARY TEXT (Consistent with previous charts) ====================== summary_text = ( "From 1970 to 2022, there’s a sharp rise, reaching about 8,000 deaths. " "The numbers continue climbing in 2023 and 2024, peaking at around 12,000 deaths. " "In 2025, the trend reverses dramatically, showing a steep decline." )
# Clean and consistent HTML box (recommended for Altair charts) st.markdown(f"""
 {summary_text}
 """, unsafe_allow_html=True)
i want the summary closer to the chartHere's the updated code with the summary closer to the chart (reduced spacing above the box):
Python# Q5: Has the frequency or severity of fatal incidents increased or decreased year-over-year?
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
    "From 1970 to 2022, there’s a sharp rise, reaching about 8,000 deaths. "
    "The numbers continue climbing in 2023 and 2024, peaking at around 12,000 deaths. "
    "In 2025, the trend reverses dramatically, showing a steep decline."
)

# Closer version - reduced top margin
st.markdown(f"""
<div style="text-align: center; margin-top: 10px; margin-bottom: 20px;">
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
Key Change:

Changed margin-top: 25px → margin-top: 10px (much closer to the line chart now)

Want it even closer?
If you want the summary very tight to the bottom of the chart, change margin-top: 10px to margin-top: 5px or even margin-top: 2px.
Would you like me to make it even closer, or do you prefer this spacing?
You can also try this ultra-close version if needed:
Python# Ultra close version
st.markdown(f"""
<div style="text-align: center; margin-top: 5px; margin-bottom: 15px;">
    ... same box style ...
</div>
""", unsafe_allow_html=True)
Let me know how it looks and if you want further adjustment!2.2sFasti want to add this summary: The key takeaway is that Borno stands out with a dramatically higher death toll compared to the rest, while Lagos records the lowest. to this code and use html design: #Q6 Top 8 states have the highest cumulative death toll?
st.subheader("Question 6:: Which states have the highest cumulative death toll?")
state_data = df.groupby('State')['Number of deaths'].sum().nlargest(8).reset_index()
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=state_data, x='Number of deaths', y='State', palette='tab20', ax=ax)
ax.set_title("Top 8 States by Total Deaths", fontsize=16)
st.pyplot(fig)Here's the updated code with your new summary added using the consistent HTML design you've been using:
Python# Q6: Top 8 states have the highest cumulative death toll?
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
    "The key takeaway is that Borno stands out with a dramatically higher death toll "
    "compared to the rest, while Lagos records the lowest."
)

st.markdown(f"""
<div style="text-align: center; margin-top: 15px; margin-bottom: 20px;">
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
This keeps the same clean HTML box style as your previous charts (light yellow background, dark blue bold text, rounded corners, subtle shadow).
Quick adjustments you can make:

Even closer to the chart → change margin-top: 15px to margin-top: 8px or margin-top: 5px
More space → increase margin-top to 20px or 25px

Would you like me to make the summary closer, larger, or add any other tweaks?1.8sFasti want to add this summary : Mortality is strongly seasonal, with a sharp spike in January and a dip in June, while the rest of the year remains relatively steady.
Q7 to my code using html : #Q7 Which months are the "deadliest" across the historical record?
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
]Here's the clean and consistent code with your new summary added using the HTML design you've been using:
Python# Q7: Which months are the "deadliest" across the historical record?
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
    "Mortality is strongly seasonal, with a sharp spike in January and a dip in June, "
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
