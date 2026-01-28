# narrative_analysis.py
"""
Narrative Analysis Module

Analyzes text descriptions of incidents to extract patterns and insights.
Focuses on clear, actionable findings from narrative data.
"""

import re
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
from collections import Counter
from wordcloud import WordCloud
import base64
from io import BytesIO
from utils.utils_common import display_metric_card, display_info_box, COLORS


def display_narrative_analysis(df: pd.DataFrame):
    """
    Main entry point for narrative analysis section.
    """
    if df.empty or "Narrative" not in df.columns:
        st.warning("No narrative data available for analysis.")
        return

    narratives = df["Narrative"].dropna()
    if narratives.empty:
        st.info("No narrative descriptions found in the current data selection.")
        return

    # Show coverage metrics
    st.markdown("### 📝 Narrative Analysis")
    display_coverage_metrics(df, narratives)
    
    # Create simple two-tab layout
    tab1, tab2 = st.tabs(["📊 Key Words & Themes", "👥 People Mentioned"])
    
    with tab1:
        display_word_analysis(narratives)
    
    with tab2:
        display_people_analysis(narratives)


def display_coverage_metrics(df: pd.DataFrame, narratives: pd.Series):
    """Show simple metrics about narrative data availability."""
    
    total_incidents = len(df)
    with_narratives = len(narratives)
    coverage_rate = (with_narratives / total_incidents * 100) if total_incidents > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Narrative Coverage", f"{coverage_rate:.0f}%", 
                  help="Percentage of incidents with text descriptions")
    
    with col2:
        st.metric("Total Narratives", f"{with_narratives:,}")
    
    with col3:
        avg_length = int(narratives.str.len().mean())
        st.metric("Avg Length", f"{avg_length} chars")


def display_word_analysis(narratives: pd.Series):
    """Analyze and display common words and themes from narratives."""
    
    st.markdown("#### What the Narratives Tell Us")
    
    # Process all narrative text
    all_text = " ".join(narratives.astype(str)).lower()
    
    # Extract meaningful words (4+ letters, exclude common words)
    words = re.findall(r'\b[a-z]{4,}\b', all_text)
    
    # Common words to exclude (expanded list for cleaner results)
    stopwords = {
        'the', 'and', 'for', 'with', 'that', 'have', 'from', 'this', 'was', 'were',
        'when', 'what', 'there', 'which', 'been', 'into', 'while', 'could', 'also',
        'after', 'they', 'their', 'them', 'where', 'would', 'about', 'school', 
        'student', 'students', 'campus', 'year', 'reported', 'police', 'said',
        'incident', 'found', 'near', 'during', 'time', 'area', 'located'
    }
    
    meaningful_words = [w for w in words if w not in stopwords]
    
    if not meaningful_words:
        st.info("No significant word patterns found.")
        return
    
    # Count word frequencies
    word_freq = Counter(meaningful_words)
    top_20 = word_freq.most_common(20)
    
    # Create simple word cloud
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("##### Word Cloud")
        
        # Generate word cloud
        wc = WordCloud(
            width=600,
            height=300,
            background_color="white",
            colormap="Blues",
            max_words=50,
            relative_scaling=0.7,
            min_font_size=14
        ).generate_from_frequencies(dict(top_20))
        
        # Convert to image and display
        img = wc.to_image()
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        st.markdown(
            f'<div style="text-align: center;">'
            f'<img src="data:image/png;base64,{img_str}" style="max-width: 100%;">'
            f'</div>',
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown("##### Top 10 Words")
        for word, count in top_20[:10]:
            pct = (count / len(meaningful_words) * 100)
            st.markdown(f"**{word}** ({count} times)")
    
    # Key themes analysis
    st.markdown("##### Key Themes Found")
    
    # Simple theme detection
    themes = {
        '🔫 Weapons': ['gun', 'firearm', 'weapon', 'pistol', 'rifle', 'shot'],
        '📍 Locations': ['parking', 'classroom', 'hallway', 'cafeteria', 'field'],
        '⏰ Timing': ['morning', 'afternoon', 'evening', 'before', 'after'],
        '👮 Response': ['arrested', 'custody', 'hospital', 'transported']
    }
    
    theme_counts = {}
    for theme_name, keywords in themes.items():
        count = sum(all_text.count(keyword) for keyword in keywords)
        if count > 0:
            theme_counts[theme_name] = count
    
    if theme_counts:
        # Display themes in a clean grid
        cols = st.columns(len(theme_counts))
        for i, (theme, count) in enumerate(theme_counts.items()):
            with cols[i]:
                st.metric(theme, count, "mentions")


def display_people_analysis(narratives: pd.Series):
    """Analyze age mentions in narratives."""
    
    st.markdown("#### Ages Mentioned in Narratives")
    
    # Extract age mentions (e.g., "17-year-old")
    age_pattern = re.compile(r'(\d{1,2})-year-old', re.IGNORECASE)
    age_mentions = []
    
    for narrative in narratives:
        ages = age_pattern.findall(str(narrative))
        age_mentions.extend([int(age) for age in ages if 5 <= int(age) <= 65])
    
    if not age_mentions:
        st.info("No age references found in the narratives.")
        return
    
    # Create age dataframe
    age_df = pd.DataFrame(age_mentions, columns=['Age'])
    
    # Summary statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Age References", len(age_mentions))
    
    with col2:
        st.metric("Average Age", f"{age_df['Age'].mean():.0f} years")
    
    with col3:
        most_common = age_df['Age'].mode().iloc[0] if not age_df.empty else 0
        st.metric("Most Common Age", f"{most_common} years")
    
    # Age distribution chart
    st.markdown("##### Age Distribution")
    
    # Create histogram
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=age_df['Age'],
        nbinsx=20,
        marker_color=COLORS['primary'],
        hovertemplate='Age: %{x}<br>Count: %{y}<extra></extra>'
    ))
    
    # Add average line
    avg_age = age_df['Age'].mean()
    fig.add_vline(
        x=avg_age,
        line_dash="dash",
        line_color=COLORS['accent'],
        annotation_text=f"Avg: {avg_age:.0f}",
        annotation_position="top right"
    )
    
    fig.update_layout(
        xaxis_title="Age (years)",
        yaxis_title="Number of Mentions",
        height=300,
        showlegend=False,
        plot_bgcolor='white'
    )
    
    st.plotly_chart(fig, width='stretch')
    
    # Age group summary
    st.markdown("##### Age Groups")
    
    # Define age groups
    age_groups = pd.cut(
        age_df['Age'],
        bins=[0, 12, 17, 25, 100],
        labels=['Children (≤12)', 'Teens (13-17)', 'Young Adults (18-25)', 'Adults (>25)']
    )
    
    group_counts = age_groups.value_counts()
    
    # Display as simple metrics
    cols = st.columns(len(group_counts))
    for i, (group, count) in enumerate(group_counts.items()):
        with cols[i]:
            pct = (count / len(age_df) * 100)
            st.metric(group, f"{pct:.0f}%", f"{count} mentions")
    
    # Note about interpretation
    st.info(
        "💡 **Note:** Age mentions in narratives may refer to victims, suspects, "
        "or witnesses. These numbers provide context but should not be interpreted "
        "as definitive demographic data."
    )