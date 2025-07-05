from googleapiclient.discovery import build
import pandas as pd

# === API CONFIG ===
youtube = build("youtube", "v3", developerKey="YOUR_YOUTUBE_API_KEY")

RETAIL_QUERIES = [
    "retail trends", "supply chain management", "Walmart restock", 
    "last mile delivery", "inventory optimization"
]

results = []

for query in RETAIL_QUERIES:
    request = youtube.search().list(
        q=query,
        part="snippet",
        type="video",
        maxResults=20,
        order="relevance"
    )
    response = request.execute()

    for item in response['items']:
        video = {
            "query": query,
            "title": item['snippet']['title'],
            "description": item['snippet'].get('description', ''),
            "channel": item['snippet']['channelTitle'],
            "publishedAt": item['snippet']['publishedAt'],
            "videoId": item['id']['videoId'],
            "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}"
        }
        results.append(video)

df = pd.DataFrame(results)
df.to_csv("output/youtube_trends.csv", index=False)
print(f"✅ Saved {len(df)} retail-focused YouTube videos.")
