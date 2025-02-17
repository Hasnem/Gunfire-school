import streamlit as st

def about_page():
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
        <h3 class="everytown-blue important">Project Motivation</h3>
        <p>
          Gunfire on school grounds is a stark reality that demands careful, data-driven attention.
          This dashboard leverages
          <a href="https://everytownresearch.org/maps/gunfire-on-school-grounds/" class="source-link" target="_blank">
          Everytown Research</a>
          to illuminate the frequency, location, nature, and context of these incidents over time.
          Our goal is to empower policymakers, educators, researchers, and the public with insights 
          that inform strategies for safer schools.
        </p>

        <!-- Data Coverage & Story -->
        <h3 class="everytown-blue important">Our Data Story</h3>
        <p>
          We present multiple interactive perspectives:
        </p>
        <ul>
          <li><span class="everytown-red important">Temporal Trends:</span> Yearly, monthly, and day-of-week patterns indicate shifts and possible seasonal effects.</li>
          <li><span class="everytown-red important">Intent & Outcome Distributions:</span> Explore key contributing motives and impacts.</li>
          <li><span class="everytown-red important">Geographical Overviews:</span> Track state-level hot spots and city-level concentrations.</li>
          <li><span class="everytown-red important">Notable Incidents:</span> Highlight high-casualty events for deeper reflection and potential lessons.</li>
          <li><span class="everytown-red important">Narrative Text Analysis:</span> Examine word clouds and age references for extra context on who’s involved and how.</li>
        </ul>
        <p>
          By connecting raw facts to dynamic visuals, we underscore the communities behind every data point, 
          fostering constructive dialogue and more effective solutions.
        </p>

        <!-- Data Contents -->
        <h3 class="everytown-blue important">Behind the Numbers</h3>
        <p>
          The dataset from Everytown includes:
        </p>
        <ul>
          <li><span class="everytown-red important">Date, City, & State</span> – placing each event in time and location</li>
          <li><span class="everytown-red important">Latitude/Longitude</span> – supporting precise mapping</li>
          <li><span class="everytown-red important">Intent & Outcome</span> – clarifying motives and consequences</li>
          <li><span class="everytown-red important">Casualties (Killed & Wounded)</span> – capturing the direct toll</li>
          <li><span class="everytown-red important">Narratives</span> – giving more context behind each incident</li>
        </ul>

        <!-- Methodology & Process -->
        <h3 class="everytown-blue important">Our Methodology & Process</h3>
        <p>
          We fetch near real-time CSV data from Everytown and transform it for analysis:
        </p>
        <ul>
          <li><span class="everytown-red important">Data Cleaning</span> – removing invalid coordinates and irrelevant fields</li>
          <li><span class="everytown-red important">Column Enhancements</span> – adding Year, Month, Day-of-Week, etc., for deeper insights</li>
          <li><span class="everytown-red important">Dynamic Filtering</span> – refining the dataset by time range, state, intent, or casualties</li>
          <li><span class="everytown-red important">Interactive Visualizations</span> – leveraging
              <b>Plotly</b> and <b>Streamlit</b> for instant, filter-responsive charts 
          </li>
          <li><span class="everytown-red important">Narrative Analysis</span> – generating word clouds and extracting common ages mentioned</li>
        </ul>
        <p>
          Each chart updates based on user filters, offering timely, customizable insight. 
          Our goal is to let the data speak while adding just enough context for clarity.
        </p>

        <!-- Tools & Technology -->
        <h3 class="everytown-blue important">Tools & Technology</h3>
        <p>
          <b>Streamlit</b> drives the interactive interface,
          <b>Pandas</b> powers data processing, and
          <b>Plotly</b> produces engaging visualizations.
          This combination keeps analysis flexible and responsive without heavy setup.
        </p>

        <!-- Limitations & Future Directions -->
        <h3 class="everytown-blue important">Limitations & Future Directions</h3>
        <ul>
          <li><span class="everytown-red important">Partial Data</span> – Some recent years (e.g., 2025) may be incomplete as incidents await verification.</li>
          <li><span class="everytown-red important">Delayed Reporting</span> – Late or unverified cases can slip through or appear after the fact.</li>
          <li><span class="everytown-red important">Geographic Accuracy</span> – Missing or approximate coordinates may affect map precision.</li>
          <li><span class="everytown-red important">Expanded Analysis</span> – Integrating policy or demographic data (e.g., local gun laws, population densities) could reveal deeper correlations.</li>
        </ul>

        <!-- Why It Matters -->
        <h3 class="everytown-blue important">Why This Matters</h3>
        <p>
          Each entry in this dataset represents a tragic real-world occurrence, underscoring the need 
          for evidence-based prevention and policies. By spotlighting recurring patterns—timing, locations, 
          and contributing factors—the dashboard encourages informed discussions on enhancing safety 
          for students and educators alike.
        </p>

        <!-- Call to Action -->
        <h3 class="everytown-blue important">Call to Action</h3>
        <p>
          We encourage you to explore the visuals, adjust the filters, and delve into observations 
          on intent, geography, and textual narratives. Data alone can’t solve the issue, but 
          transparency and informed debate form a critical step in developing effective strategies 
          for safer school communities.
        </p>
        """,
        unsafe_allow_html=True
    )
