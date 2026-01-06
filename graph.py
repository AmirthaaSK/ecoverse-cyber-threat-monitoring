import praw
import matplotlib.pyplot as plt
import io
import base64
from collections import defaultdict
import plotly.graph_objects as go

import os
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv('REDDIT_CLIENT_ID')
client_secret = os.getenv('REDDIT_CLIENT_SECRET')
user_agent = os.getenv('REDDIT_USER_AGENT')

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)

# Subreddit and keywords
subreddit = reddit.subreddit("cybersecurity")

keywords = [
    "cybersecurity", "malware", "phishing", "ransomware", "data breach",
    "vulnerability", "exploit", "threat intelligence", "incident response",
    "penetration testing", "network security", "firewall",
    "encryption", "authentication", "access control",
    "zero trust", "compliance", "risk management", "APT", "OSINT",
    "CVE", "patch management", "cloud security", "API security",
    "IoT security", "cryptography", "bug bounty", "forensics",
    "red team", "blue team", "DevSecOps", "DLP", "insider threat",
    "social engineering", "zero-day", "DNS security", "SSL/TLS"
]

def fetch_posts():
    posts = []
    count = 0
    for submission in subreddit.new(limit=1500):
        title = submission.title.lower()
        found_keywords = [k for k in keywords if k in title]
        if found_keywords:
            count += 1
            posts.append({
                'title': f"{count}. {submission.title}",
                'url': submission.url,
                'score': submission.score,
                'keywords': found_keywords
            })
    return posts

def generate_bar_chart(posts_data):
    # Sort posts by score in descending order and select the top 10
    top_posts = sorted(posts_data, key=lambda x: x['score'], reverse=True)[:10]
    titles = [post['title'] for post in top_posts]
    scores = [post['score'] for post in top_posts]

    # Create interactive bar chart with hover effects using plotly
    fig = go.Figure(go.Bar(
        x=scores,
        y=titles,
        orientation='h',
        hoverinfo='x+y+text',
        text=scores,  # Show score on hover
        marker=dict(color='skyblue')
    ))

    fig.update_layout(
        title='Top 10 Cybersecurity Reddit Posts by Score',
        xaxis_title='Score (Likes)',
        yaxis_title='Post Titles',
        hoverlabel=dict(bgcolor='white', font_size=13),
        height=600
    )

    fig.show()

def generate_pie_chart(posts_data):
    keyword_count = defaultdict(int)
    for post in posts_data:
        for kw in post['keywords']:
            keyword_count[kw] += 1

    # Group keywords into 5 categories
    categories = {
        'Threat Detection': ['cybersecurity', 'malware', 'exploit', 'ransomware'],
        'Access Control': ['authentication', 'access control', 'zero trust', 'firewall'],
        'Risk Management': ['compliance', 'risk management', 'incident response', 'penetration testing'],
        'Data Protection': ['encryption', 'data breach', 'patch management', 'DLP'],
        'Advanced Topics': ['APT', 'OSINT', 'CVE', 'IoT security', 'cloud security']
    }

    # Group keyword counts into categories
    category_counts = {category: sum(keyword_count.get(kw, 0) for kw in keywords) for category, keywords in categories.items()}

    # Plot pie chart using plotly for interactive display
    fig = go.Figure(go.Pie(
        labels=list(category_counts.keys()),
        values=list(category_counts.values()),
        hoverinfo='label+percent',
        textinfo='percent+label',  # Display percentage along with the label
        marker=dict(colors=['#FF9999','#66B2FF','#99FF99','#FFCC99','#FF6666'])
    ))

    fig.update_layout(
        title='Top 5 Cybersecurity Keyword Categories',
        height=600
    )

    fig.show()

# Fetch posts and generate charts
posts_data = fetch_posts()

# Generate Bar Chart and Pie Chart
generate_bar_chart(posts_data)
generate_pie_chart(posts_data)
