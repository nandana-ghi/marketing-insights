import pandas as pd


df = pd.read_csv("campaigns.csv")


print(df.head())   
print(df.info())   


df = df.drop_duplicates()                          
df["clicks"] = df["clicks"].fillna(df["clicks"].median())
df["clicks"] = df["clicks"].astype(int)             
df["date"] = pd.to_datetime(df["date"])            

print("\nCleaned data:")
print(df)
import sqlite3


conn = sqlite3.connect("campaigns.db")
df.to_sql("campaigns", conn, if_exists="replace", index=False)


query1 = """
SELECT campaign_name, SUM(conversions) AS total_conversions
FROM campaigns
GROUP BY campaign_name
ORDER BY total_conversions DESC
LIMIT 5
"""
print("\nTop campaigns:")
print(pd.read_sql_query(query1, conn))


query2 = """
SELECT channel, ROUND(SUM(spend) * 1.0 / SUM(clicks), 2) AS cost_per_click
FROM campaigns
GROUP BY channel
"""
print("\nCost per click by channel:")
print(pd.read_sql_query(query2, conn))

summary = pd.read_sql_query("""
SELECT campaign_name, channel,
       SUM(impressions) AS impressions,
       SUM(clicks) AS clicks,
       SUM(spend) AS spend,
       SUM(conversions) AS conversions
FROM campaigns
GROUP BY campaign_name, channel
""", conn)

summary["ctr"] = (summary["clicks"] / summary["impressions"] * 100).round(2)
summary["cpc"] = (summary["spend"] / summary["clicks"]).round(2)
summary["conversion_rate"] = (summary["conversions"] / summary["clicks"] * 100).round(2)
summary["cost_per_conversion"] = (summary["spend"] / summary["conversions"]).round(2)

print("\nCampaign metrics:")
print(summary)

import os
import json
from google import genai


client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


data_json = summary.to_json(orient="records")

prompt = f"""You are a marketing analyst. Here is campaign performance data as JSON:
{data_json}

Return ONLY a JSON object with these keys:
- "summary": a 2-3 sentence overview of performance
- "top_insight": the single most important finding
- "problem_campaigns": a list of campaign names that are performing poorly
- "suggested_ad_copy": a list of 3 short ad headlines for the best campaign
"""

response = client.models.generate_content(
    model="gemini-flash-latest",
    contents=prompt,
    config={"response_mime_type": "application/json"},
)

result = json.loads(response.text)
print("\nAI insights:")
print(json.dumps(result, indent=2))

with open("report.md", "w", encoding="utf-8") as f:
    f.write("# Marketing Campaign Insights\n\n")
    f.write(f"## Summary\n{result['summary']}\n\n")
    f.write(f"## Top Insight\n{result['top_insight']}\n\n")
    f.write("## Campaigns Needing Attention\n")
    for name in result["problem_campaigns"]:
        f.write(f"- {name}\n")
    f.write("\n## Suggested Ad Copy\n")
    for line in result["suggested_ad_copy"]:
        f.write(f"- {line}\n")

print("\nReport saved to report.md")
