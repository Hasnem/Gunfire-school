import streamlit as st

def about_page() -> None:
    """
    Renders a more comprehensive "About" page detailing the project's context,
    methodology, tools, limitations, and call to action.
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

        <!-- Project Overview -->
        <h4 class="everytown-blue important">Project Motivation</h4>
        <p>
          Gunfire on school grounds is a deeply troubling reality that demands attention 
          and actionable insights. This project aims to harness data from 
          <a href="https://everytownresearch.org/maps/gunfire-on-school-grounds/" 
             class="source-link" target="_blank">Everytown Research</a> 
          to inform policymakers, educators, researchers, and the public about the scale 
          and nature of these incidents, and inspire data-driven dialogue.
        </p>

        <!-- Our Data Story -->
        <h4 class="everytown-blue important">Our Data Story</h4>
        <p>
          Each chart and observation in this dashboard tells a chapter in a broader narrative 
          about gunfire incidents on school grounds across the United States. 
          By translating raw data into digestible visuals, our goal is to illuminate trends 
          and encourage thoughtful discussions around prevention.
        </p>

        <!-- Behind the Numbers -->
        <h4 class="everytown-blue important">Behind the Numbers</h4>
        <p>
          The dataset includes:
        </p>
        <ul>
          <li><span class="everytown-red important">Date, City, and State</span> – pinpointing each incident in time and space</li>
          <li><span class="everytown-red important">Latitude/Longitude</span> – enabling geographic plotting and hotspot identification</li>
          <li><span class="everytown-red important">Intent & Outcome</span> – offering insights into the nature and aftermath of these events</li>
          <li><span class="everytown-red important">Number Killed & Wounded</span> – revealing the human toll in stark terms</li>
          <li><span class="everytown-red important">Narratives</span> – providing qualitative context for each incident where available</li>
        </ul>

        <!-- Methodology & Sources -->
        <h4 class="everytown-blue important">Methodology & Sources</h4>
        <p>
          <a href="https://everytownresearch.org/" class="source-link" target="_blank">Everytown Research</a> 
          continually updates these figures through news reports, law enforcement data, 
          and official records. Our dashboard fetches this dataset in near real-time, 
          and automatically applies data transformations (cleaning, mapping state abbreviations, 
          and generating new columns) for seamless exploration.
        </p>

        <!-- Tools & Technology -->
        <h4 class="everytown-blue important">Tools & Technology</h4>
        <ul>
          <li><b>Streamlit</b> – for the interactive UI and user-driven filters</li>
          <li><b>Pandas</b> – for data cleaning, filtering, and analysis</li>
          <li><b>Plotly</b> – to create dynamic and interactive visualizations (line charts, bar charts, maps, etc.)</li>
          <li><b>Requests</b> – for fetching CSV data from Everytown’s website</li>
        </ul>

        <!-- Limitations & Future Directions -->
        <h4 class="everytown-blue important">Limitations & Future Directions</h4>
        <p>
          Despite striving for timely and accurate insights, there are inherent limitations:
        </p>
        <ul>
          <li><span class="everytown-red important">Partial 2025 Data</span> – The data for 2025 is still evolving and may not capture all incidents.</li>
          <li><span class="everytown-red important">Delayed Reporting</span> – Some incidents may be reported late or require verification.</li>
          <li><span class="everytown-red important">Geo-Coordinates</span> – Missing or inaccurate latitude/longitude can affect the accuracy of the maps.</li>
          <li><span class="everytown-red important">Future Enhancements</span> – Including external datasets (e.g., demographic, local policy) could add vital context.</li>
        </ul>

        <!-- Our Mission -->
        <h4 class="everytown-blue important">Our Mission</h4>
        <p>
          By transforming raw data into compelling visuals, this dashboard seeks to spark 
          conversations and drive meaningful changes to address gun violence in schools.
        </p>

        <!-- A Call to Action -->
        <h4 class="everytown-blue important">A Call to Action</h4>
        <p>
          We invite everyone—policymakers, researchers, educators, concerned citizens—to explore 
          these findings. Every data point is a step toward greater awareness and collaborative 
          action in preventing future tragedies.
        </p>
        """,
        unsafe_allow_html=True
    )
