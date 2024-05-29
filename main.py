from google_play_scraper import search, app
from openpyxl import Workbook
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

target_search_terms = {
    'ecommerce': 'shopping',
    'music/podcast streaming': 'music streaming',
    'fintech': 'finance',
    'food delivery': 'food delivery',
    'utility': 'productivity',
    'mobile dashboards': 'business'
}

wb = Workbook()
ws = wb.active
ws.title = "Apps Data"

header = ['App Name', 'Description', 'Downloads', 'Developer Email', 'Category', 'App Link', 'Website']
ws.append(header)


def fetch_apps(search_term, category_name):
    try:
        results = search(
            search_term,
            lang='en',
            country='us',
            n_hits=100
        )

        if not results:
            logging.info(f"No results for category {category_name} with search term {search_term}.")
            return

        for result in results:
            app_id = result['appId']
            details = app(app_id, lang='en', country='us')

            name = details['title']
            description = details['description']
            downloads = details['installs']
            developer_email = details.get('developerEmail', 'N/A')
            app_link = f"https://play.google.com/store/apps/details?id={app_id}"
            website = details.get('developerWebsite', 'N/A')

            downloads_count = int(downloads.replace(',', '').replace('+', '').split(' ')[0])
            if downloads_count < 100000:
                ws.append([
                    name,
                    description,
                    downloads,
                    developer_email,
                    category_name,
                    app_link,
                    website
                ])

                wb.save('filtered_apps.xlsx')

        logging.info(f"Processed apps for category {category_name} with search term {search_term}.")

    except Exception as e:
        logging.error(f"Error fetching details for category {category_name} with search term {search_term}: {e}")


for category_name, search_term in target_search_terms.items():
    logging.info(f"Fetching apps for category {category_name}")
    fetch_apps(search_term, category_name)

logging.info("Data saved to filtered_apps.xlsx")
