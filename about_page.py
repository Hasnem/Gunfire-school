import streamlit as st
from datetime import datetime

def about_page():
    """Display comprehensive about page with enhanced design and information."""
    
    # Page title
    st.title("About This Dashboard")
    
    # Calculate dynamic statistics
    current_year = datetime.now().year
    years_of_data = current_year - 2013  # Approximate start year
    
    # Main content with enhanced HTML and CSS
    about_html = f"""
    <style>
        /* Custom CSS for About Page */
        .about-container {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            line-height: 1.7;
            color: #2c3e50;
        }}
        
        /* Hero Section with Gradient */
        .hero-section {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 3rem;
            border-radius: 12px;
            margin-bottom: 3rem;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            position: relative;
            overflow: hidden;
        }}
        
        .hero-section::before {{
            content: "";
            position: absolute;
            top: -50%;
            right: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: pulse 4s ease-in-out infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ transform: scale(0.8); opacity: 0.5; }}
            50% {{ transform: scale(1.2); opacity: 0.8; }}
        }}
        
        .hero-section h2 {{
            margin: 0 0 1.5rem 0;
            font-size: 2.2rem;
            font-weight: 700;
            position: relative;
            z-index: 1;
        }}
        
        .hero-section p {{
            margin: 0;
            font-size: 1.2rem;
            opacity: 0.95;
            position: relative;
            z-index: 1;
            line-height: 1.8;
        }}
        
        /* Statistics Banner */
        .stats-banner {{
            background: #f8f9fa;
            padding: 2rem;
            border-radius: 10px;
            margin: 2rem 0;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 2rem;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        }}
        
        .stat-item {{
            padding: 1rem;
        }}
        
        .stat-number {{
            font-size: 2.5rem;
            font-weight: 700;
            color: #3498db;
            margin: 0;
            line-height: 1;
        }}
        
        .stat-label {{
            color: #7f8c8d;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-top: 0.5rem;
        }}
        
        /* Feature Grid */
        .feature-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 2rem;
            margin: 3rem 0;
        }}
        
        .feature-card {{
            background: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
            transition: all 0.3s ease;
            border-top: 4px solid #3498db;
            position: relative;
            overflow: hidden;
        }}
        
        .feature-card::before {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #3498db, #9b59b6);
            transform: scaleX(0);
            transition: transform 0.3s ease;
        }}
        
        .feature-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
        }}
        
        .feature-card:hover::before {{
            transform: scaleX(1);
        }}
        
        .feature-card h4 {{
            color: #2c3e50;
            margin: 0 0 1rem 0;
            font-size: 1.3rem;
            font-weight: 600;
        }}
        
        .feature-card p {{
            color: #5a6c7d;
            margin: 0;
            font-size: 1rem;
            line-height: 1.6;
        }}
        
        /* Info Sections */
        .info-section {{
            background: linear-gradient(135deg, #e8f4f8 0%, #d6f0f7 100%);
            border: 1px solid #3498db;
            padding: 2rem;
            border-radius: 10px;
            margin: 2.5rem 0;
            position: relative;
        }}
        
        .info-section::before {{
            content: "ℹ️";
            position: absolute;
            top: -15px;
            left: 20px;
            background: white;
            padding: 0 10px;
            font-size: 1.5rem;
        }}
        
        .info-section h3 {{
            color: #2c3e50;
            margin: 0 0 1.5rem 0;
            font-size: 1.5rem;
        }}
        
        /* Process Steps */
        .steps-list {{
            background: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
            margin: 2rem 0;
        }}
        
        .steps-list ol {{
            margin: 0;
            padding-left: 0;
            counter-reset: step-counter;
            list-style: none;
        }}
        
        .steps-list li {{
            margin: 1.5rem 0;
            padding-left: 3rem;
            position: relative;
            color: #34495e;
            line-height: 1.8;
        }}
        
        .steps-list li::before {{
            content: counter(step-counter);
            counter-increment: step-counter;
            position: absolute;
            left: 0;
            top: 0;
            background: #3498db;
            color: white;
            width: 2rem;
            height: 2rem;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 1rem;
        }}
        
        /* Warning Box */
        .warning-box {{
            background: linear-gradient(135deg, #fef5e7 0%, #fdebd0 100%);
            border-left: 5px solid #f39c12;
            padding: 1.5rem;
            margin: 2.5rem 0;
            border-radius: 8px;
            box-shadow: 0 3px 10px rgba(243, 156, 18, 0.1);
        }}
        
        .warning-box h4 {{
            color: #e67e22;
            margin: 0 0 1rem 0;
            font-size: 1.2rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        /* Technology Stack */
        .tech-stack {{
            background: #2c3e50;
            color: white;
            padding: 2.5rem;
            border-radius: 10px;
            margin: 2.5rem 0;
        }}
        
        .tech-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1.5rem;
            margin-top: 1.5rem;
        }}
        
        .tech-item {{
            text-align: center;
            padding: 1rem;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            transition: all 0.3s ease;
        }}
        
        .tech-item:hover {{
            background: rgba(255, 255, 255, 0.2);
            transform: translateY(-3px);
        }}
        
        .tech-icon {{
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }}
        
        .tech-name {{
            font-weight: 600;
            margin-bottom: 0.25rem;
        }}
        
        .tech-desc {{
            font-size: 0.85rem;
            opacity: 0.8;
        }}
        
        /* CTA Section */
        .cta-section {{
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
            padding: 3rem;
            border-radius: 12px;
            margin: 3rem 0;
            text-align: center;
            position: relative;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(17, 153, 142, 0.3);
        }}
        
        .cta-section::before {{
            content: "";
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 60%);
            animation: rotate 10s linear infinite;
        }}
        
        @keyframes rotate {{
            from {{ transform: rotate(0deg); }}
            to {{ transform: rotate(360deg); }}
        }}
        
        .cta-section h3 {{
            margin: 0 0 1.5rem 0;
            font-size: 2rem;
            position: relative;
            z-index: 1;
        }}
        
        .cta-section p {{
            margin: 0.5rem 0;
            font-size: 1.15rem;
            position: relative;
            z-index: 1;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }}
        
        /* Data Source Box */
        .data-source {{
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 2rem;
            border-radius: 10px;
            margin: 2.5rem 0;
            border: 1px solid #dee2e6;
            box-shadow: 0 3px 15px rgba(0, 0, 0, 0.08);
        }}
        
        .data-source h3 {{
            color: #2c3e50;
            margin: 0 0 1.5rem 0;
            font-size: 1.5rem;
        }}
        
        .data-source-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin-top: 1.5rem;
        }}
        
        .data-item {{
            padding: 1rem;
            background: white;
            border-radius: 6px;
            border-left: 3px solid #3498db;
        }}
        
        .data-item strong {{
            color: #2c3e50;
            display: block;
            margin-bottom: 0.5rem;
        }}
        
        /* Icon styling */
        .icon {{
            font-size: 1.8rem;
            margin-right: 0.75rem;
            vertical-align: middle;
            display: inline-block;
        }}
        
        /* Links */
        a {{
            color: #3498db;
            text-decoration: none;
            font-weight: 500;
            transition: all 0.2s ease;
        }}
        
        a:hover {{
            color: #2980b9;
            text-decoration: underline;
        }}
        
        /* Responsive Design */
        @media (max-width: 768px) {{
            .hero-section {{
                padding: 2rem;
            }}
            
            .hero-section h2 {{
                font-size: 1.8rem;
            }}
            
            .feature-grid {{
                grid-template-columns: 1fr;
                gap: 1.5rem;
            }}
            
            .stats-banner {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}
        
        /* Animations */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .fade-in {{
            animation: fadeIn 0.6s ease-out;
        }}
    </style>
    
    <div class="about-container">
        <!-- Hero Section -->
        <div class="hero-section fade-in">
            <h2>📊 Transforming Data into Actionable Insights for Safer Schools</h2>
            <p>
                Gun violence on school grounds is a critical public safety issue affecting communities 
                across America. This comprehensive dashboard transforms complex incident data into clear, 
                actionable insights that empower policymakers, educators, law enforcement, and communities 
                to develop evidence-based prevention strategies and save lives.
            </p>
        </div>
        
        <!-- Impact Statistics -->
        <div class="stats-banner">
            <div class="stat-item">
                <p class="stat-number">50+</p>
                <p class="stat-label">States Covered</p>
            </div>
            <div class="stat-item">
                <p class="stat-number">{years_of_data}+</p>
                <p class="stat-label">Years of Data</p>
            </div>
            <div class="stat-item">
                <p class="stat-number">1000s</p>
                <p class="stat-label">Schools Tracked</p>
            </div>
            <div class="stat-item">
                <p class="stat-number">Real-time</p>
                <p class="stat-label">Updates</p>
            </div>
        </div>
        
        <!-- Mission Statement -->
        <div class="info-section">
            <h3>Our Mission</h3>
            <p style="font-size: 1.1rem; line-height: 1.8;">
                We believe that data-driven insights are crucial for creating safer educational environments. 
                By making gun violence data accessible, understandable, and actionable, we aim to:
            </p>
            <ul style="font-size: 1.05rem; line-height: 1.8; margin-top: 1rem;">
                <li>Enable evidence-based policy decisions at local, state, and federal levels</li>
                <li>Help schools and communities identify risk patterns and implement targeted interventions</li>
                <li>Support researchers and advocates with comprehensive, reliable data analysis</li>
                <li>Foster informed public dialogue about school safety and gun violence prevention</li>
            </ul>
        </div>
        
        <!-- Key Features -->
        <h3 style="color: #2c3e50; margin: 3rem 0 2rem 0; font-size: 1.8rem;">
            <span class="icon">✨</span>Dashboard Capabilities
        </h3>
        <div class="feature-grid">
            <div class="feature-card">
                <h4><span class="icon">📈</span>Trend Analysis</h4>
                <p>Track incidents over time with yearly, monthly, and weekly breakdowns. 
                Identify patterns, seasonal variations, and long-term trends to inform 
                prevention strategies.</p>
            </div>
            
            <div class="feature-card">
                <h4><span class="icon">📍</span>Geographic Mapping</h4>
                <p>Explore interactive maps and detailed geographic breakdowns by state and city. 
                Understand regional patterns and identify areas requiring focused intervention.</p>
            </div>
            
            <div class="feature-card">
                <h4><span class="icon">⚠️</span>Severity Assessment</h4>
                <p>Analyze incident severity, casualty data, and outcome patterns. 
                Distinguish between different types of incidents to develop appropriate 
                response protocols.</p>
            </div>
            
            <div class="feature-card">
                <h4><span class="icon">📝</span>Narrative Analysis</h4>
                <p>Extract insights from incident descriptions using natural language processing. 
                Identify common themes, circumstances, and contributing factors.</p>
            </div>
            
            <div class="feature-card">
                <h4><span class="icon">📊</span>Real-time Filtering</h4>
                <p>Dynamically filter data by time period, location, severity, and other factors. 
                Create custom views tailored to specific research or policy needs.</p>
            </div>
            
            <div class="feature-card">
                <h4><span class="icon">📑</span>Executive Reports</h4>
                <p>Generate professional, comprehensive reports with a single click. 
                Perfect for briefings, grant applications, and stakeholder communications.</p>
            </div>
        </div>
        
        <!-- Data Source Information -->
        <div class="data-source">
            <h3><span class="icon">🔍</span>About the Data</h3>
            <p style="font-size: 1.05rem; margin-bottom: 1.5rem;">
                This dashboard is powered by comprehensive data from 
                <a href="https://everytownresearch.org/maps/gunfire-on-school-grounds/" 
                   target="_blank" style="font-weight: 600;">Everytown Research</a>, 
                a leading source for gun violence statistics and research.
            </p>
            
            <div class="data-source-grid">
                <div class="data-item">
                    <strong>📋 Coverage</strong>
                    All incidents where a firearm was brandished, fired, or a bullet hit school property
                </div>
                <div class="data-item">
                    <strong>🏫 Scope</strong>
                    K-12 schools and colleges across all U.S. states and territories
                </div>
                <div class="data-item">
                    <strong>🔄 Updates</strong>
                    Continuously updated as new incidents are reported and verified
                </div>
                <div class="data-item">
                    <strong>✅ Verification</strong>
                    Multi-source verification including media reports and official records
                </div>
            </div>
        </div>
        
        <!-- How to Use Guide -->
        <h3 style="color: #2c3e50; margin: 3rem 0 2rem 0; font-size: 1.8rem;">
            <span class="icon">🚀</span>Getting Started Guide
        </h3>
        <div class="steps-list">
            <ol>
                <li><strong>Review the Overview:</strong> Start on the dashboard home page to see 
                    key metrics, latest incidents, and overall statistics. This gives you a 
                    comprehensive snapshot of the current situation.</li>
                <li><strong>Apply Filters:</strong> Use the sidebar controls to focus on specific 
                    time periods, geographic regions, or incident types. You can combine multiple 
                    filters for precise analysis.</li>
                <li><strong>Explore Analysis Tabs:</strong> Navigate through Trends, Geography, 
                    Severity, and Narratives tabs to dive deep into different aspects of the data. 
                    Each tab provides unique insights and visualizations.</li>
                <li><strong>Interact with Visualizations:</strong> Hover over charts for detailed 
                    information, click on map regions for specifics, and use the dynamic controls 
                    to adjust views.</li>
                <li><strong>Generate Reports:</strong> Create professional executive summaries by 
                    selecting desired sections and clicking the generate button. Reports can be 
                    downloaded and shared.</li>
                <li><strong>Stay Updated:</strong> Check back regularly as new data is added. 
                    The dashboard automatically incorporates the latest verified incidents.</li>
            </ol>
        </div>
        
        <!-- Technology Stack -->
        <div class="tech-stack">
            <h3 style="color: white; margin: 0 0 1rem 0; text-align: center;">
                <span class="icon">⚙️</span>Built with Modern Technology
            </h3>
            <div class="tech-grid">
                <div class="tech-item">
                    <div class="tech-icon">🐍</div>
                    <div class="tech-name">Python</div>
                    <div class="tech-desc">Core language</div>
                </div>
                <div class="tech-item">
                    <div class="tech-icon">📊</div>
                    <div class="tech-name">Streamlit</div>
                    <div class="tech-desc">Web framework</div>
                </div>
                <div class="tech-item">
                    <div class="tech-icon">🐼</div>
                    <div class="tech-name">Pandas</div>
                    <div class="tech-desc">Data analysis</div>
                </div>
                <div class="tech-item">
                    <div class="tech-icon">📈</div>
                    <div class="tech-name">Plotly</div>
                    <div class="tech-desc">Visualizations</div>
                </div>
                <div class="tech-item">
                    <div class="tech-icon">🌍</div>
                    <div class="tech-name">Folium</div>
                    <div class="tech-desc">Mapping</div>
                </div>
                <div class="tech-item">
                    <div class="tech-icon">📝</div>
                    <div class="tech-name">NLTK</div>
                    <div class="tech-desc">Text analysis</div>
                </div>
            </div>
        </div>
        
        <!-- Important Considerations -->
        <div class="warning-box">
            <h4><span class="icon">⚠️</span>Important Considerations</h4>
            <ul style="margin: 1rem 0; line-height: 1.8;">
                <li><strong>Current Year Data:</strong> {current_year} data is incomplete and continuously 
                    updated. Avoid year-over-year comparisons with the current year.</li>
                <li><strong>Geographic Context:</strong> When comparing states or cities, consider 
                    differences in population size, school density, and reporting practices.</li>
                <li><strong>Data Sensitivity:</strong> Each data point represents real people affected 
                    by violence. Please handle this information with appropriate care and respect.</li>
                <li><strong>Reporting Variations:</strong> Some incidents may be underreported in 
                    certain regions due to differences in media coverage or reporting requirements.</li>
            </ul>
        </div>
        
        <!-- Use Cases -->
        <h3 style="color: #2c3e50; margin: 3rem 0 2rem 0; font-size: 1.8rem;">
            <span class="icon">💡</span>Who Uses This Dashboard
        </h3>
        <div class="feature-grid">
            <div class="feature-card">
                <h4>📚 Educators & Administrators</h4>
                <p>Understand risks, benchmark against similar schools, and develop evidence-based 
                safety protocols tailored to their specific context.</p>
            </div>
            
            <div class="feature-card">
                <h4>🏛️ Policymakers</h4>
                <p>Access reliable data for legislation, allocate resources effectively, and 
                track the impact of policy interventions over time.</p>
            </div>
            
            <div class="feature-card">
                <h4>🔬 Researchers</h4>
                <p>Analyze comprehensive datasets, identify trends for academic studies, and 
                contribute to the growing body of violence prevention research.</p>
            </div>
            
            <div class="feature-card">
                <h4>👮 Law Enforcement</h4>
                <p>Identify patterns for resource deployment, develop targeted interventions, 
                and coordinate multi-agency response strategies.</p>
            </div>
            
            <div class="feature-card">
                <h4>📰 Journalists</h4>
                <p>Access accurate, up-to-date statistics for reporting, understand context 
                beyond individual incidents, and inform public discourse.</p>
            </div>
            
            <div class="feature-card">
                <h4>👨‍👩‍👧‍👦 Community Members</h4>
                <p>Stay informed about local safety, advocate for evidence-based solutions, 
                and participate in community safety initiatives.</p>
            </div>
        </div>
        
        <!-- Call to Action -->
        <div class="cta-section">
            <h3>🎯 Making a Measurable Difference</h3>
            <p>
                Every insight gained from this data has the potential to prevent future tragedies. 
                By understanding patterns, identifying risk factors, and implementing evidence-based 
                interventions, we can work together to create safer learning environments.
            </p>
            <p style="font-weight: 700; margin-top: 2rem; font-size: 1.3rem;">
                Together, we can turn data into action and action into safer schools.
            </p>
        </div>
        
        <!-- Privacy and Ethics -->
        <div class="info-section">
            <h3>🔒 Privacy and Ethical Considerations</h3>
            <p>This dashboard is committed to responsible data use:</p>
            <ul style="line-height: 1.8; margin-top: 1rem;">
                <li>No personally identifiable information about victims or perpetrators is displayed</li>
                <li>Data is aggregated to protect individual privacy while maintaining statistical accuracy</li>
                <li>All information is sourced from publicly available reports and official records</li>
                <li>We follow ethical guidelines for presenting sensitive violence-related data</li>
            </ul>
        </div>
        
        <!-- Contact and Support -->
        <div class="data-source">
            <h3><span class="icon">📧</span>Get Involved</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem; margin-top: 1.5rem;">
                <div>
                    <h4 style="color: #2c3e50; margin-bottom: 1rem;">For Researchers</h4>
                    <p>Access raw data and methodology documentation at 
                    <a href="https://everytownresearch.org" target="_blank">Everytown Research</a></p>
                </div>
                <div>
                    <h4 style="color: #2c3e50; margin-bottom: 1rem;">For Developers</h4>
                    <p>Contribute to this open-source project on
                    <a href="https://github.com/hasnem/Gunfire-school" target="_blank">GitHub</a></p>
                </div>
                <div>
                    <h4 style="color: #2c3e50; margin-bottom: 1rem;">For Feedback</h4>
                    <p>Share suggestions, report issues, or request features through our 
                    feedback channels</p>
                </div>
            </div>
        </div>
    </div>
    """
    
    # Render the HTML content
    st.html(about_html)
    
    # Footer with additional links
    st.markdown("---")
    
    # Three-column footer
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📚 Resources")
        st.markdown("""
        - [Everytown Research](https://everytownresearch.org)
        - [Gun Violence Archive](https://www.gunviolencearchive.org)
        - [K-12 School Shooting Database](https://k12ssdb.org)
        """)
    
    with col2:
        st.markdown("### 🛡️ Prevention")
        st.markdown("""
        - [Sandy Hook Promise](https://www.sandyhookpromise.org)
        - [Safe Schools Initiative](https://www.secretservice.gov)
        - [NASP School Safety](https://www.nasponline.org)
        """)
    
    with col3:
        st.markdown("### 📖 Learn More")
        st.markdown("""
        - [Understanding the Data](https://everytownresearch.org/methodology/)
        - [School Safety Best Practices](#)
        - [Crisis Response Resources](#)
        """)
    
    # Final disclaimer
    st.caption("""
    **Disclaimer:** This dashboard is an independent analysis tool. While we strive for accuracy, 
    please verify critical information with original sources. For the most current research and 
    resources, visit [Everytown Research](https://everytownresearch.org).
    
    Last updated: {:%B %Y}
    """.format(datetime.now()))