import pandas as pd
import requests
import io
import streamlit as st

@st.cache_data
def load_and_preprocess_data() -> pd.DataFrame:
    url = 'https://everytownresearch.org/wp-content/uploads/sites/4/etown-maps/gunfire-on-school-grounds/data.csv'
    headers = {'User-Agent': 'Mozilla/5.0'}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()

    df = pd.read_csv(io.StringIO(resp.text))

    df['Incident Date'] = pd.to_datetime(df['Incident Date'], errors='coerce')
    df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
    df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')
    df.dropna(subset=['Latitude','Longitude'], inplace=True)

    # Drop extraneous columns
    remove_cols = ['Source 2', 'URL 2', 'Source 3', 'URL 3', 'School Type', 'Created', 'Last Modified']
    for c in remove_cols:
        if c in df.columns:
            df.drop(columns=c, inplace=True)

    df['Year'] = df['Incident Date'].dt.year
    df['Month'] = df['Incident Date'].dt.strftime('%b')
    df['DayOfWeek'] = df['Incident Date'].dt.strftime('%a')

    # Map state abbreviations
    state_map = {
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
    df['State_name'] = df['State'].map(state_map)

    return df
