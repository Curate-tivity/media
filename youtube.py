import logging
import requests
from youtube_transcript_api import YouTubeTranscriptApi
import openai
import os
from dotenv import load_dotenv
from utils.sql import create_connection, insert_data

# Set up logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
youtube_api_key = os.getenv('YOUTUBE_API_KEY')

connection = create_connection()

def get_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([i['text'] for i in transcript_list])
        return transcript
    except Exception as e:
        logging.error(f"An error occurred while getting the transcript: {e}")
        return None

def analyze_transcript(transcript):
    try:
        messages = [
            {"role": "system", "content": "You are an AI capable of summarizing YouTube video content based on its transcript. A clear and concise summary can provide a quick understanding of the video's content."},
            {"role": "user", "content": f"Generate a concise summary of the YouTube video using this transcript: {transcript}."},
        ]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=messages,
            temperature=0,
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"An error occurred while analyzing the transcript: {e}")
        return None

def get_videos_from_channel(channel_id):
    try:
        url = f"https://www.googleapis.com/youtube/v3/search?key={os.getenv('YOUTUBE_API_KEY')}&channelId={channel_id}&part=snippet,id&order=date&maxResults=20"
        response = requests.get(url)
        response.raise_for_status()
        video_data = []
        for item in response.json()['items']:
            if item['id'].get('videoId'):
                video_id = item['id']['videoId']
                video_info_url = f"https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={os.getenv('YOUTUBE_API_KEY')}&part=snippet,contentDetails,statistics"
                video_info_response = requests.get(video_info_url)
                video_info_response.raise_for_status()
                video_info = video_info_response.json()['items'][0]
                video_data.append({
                    'videoId': video_id,
                    'publishedAt': video_info['snippet']['publishedAt'],
                    'channelId': video_info['snippet']['channelId'],
                    'title': video_info['snippet']['title'],
                    'description': video_info['snippet']['description'],
                    'thumbnails': video_info['snippet']['thumbnails'],
                    'channelTitle': video_info['snippet']['channelTitle'],
                    'tags': video_info['snippet'].get('tags', []),
                    'categoryId': video_info['snippet']['categoryId'],
                    'duration': video_info['contentDetails']['duration'],
                    'aspectRatio': video_info['contentDetails'].get('aspectRatio'),
                    'definition': video_info['contentDetails']['definition'],
                    'caption': video_info['contentDetails']['caption'],
                    'viewCount': video_info['statistics']['viewCount'],
                    'likeCount': video_info['statistics'].get('likeCount'),
                    'dislikeCount': video_info['statistics'].get('dislikeCount'),
                    'favoriteCount': video_info['statistics']['favoriteCount'],
                    'commentCount': video_info['statistics'].get('commentCount'),
                })
        return video_data
    except Exception as e:
        print(f"An error occurred while getting videos from the channel: {e}")
        return []

channel_ids = ["UCNJ1Ymd5yFuUPtn21xtRbbw","UCvKRFNawVcuz4b9ihUTApCg"]  # Replace with your list of channel IDs
# need to add to the channel list, by going to each channel page -> right click -> view page source -> then search channelid
# should probably add feature to check video titles to see if I already have the data
# this is a costly script, so I should also split the openai calls out of this particular script, and batch summarize at a different time
# should chunk the transcripts before giving to GPT4, and I should expand the prompt to where I get a more thorough response.


for channel_id in channel_ids:
    try:
        videos_info = get_videos_from_channel(channel_id)
        for video_info in videos_info:
            transcript = get_transcript(video_info['videoId'])
            if transcript:
                analysis = analyze_transcript(transcript)
                try:
                    insert_data(connection, video_info, transcript, analysis)
                except Exception as e:
                    print(f"An error occurred while inserting data into the database: {e}")
                    with open('failed_inserts.txt', 'a') as f:
                        f.write(f"Video Info: {video_info}\nTranscript: {transcript}\nAnalysis: {analysis}\n\n")
    except Exception as e:
        print(f"An error occurred while processing channel {channel_id}: {e}")
