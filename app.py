from flask import Flask, render_template, request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
import os

app = Flask(__name__)

# Load environment variables
load_dotenv()

# Load credentials and create an API client
file_name = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
credentials = Credentials.from_service_account_file(file_name)
youtube = build('youtube', 'v3', credentials=credentials)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_term = request.form['search_term']
        try:
            search_response = youtube.search().list(
                q=search_term,
                part='id,snippet',
                maxResults=10
            ).execute()

            videos = []

            for search_result in search_response.get('items', []):
                if search_result['id']['kind'] == 'youtube#video':
                    videos.append(search_result)
            return render_template('search.html', videos=videos)

        except HttpError as e:
            print(f'An HTTP error {e.resp.status} occurred: {e.content}')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
