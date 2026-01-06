# 🛡️ Cybersecurity Incident Dashboard

A real-time web dashboard that visualizes cybersecurity incidents with live charts, keyword detection, and keyword-based search, complete with a dark mode toggle and animated preloader.

![Dashboard Preview](demo1.png "Cybersecurity Dashboard Screenshot")

## To  View Live
https://cyber-blogs-crawler.onrender.com/

## 🔥 🚀 Features

📊 Live Charts: Visualize incident types and frequency over time using Chart.js.

🔍 Search Functionality: Filter incidents based on keywords or titles.

🌙 Dark Mode: Toggle between light and dark themes for better usability.

🔄 Auto Refresh: Automatically fetches new incident data every 60 seconds.

⏳ Preloader: Smooth animated spinner with loading message during data fetch.

📅 Last Updated Time: Displays the most recent data fetch timestamp.

📱 Responsive Design: Works seamlessly across desktop and mobile devices.

♿ Accessible UI: Clear color contrast and readable layouts.

🔔 Alert System 
Automatically triggers alerts when incident counts cross predefined thresholds.
Supports multiple alert categories (General, Malware, Ransomware, Data Breach).
Alerts are color-coded and can be dismissed individually or all at once.

🚦 Severity Level Classification 

Each incident is classified as LOW, MEDIUM, HIGH, or CRITICAL.
Severity is assigned based on keyword type and incident impact.
Enables quick prioritization of critical threats by analysts.
---

## 🚀  Frontend

HTML5 – Structure and layout of the dashboard
CSS3 – Responsive styling with CSS Variables for theming
JavaScript (ES6+) – Dynamic UI updates and data handling
Chart.js – Live visualization of incident types and trends

⚙️ Backend

Python – Core logic for data processing and rule-based detection
Flask – Lightweight web framework to serve APIs and dashboard data

🧠 Intelligence & Logic

Rule-Based Engine – Keyword detection, incident classification, severity assignment, and alert triggering
Threshold-Based Alerting – Generates alerts when incident counts exceed safe limits

---

## 📁 Folder Structure
cybersecurity-dashboard/
│
├── app.py                     # 🔁 Main Flask (Python) backend file
│
├── 📁 templates/              # 🖼️ HTML files served via Flask
│   └── index.html 


---

## ⚙️ Setup Instructions

### 1. Clone or Download
```bash
git clone https://github.com/your-username/cybersecurity-dashboard.git
cd cybersecurity-dashboard

GET /fetch_posts
{
  "posts": [
    {
      "title": "Example Incident",
      "url": "https://example.com",
      "score": 42,
      "keywords": ["malware", "ransomware"],
      "timestamp": "2025-07-07T15:30:00Z"
    }
  ]
}

python app.py

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/fetch_posts")
def fetch_posts():
    # Replace with actual data fetching logic
    return {"posts": [...]}

