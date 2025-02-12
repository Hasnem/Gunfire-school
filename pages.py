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
          to inform policymakers, educators, researchers, and the public about the scale and nature of these incidents.
        </p>

        <!-- Our Data Story -->
        <h4 class="everytown-blue important">Our Data Story</h4>
        <p>
          Each chart and observation in this dashboard tells a chapter in a broader narrative 
          about gunfire incidents on school grounds across the United States. 
          By translating raw data into digestible visuals, our goal is to illuminate trends 
          and encourage data-driven discussions around safety and prevention.
        </p>

        <!-- Behind the Numbers -->
        <h4 class="everytown-blue important">Behind the Numbers</h4>
        <p>
          The dataset includes:
        </p>
        <ul>
          <li><span class="everytown-red important">Date, City, and State</span> – pinpoints each incident in time and space</li>
          <li><span class="everytown-red important">Latitude/Longitude</span> – enables geographic plotting and hotspot identification</li>
          <li><span class="everytown-red important">Intent & Outcome</span> – offers insight into the nature and aftermath of these events</li>
          <li><span class="everytown-red important">Number Killed & Wounded</span> – reveals the human toll in stark terms</li>
          <li><span class="everytown-red important">Narratives</span> – adds qualitative context to each incident where available</li>
        </ul>

        <!-- Methodology & Sources -->
        <h4 class="everytown-blue important">Methodology & Sources</h4>
        <p>
          <a href="https://everytownresearch.org/" class="source-link" target="_blank">Everytown Research</a> 
          continually updates these figures through news reports, law enforcement data, 
          and official records. Our dashboard fetches this dataset in near real-time 
          and applies a series of data transformations—cleaning, mapping state abbreviations, 
          and generating new columns for analysis. 
        </p>

        <!-- Tools & Technology -->
        <h4 class="everytown-blue important">Tools & Technology</h4>
        <ul>
          <li><b>Streamlit</b> – for the interactive UI</li>
          <li><b>Pandas</b> – for data cleaning and manipulation</li>
          <li><b>Plotly</b> – to create interactive visualizations</li>
          <li><b>Requests</b> – for fetching live CSV data from Everytown’s website</li>
        </ul>

        <!-- Limitations & Future Directions -->
        <h4 class="everytown-blue important">Limitations & Future Directions</h4>
        <p>
          Although this dashboard strives to provide a comprehensive and timely overview, 
          there are some inherent limitations:
        </p>
        <ul>
          <li><span class="everytown-red important">Partial 2025 Data</span> – The data for 2025 is still evolving and may not capture all incidents.</li>
          <li><span class="everytown-red important">Delayed Reporting</span> – Some incidents might be reported late or require verification.</li>
          <li><span class="everytown-red important">Geo-Coordinates</span> – Missing or inaccurate latitude/longitude values can affect the map analysis.</li>
          <li><span class="everytown-red important">Future Enhancements</span> – We plan to integrate more external datasets (e.g., demographic factors, local policies) for richer context.</li>
        </ul>

        <!-- Our Mission -->
        <h4 class="everytown-blue important">Our Mission</h4>
        <p>
          By transforming raw data into compelling, easy-to-understand visuals, this dashboard 
          endeavors to spark conversations and motivate meaningful changes to address gun violence 
          in schools.
        </p>

        <!-- A Call to Action -->
        <h4 class="everytown-blue important">A Call to Action</h4>
        <p>
          We invite policymakers, researchers, educators, and the general public to explore these findings. 
          Let every data point be a moment for reflection—and a step closer to collective action 
          in preventing further tragedies.
        </p>
        """,
        unsafe_allow_html=True
    )
