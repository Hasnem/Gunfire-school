# narrative_analysis.py
"""
Narrative Analysis Module

Features:
  1) Word Cloud of most common words in 'Narrative' (Plotly-based)
  2) Age distribution from "X-year-old" references (Plotly-based)
  3) Clear disclaimers about the limitations of textual data.
"""

import re
import io
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from collections import Counter
from wordcloud import WordCloud


def display_narrative_analysis(df: pd.DataFrame):
    """
    Main function to render all narrative-based analyses:
      - Word Cloud visualization
      - Age extraction and histogram
      - Observations & disclaimers for each
    """
    if df.empty or "Narrative" not in df.columns:
        st.warning("No 'Narrative' data is available.")
        return

    st.markdown("<h2>Narrative Analysis</h2>", unsafe_allow_html=True)
    st.divider()

    # 1) Word Cloud
    st.markdown("<h3>1. Word Cloud of Common Terms</h3>", unsafe_allow_html=True)
    plot_narrative_wordcloud(df)
    st.markdown(generate_wordcloud_observation(df), unsafe_allow_html=True)
    st.divider()

    # 2) Age Mentions
    st.markdown('<h3>2. Age Mentions ("X-year-old")</h3>', unsafe_allow_html=True)
    plot_age_distribution(df)
    st.markdown(generate_age_distribution_observation(df), unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 1) WORD CLOUD
# -----------------------------------------------------------------------------

def plot_narrative_wordcloud(df: pd.DataFrame, max_words: int = 200):
    """
    Build a word cloud from the 'Narrative' text, then embed it into a Plotly figure
    so it fits the dashboard's overall style.

    Parameters
    ----------
    df : pd.DataFrame
        The filtered dataset containing a 'Narrative' column.
    max_words : int, optional
        The maximum number of words to display in the cloud. Defaults to 200.
    """
    narratives = df["Narrative"].dropna().astype(str)
    if narratives.empty:
        st.info("No valid 'Narrative' text found.")
        return

    # Combine all narratives into one string (lowercased)
    combined_text = " ".join(narratives).lower()

    # Find words of length >=3 (so we skip 'a', 'an', 'the', etc.)
    words = re.findall(r'\b[a-z]{3,}\b', combined_text)

    # Minimal stopwords (expand as needed)
    stopwords = {
        "the","and","for","with","that","have","from","this","was","were","when",
        "what","there","which","been","into","while","could","also","after","such",
        "they","their","them","where","would","should","about","very","many","said",
        "those","being","some","other","these","every","your","having","them"
    }
    filtered_words = [w for w in words if w not in stopwords]
    if not filtered_words:
        st.info("No significant words found after removing common filler words.")
        return

    # Count frequencies
    freq_dict = Counter(filtered_words)

    # Generate the word cloud image using the "Blues" colormap
    wc = WordCloud(
        width=800,
        height=400,
        background_color="white",
        colormap="Blues",
        max_words=max_words
    ).generate_from_frequencies(freq_dict)

    # Convert the WordCloud to an array (RGB) that we can embed in Plotly
    wc_img = wc.to_array()

    # Create a blank Plotly figure and add the word cloud image
    fig = go.Figure()

    # We embed the NumPy array as an image in the layout
    fig.add_layout_image(
        dict(
            source=px.imshow(wc_img).data[0].source,
            xref="paper",
            yref="paper",
            x=0,
            y=1,
            sizex=1,
            sizey=1,
            xanchor="left",
            yanchor="top",
            sizing="stretch",
            layer="below"
        )
    )

    # Hide axes, set a minimal margin
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    fig.update_layout(
        width=800,
        height=400,
        margin=dict(l=0, r=0, t=30, b=0),
        paper_bgcolor="white"
    )

    st.plotly_chart(fig, use_container_width=True)


def generate_wordcloud_observation(df: pd.DataFrame) -> str:
    """
    Provide textual insights about the word cloud.

    Parameters
    ----------
    df : pd.DataFrame

    Returns
    -------
    str
        HTML snippet with observations and disclaimers.
    """
    n_narratives = df["Narrative"].dropna().shape[0]
    if n_narratives == 0:
        return "<p>No narratives to discuss.</p>"

    return f"""
    <p style="font-size:90%;">
      <b>Observations:</b><br/>
      We analyzed <b>{n_narratives}</b> narratives to generate this word cloud. 
      The largest words in the cloud appear most frequently in the text, 
      hinting at recurring storylines (e.g., <i>gun</i>, <i>shooting</i>, 
      <i>student</i>, <i>police</i>). High-frequency words can reflect the 
      key issues or circumstances surrounding these incidents, though they 
      won't tell the full story by themselves.<br/><br/>
      By scanning these commonly used terms, readers can quickly grasp 
      overarching themes—like arguments in school parking lots or 
      ongoing campus security challenges—warranting deeper exploration.
    </p>
    """


# -----------------------------------------------------------------------------
# 2) AGE MENTIONS
# -----------------------------------------------------------------------------

def plot_age_distribution(df: pd.DataFrame):
    """
    Parses all 'Narrative' text for patterns like "16-year-old" and plots a histogram.
    For a consistent look-and-feel, we use Plotly and the 'Blues' color scheme.

    Parameters
    ----------
    df : pd.DataFrame
        The filtered dataset with a 'Narrative' column.
    """
    narratives = df["Narrative"].dropna().astype(str)
    if narratives.empty:
        st.info("No valid 'Narrative' text available.")
        return

    # Extract any 'X-year-old' references
    pattern = re.compile(r'\b(\d{1,2})-year-old\b', re.IGNORECASE)
    extracted_ages = []

    for text in narratives:
        matches = pattern.findall(text)
        extracted_ages.extend(int(age_str) for age_str in matches)

    if not extracted_ages:
        st.info("No 'X-year-old' references found in these narratives.")
        return

    age_series = pd.Series(extracted_ages, name="Ages")
    total_mentions = len(extracted_ages)
    avg_age = age_series.mean()
    median_age = age_series.median()

    # Display quick stats
    c1, c2, c3 = st.columns(3)
    c1.metric("References Found", f"{total_mentions}")
    c2.metric("Avg Age", f"{avg_age:.1f}")
    c3.metric("Median Age", f"{median_age:.1f}")

    # Top 5 most-mentioned ages
    top5 = age_series.value_counts().head(5).rename("Count")
    st.subheader("5 Most-Mentioned Ages")
    st.table(top5)

    # Build a Plotly histogram
    fig = px.histogram(
        age_series,
        x="Ages",
        nbins=20,
        title="Distribution of 'X-year-old' Mentions in Narratives",
        color_discrete_sequence=["#094486"]  # a deep "Blues" tone
    )
    fig.update_layout(
        xaxis_title="Age (as mentioned in text)",
        yaxis_title="Count of Mentions",
        bargap=0.1,
        margin=dict(l=0, r=0, t=80, b=0)
    )
    st.plotly_chart(fig, use_container_width=True)


def generate_age_distribution_observation(df: pd.DataFrame) -> str:
    """
    Create a short explanatory HTML snippet for the Age Distribution chart,
    clarifying that we don't know if these ages are suspects, victims, or others.

    Parameters
    ----------
    df : pd.DataFrame

    Returns
    -------
    str
        HTML snippet with disclaimers and potential interpretations.
    """
    pattern = re.compile(r'\b(\d{1,2})-year-old\b', re.IGNORECASE)
    combined_text = " ".join(df["Narrative"].dropna().astype(str))
    mentions = pattern.findall(combined_text)
    if not mentions:
        return "<p>No age references to analyze.</p>"

    total_references = len(mentions)
    return f"""
    <p style="font-size:90%;">
      <b>Observations & Disclaimers:</b><br/>
      In total, we detected <b>{total_references}</b> references to “X-year-old”
      across the narratives. However, these mentions do not indicate whether
      the individuals cited were victims, suspects, bystanders, or otherwise
      involved. Some incidents include multiple ages (e.g., both the shooter
      and victims), potentially skewing the data.<br/><br/>
      Repeated references to certain ages—like 16 or 17—might suggest 
      teenagers are frequently involved, but additional details would be needed
      to distinguish their specific roles or motivations. For a comprehensive
      understanding, we recommend looking beyond these numeric hints and
      considering the incident context, outcomes, and any available 
      investigative reports.
    </p>
    """
