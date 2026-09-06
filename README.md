◉ Percepta
AI-Powered Accessibility for Data Visualizations

Percepta is an AI-powered accessibility tool that helps make data visualizations easier to understand for people with Color Vision Deficiency (CVD).

Many charts and dashboards rely heavily on color to communicate information. When two colors appear similar to someone with CVD, important information can become difficult to interpret.

Percepta addresses this problem by analyzing visualizations and adding multiple visual cues such as:

Colorblind-friendly color palettes
Different patterns and visual styles
Clear labels
Improved contrast
CVD simulation
Accessibility scoring
AI-generated explanations
How Percepta Works
Upload Chart / Dataset
          ↓
Analyze Colors & Contrast
          ↓
Simulate CVD
          ↓
Detect Accessibility Issues
          ↓
Generate Improved Visualization
          ↓
Calculate Accessibility Score
          ↓
Generate AI Explanation

Key Features
CVD Simulation

Percepta simulates how a visualization may appear under:

Protanopia
Deuteranopia
Tritanopia
Accessibility Analysis

The system checks for potentially problematic:

Similar colors
Low contrast
Color-dependent information
Accessible Visualization

Percepta improves visualizations using multiple cues instead of relying only on color:

Shapes
Patterns
Labels
Contrast
Colorblind-friendly palettes
Accessibility Score

Each visualization receives an accessibility score from 0 to 100.

The score provides a quick indication of how accessible the visualization is.

AI Explanation

Percepta provides a simple explanation of:

What accessibility problems were detected
What was changed
Why the changes improve accessibility
Healthcare Use Case

Medical dashboards often use colors such as green, yellow, and red to represent patient status.

For example:

Before:

🟢 Stable
🟡 Monitor
🔴 Critical


Percepta can introduce additional visual cues:

After:

● Stable
▲ Monitor
■ Critical


This means the information remains distinguishable even when color perception is limited.

Technology Stack
Frontend
Streamlit
Backend / Processing
Python
Data & Visualization
Pandas
Matplotlib
NumPy
OpenCV
AI
Large Language Model for accessibility explanations
Project Structure
percepta/
│
├── app.py
├── requirements.txt
├── README.md
│
└── modules/
    ├── cvd.py
    ├── analysis.py
    ├── visualization.py
    ├── scoring.py
    └── ai.py

Running the Project

Install the required dependencies:

pip install -r requirements.txt


Run the Streamlit application:

streamlit run app.py

Expected Outcome

The prototype allows users to:

Upload a chart or dataset.
Analyze potential accessibility problems.
Simulate different types of CVD.
Generate a more accessible visualization.
View an accessibility score.
Read an AI-generated explanation of the improvements.
Hackathon Project

Percepta aims to make data visualizations more inclusive by ensuring that important information is communicated through more than color alone.
