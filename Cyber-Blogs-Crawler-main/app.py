from flask import Flask, render_template, jsonify
import praw
import datetime as dt

app = Flask(__name__)

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

print("CLIENT_ID:",client_id)
print("CLIENT_SECRET:",client_secret)

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

# Severity keywords
HIGH_SEVERITY = [
    "ransomware", "data breach", "APT", "zero-day", "critical", 
    "exploit", "RCE", "compromise", "attack", "incident"
]

MEDIUM_SEVERITY = [
    "vulnerability", "CVE", "patch", "risk", "malware", "phishing",
    "threat intelligence", "forensics"
]

LOW_SEVERITY = [
    "security", "firewall", "encryption", "authentication", 
    "compliance", "testing", "forensics", "OSINT"
]

def detect_severity(title):
    """Detect severity level (LOW, MEDIUM, HIGH) based on keywords"""
    title_lower = title.lower()
    
    # Check high severity keywords
    for keyword in HIGH_SEVERITY:
        if keyword.lower() in title_lower:
            print(f"✓ HIGH severity detected: '{keyword}' in '{title}'")
            return "HIGH"
    
    # Check medium severity keywords
    for keyword in MEDIUM_SEVERITY:
        if keyword.lower() in title_lower:
            print(f"✓ MEDIUM severity detected: '{keyword}' in '{title}'")
            return "MEDIUM"
    
    # Default to low severity
    print(f"✓ LOW severity (default) for '{title}'")
    return "LOW"

@app.route('/')
def home():
    return render_template('dashboard.html')

@app.route('/fetch_posts')
def fetch_posts():
    posts = []
    count = 0
    print("\n🔄 Fetching posts with severity detection...\n")
    
    # Increase limit to 50 for more posts
    for idx, submission in enumerate(subreddit.new(limit=1500), start=1):
        title = submission.title.lower()
        found_keywords = [k for k in keywords if k in title]
        if found_keywords:
            severity = detect_severity(submission.title)
            count += 1
            post_data = {
                'title': f"{count}. {submission.title}",
                'url': submission.url,
                'score': submission.score,
                'keywords': found_keywords,
                'severity': severity
            }
            posts.append(post_data)
            print(f"Post #{count}: {submission.title[:50]}... → {severity}")
    
    print(f"\n✅ Total posts found: {count}\n")
    return jsonify({'posts': posts})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # this line is the key
    app.run(host="0.0.0.0", port=port)



