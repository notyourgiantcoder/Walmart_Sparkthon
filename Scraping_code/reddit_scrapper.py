import praw
import pandas as pd
from datetime import datetime

RETAIL_KEYWORDS = ["inventory", "supply chain", "restock", "POS", "store", "merchandise", "logistics"]

# === API CONFIG ===
reddit = praw.Reddit(
    client_id="YOUR_ID",
    client_secret="YOUR_SECRET",
    user_agent="retail_scraper/0.1"
)

# === Retail-focused subreddits ===
subreddits = [
    "walmart", "Target", "Costco", "retail", "RetailHell",
    "smallbusiness", "retailnews"
]

results = []

for subreddit_name in subreddits:
    subreddit = reddit.subreddit(subreddit_name)
    for post in subreddit.search(" OR ".join(RETAIL_KEYWORDS), limit=50):
        post_data = {
            'subreddit': subreddit_name,
            'title': post.title,
            'text': post.selftext,
            'score': post.score,
            'comments': post.num_comments,
            'created': datetime.utcfromtimestamp(post.created_utc).isoformat(),
            'url': post.url
        }
        results.append(post_data)

df = pd.DataFrame(results)
df.to_csv("output/reddit_trends.csv", index=False)
print(f"✅ Saved {len(df)} retail-focused Reddit posts.")
