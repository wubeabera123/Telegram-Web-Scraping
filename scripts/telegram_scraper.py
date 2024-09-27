import requests
from bs4 import BeautifulSoup
import csv

# Function to scrape a Telegram channel
def scrape_telegram_channel(channel_url, data_list):
    response = requests.get(channel_url)

    # Check if request was successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Scrape Channel Title
        try:
            channel_title = soup.find('div', class_='tgme_channel_info_header_title').text.strip()
        except AttributeError:
            channel_title = 'N/A'

        # Scrape Channel Username from URL
        channel_username = channel_url.split('/')[-1]

        print(f"Channel Title: {channel_title}")
        print(f"Channel Username: {channel_username}")

        # Scrape messages
        messages = soup.find_all('div', class_='tgme_widget_message_wrap')

        for message in messages:
            try:
                # Scrape message ID
                message_id = message['data-post']

                # Scrape message content
                message_text_element = message.find('div', class_='tgme_widget_message_text')
                message_text = message_text_element.text.strip() if message_text_element else "No message text"

                # Scrape date
                message_date_element = message.find('time')
                message_date = message_date_element['datetime'] if message_date_element else "No date"

                # Scrape media (if exists)
                media_elements = message.find_all('a', href=True)
                media_path = [media['href'] for media in media_elements if 'file' in media['href']]

                # Append the scraped data to the list
                data_list.append({
                    "Channel Title": channel_title,
                    "Channel Username": channel_username,
                    "ID": message_id,
                    "Message": message_text,
                    "Date": message_date,
                    "Media Path": ', '.join(media_path) if media_path else 'None'
                })

                print(f"Message ID: {message_id}, Message: {message_text}, Date: {message_date}, Media Path: {media_path}")

            except Exception as e:
                print(f"Error parsing message: {e}")
    else:
        print(f"Failed to retrieve the channel page. Status code: {response.status_code}")

# List of Telegram channels
channels = [
    'https://t.me/s/ethiopia_online_shopping',
    'https://t.me/s/Ethiomarkettttt',
    'https://t.me/s/ethiocar_sales'
]

# List to hold all the scraped data
scraped_data = []

# Loop through and scrape each channel
for channel in channels:
    scrape_telegram_channel(channel, scraped_data)

# Write the scraped data to a CSV file
csv_file = '../data/telegram_scraped_data.csv'
csv_columns = ["Channel Title", "Channel Username", "ID", "Message", "Date", "Media Path"]

try:
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=csv_columns)
        writer.writeheader()
        writer.writerows(scraped_data)
    print(f"Data successfully saved to {csv_file}")
except IOError:
    print("I/O error while writing the CSV file")
