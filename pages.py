import streamlit as st

def about_page() -> None:
    """
    Renders the "About" page with a narrative that sets the context for the dashboard.
    """
    st.title("About This Dashboard")
    st.markdown(
        """
        <style>
        .everytown-red { color: #E91436; }
        .everytown-blue { color: #00629b; }
        .important { font-weight: bold; }
        .source-link { color: #0033A0; text-decoration: none; }
        </style>

        <h4 class="everytown-blue important">Our Data Story</h4>
        <p>
          This dashboard presents data meticulously compiled by 
          <a href="https://everytownresearch.org/maps/gunfire-on-school-grounds/" class="source-link" target="_blank">
          Everytown Research
          </a>. Each number, chart, and observation is a chapter in a broader narrative about gunfire incidents on school grounds across the United States.
        </p>

        <h4 class="everytown-blue important">Behind the Numbers</h4>
        <p>
          The dataset encompasses details such as:
        </p>
        <ul>
          <li><span class="everytown-red important">Date, City, and State</span> – situating each incident in time and space</li>
          <li><span class="everytown-red important">Geographic Coordinates</span> – enabling a spatial exploration of incidents</li>
          <li><span class="everytown-red important">Intent & Outcome</span> – offering insights into the nature of these events</li>
          <li><span class="everytown-red important">Casualties</span> – highlighting the human toll through numbers killed and injured</li>
          <li><span class="everytown-red important">Narratives</span> – providing contextual depth to each incident</li>
        </ul>

        <h4 class="everytown-blue important">Our Mission</h4>
        <p>
          By transforming raw data into compelling visual stories, this dashboard aims to inform, engage, and ultimately inspire action on the urgent issue of gun violence in schools.
        </p>

        <h4 class="everytown-blue important">Methodology & Sources</h4>
        <p>
          Everytown Research employs rigorous cross-verification with news reports, law enforcement data, and official records to ensure the accuracy of the information presented here.
        </p>

        <h4 class="everytown-blue important">A Call to Action</h4>
        <p>
          As you explore the evolving narrative—from yearly reflections to regional insights—let each statistic be a reminder of the lives behind the numbers and a call for meaningful change.
        </p>
        """,
        unsafe_allow_html=True
    )
