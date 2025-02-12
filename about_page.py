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
          Gunfire on school grounds remains a pressing concern that calls for clear, data-driven insights. 
          This dashboard draws upon 
          <a href="https://everytownresearch.org/maps/gunfire-on-school-grounds/" class="source-link" target="_blank">
          Everytown Research</a>
          to highlight the frequency, location, and nature of these incidents over time. 
          By making these patterns visible, we aim to equip policymakers, educators, researchers, 
          and the public with actionable knowledge to enhance school safety.
        </p>

        <!-- Data Coverage & Story -->
        <h3 class="everytown-blue important">Our Data Story</h3>
        <p>
          Each interactive chart provides a different lens on the data:
        </p>
        <ul>
          <li><span class="everytown-red important">Yearly, Monthly, and Day-of-Week Trends</span> – Pinpoint temporal shifts and possible seasonal or day patterns.</li>
          <li><span class="everytown-red important">Intent & Outcome Distribution</span> – Understand the nature of incidents, including motives and their aftermath.</li>
          <li><span class="everytown-red important">Geographical Analyses</span> – Spot regional hotspots at both state and city levels, and examine potential policy or population factors.</li>
          <li><span class="everytown-red important">Top Tragic Incidents</span> – Identify incidents with the highest casualties for deeper reflection and potential lessons.</li>
        </ul>
        <p>
          By linking raw facts to dynamic visuals, our goal is to emphasize the real communities 
          behind each statistic, prompting constructive dialogue and targeted solutions.
        </p>

        <!-- Data Contents -->
        <h3 class="everytown-blue important">Behind the Numbers</h3>
        <p>
          The dataset from Everytown includes:
        </p>
        <ul>
          <li><span class="everytown-red important">Date, City, & State</span> – situating each event in time and space</li>
          <li><span class="everytown-red important">Latitude/Longitude</span> – enabling precise mapping of incidents</li>
          <li><span class="everytown-red important">Intent & Outcome</span> – revealing the nature and aftermath of each incident</li>
          <li><span class="everytown-red important">Casualties (Killed & Wounded)</span> – quantifying the direct human toll</li>
          <li><span class="everytown-red important">Narratives</span> – offering contextual background behind each incident</li>
        </ul>

        <!-- Methodology & Process -->
        <h3 class="everytown-blue important">Our Methodology & Process</h3>
        <p>
          We fetch the latest CSV data directly from Everytown's site in near real time, 
          and carry out key transformations:
        </p>
        <ul>
          <li><span class="everytown-red important">Data Cleaning</span> – removing invalid coordinates and irrelevant fields</li>
          <li><span class="everytown-red important">Column Enhancements</span> – creating new columns (Year, Month, Day-of-Week, etc.) for deeper analysis</li>
          <li><span class="everytown-red important">Dynamic Filtering</span> – allowing users to refine the data by date range, state, intent, or a minimum casualties threshold</li>
          <li><span class="everytown-red important">Interactive Visualizations</span> – plotting incidents, casualties, and distributions using 
              <b>Plotly</b> and serving them through <b>Streamlit</b></li>
        </ul>
        <p>
          Every chart is dynamically updated based on user-selected filters, presenting 
          the most relevant insights instantly. The underlying approach is transparent, 
          letting the data speak while providing narrative context.
        </p>

        <!-- Tools & Technology -->
        <h3 class="everytown-blue important">Tools & Technology</h3>
        <p>
          <b>Streamlit</b> drives the dashboard's interactivity, 
          <b>Pandas</b> handles data wrangling, and 
          <b>Plotly</b> delivers the interactive graphs and maps. 
          This combination ensures intuitive exploration and real-time updates without complex setup.
        </p>

        <!-- Limitations & Future Directions -->
        <h3 class="everytown-blue important">Limitations & Future Directions</h3>
        <ul>
          <li><span class="everytown-red important">Partial Data</span> – Some years, such as 2025, may still be incomplete as incidents are confirmed or added.</li>
          <li><span class="everytown-red important">Delayed Reporting</span> – Late or unverified incidents might not appear in the dataset immediately.</li>
          <li><span class="everytown-red important">Geographic Accuracy</span> – Missing or approximate coordinates can affect the precision of maps.</li>
          <li><span class="everytown-red important">Further Enhancements</span> – Incorporating demographic or policy data could uncover deeper correlations (e.g., legislative context, population density).</li>
        </ul>

        <!-- Overall Mission -->
        <h3 class="everytown-blue important">Why This Matters</h3>
        <p>
          Each data point represents a real-world tragedy, reminding us that preventative strategies 
          and informed policies are crucial. By highlighting patterns—when, where, and how these 
          incidents occur—the dashboard encourages data-driven conversations about how to protect 
          students, educators, and communities.
        </p>

        <!-- Call to Action -->
        <h3 class="everytown-blue important">Call to Action</h3>
        <p>
          We invite you to explore the trends, filters, and observations to glean insights 
          into possible preventive measures and resource allocations. 
          Only through awareness and collaboration can we hope to reduce these incidents 
          and maintain safer learning environments for everyone.
        </p>
        """,
        unsafe_allow_html=True
    )
