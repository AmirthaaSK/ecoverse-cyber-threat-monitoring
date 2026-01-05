import praw
import datetime as dt
import time
from praw.exceptions import PRAWException, ClientException, RedditAPIException

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
seen_posts = set()
count = 0
while True:
    print(f"\n🔄 Fetching posts at {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}...\n")
    
    try:
        for submission in subreddit.new(limit=20):  # Adjust limit as needed
            if submission.id in seen_posts:
                continue  # Skip if already seen
            seen_posts.add(submission.id)
            
            title = submission.title.lower()
            found_keywords = [k for k in keywords if k in title]
            if found_keywords:
                count += 1
                print(f"🔍 Post #{count}:")
                print(f"📌 Title: {submission.title}")
                print(f"   👍 Score: {submission.score}")
                print(f"   🔗 URL: {submission.url}")
                print(f"   🧠 Keywords Found: {', '.join(found_keywords)}\n")
    
    except ClientException as e:
        print(f"⚠️ ClientException occurred: {e}")
        print("⏳ Retrying in 60 seconds...")
    
    except RedditAPIException as e:
        print(f"⚠️ RedditAPIException occurred: {e}")
        print("⏳ Retrying in 60 seconds...")
    
    except PRAWException as e:
        print(f"⚠️ PRAWException occurred: {e}")
        print("⏳ Retrying in 60 seconds...")
    
    except Exception as e:
        print(f"⚠️ An unexpected error occurred: {e}")
        print("⏳ Retrying in 60 seconds...")
    
    print("⏳ Waiting 60 seconds before next fetch...\n")
    time.sleep(60)

