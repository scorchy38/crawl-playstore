import pandas as pd
import openai
from google_play_scraper import search, app as gplay_app
from dotenv import load_dotenv
import os

# Load API key from .env file
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# Define the categories to search from
target_categories = [
    'ecommerce', 'music/podcast streaming', 'fintech',
    'food delivery', 'utility', 'mobile dashboards'
]


def categorize_app(app_name, app_description):
    prompt = f"Categorize the following app into one of the categories: ecommerce, music/podcast streaming, fintech, food delivery, utility, mobile dashboards.\n\nApp Name: {app_name}\nDescription: {app_description}\n\nCategory:"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=10
    )
    app_category = response.choices[0].message['content'].strip().lower()
    return app_category


apps_data = []

search_terms = ["ecommerce", "music", "podcast", "fintech", "food delivery", "utility", "budgeting", "notes",
                "mobile dashboards"]
for term in search_terms:
    results = search(term, lang='en', country='us', n_hits=200)

    for result in results:
        try:
            app_id = result['appId']
            details = gplay_app(app_id, lang='en', country='us')

            name = details['title']
            description = details['description']
            downloads = int(details['installs'].replace(',', '').replace('+', ''))
            developer_email = details.get('developerEmail', 'N/A')

            if downloads < 100000:
                category = categorize_app(name, description)
                if category in target_categories:
                    apps_data.append({
                        'App Name': name,
                        'Description': description,
                        'Downloads': downloads,
                        'Developer Email': developer_email,
                        'Category': category
                    })
        except Exception as e:
            print(f"Error fetching details for {result['appId']}: {e}")

df = pd.DataFrame(apps_data)
df.to_excel('filtered_apps.xlsx', index=False)
print("Data saved to filtered_apps.xlsx")
