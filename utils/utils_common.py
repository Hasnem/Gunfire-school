import streamlit as st
import pandas as pd

FONT_SIZE = "16px"

STATE_MAPPING = {
    'AL':'Alabama','AK':'Alaska','AZ':'Arizona','AR':'Arkansas','CA':'California','CO':'Colorado','CT':'Connecticut',
    'DE':'Delaware','FL':'Florida','GA':'Georgia','HI':'Hawaii','ID':'Idaho','IL':'Illinois','IN':'Indiana','IA':'Iowa',
    'KS':'Kansas','KY':'Kentucky','LA':'Louisiana','ME':'Maine','MD':'Maryland','MA':'Massachusetts','MI':'Michigan',
    'MN':'Minnesota','MS':'Mississippi','MO':'Missouri','MT':'Montana','NE':'Nebraska','NV':'Nevada','NH':'New Hampshire',
    'NJ':'New Jersey','NM':'New Mexico','NY':'New York','NC':'North Carolina','ND':'North Dakota','OH':'Ohio','OK':'Oklahoma',
    'OR':'Oregon','PA':'Pennsylvania','RI':'Rhode Island','SC':'South Carolina','SD':'South Dakota','TN':'Tennessee',
    'TX':'Texas','UT':'Utah','VT':'Vermont','VA':'Virginia','WA':'Washington','WV':'West Virginia','WI':'Wisconsin',
    'WY':'Wyoming','DC':'District of Columbia','PR':'Puerto Rico','GU':'Guam','VI':'Virgin Islands',
    'MP':'Northern Mariana Islands','AS':'American Samoa'
}

def display_header():
    st.markdown(
        f"""
        <h1 style="font-size:2.5em;">
            <span style="color:red;">Gunfire</span> on U.S. School Grounds: 
            <span style="color:red;">A Real-Time Dashboard</span>
        </h1>
        <p style="font-size:{FONT_SIZE};">
          Data source: 
          <a href="https://everytownresearch.org/maps/gunfire-on-school-grounds/"
             target="_blank" style="text-decoration:none; color:blue;">
            Everytown Research
          </a>
        </p>
        """,
        unsafe_allow_html=True
    )

def display_latest_incident(df: pd.DataFrame):
    if df.empty:
        st.sidebar.subheader("No incidents found for the selected filters.")
        return
    
    max_date = df["Incident Date"].max()
    row = df.loc[df["Incident Date"] == max_date].iloc[0]
    date_str = row["Incident Date"].strftime("%B %d, %Y")
    # If 'Narrative' doesn't exist or is empty, provide a fallback
    narrative_text = row["Narrative"] if "Narrative" in row and pd.notnull(row["Narrative"]) else "No additional narrative available."

    st.sidebar.subheader("Latest Recorded Incident:")
    st.sidebar.markdown(
        f"""
        <p>
          <b>Date:</b> {date_str}<br>
          <b>Location:</b> {row['School name']} in {row['City']}, {row['State']}<br>
          <b style="color:red;">Killed:</b> {row['Number Killed']} |
          <b style="color:green;">Wounded:</b> {row['Number Wounded']}<br>
          <b>Narrative:</b> {narrative_text}
        </p>
        """,
        unsafe_allow_html=True
    )

def metric_cards(df: pd.DataFrame):
    if df.empty:
        st.write("No data to show metrics.")
        return
    
    num_incidents = len(df)
    killed = int(df["Number Killed"].sum())
    wounded = int(df["Number Wounded"].sum())
    total_victims = killed + wounded

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Victims", total_victims)
    c2.metric("Incidents", num_incidents)
    c3.metric("Killed", killed)
    c4.metric("Wounded", wounded)

    style_metric_cards()
    st.divider()

def style_metric_cards(background_color:str="#FAFAFA",
                       border_size_px:int=1,
                       border_color:str="#CCC",
                       border_radius_px:int=5,
                       border_left_color:str="#ED2F2C",
                       box_shadow:bool=True):
    box_shadow_str = "box-shadow:0 0.15rem 1.75rem 0 rgba(58,59,69,0.15) !important;" if box_shadow else "box-shadow:none !important;"
    st.markdown(
        f"""
        <style>
          div[data-testid="stMetric"],
          div[data-testid="metric-container"] {{
            background-color:{background_color} !important;
            border:{border_size_px}px solid {border_color} !important;
            padding:3% 3% 3% 5% !important;
            border-radius:{border_radius_px}px !important;
            border-left:0.5rem solid {border_left_color} !important;
            {box_shadow_str}
          }}
        </style>
        """,
        unsafe_allow_html=True
    )
