import pyodbc
import logging

def create_connection():
    server = 'server'
    database = 'database'
    driver= '{ODBC Driver 17 for SQL Server}'
    try:
        connection = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes;')
        return connection
    except pyodbc.Error as e:
        logging.error(f"An error occurred while creating a connection: {e}")
        return None

def insert_data(connection, video_info, transcript, analysis, is_processed, token_count, api_calls, last_api_call, transcript_cache):
    if connection is None:
        logging.error("No connection to the database.")
        return
    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO dbo.youtube (VideoId, PublishedAt, ChannelId, Title, Description, Thumbnails, ChannelTitle, Tags, CategoryId, Duration, AspectRatio, Definition, Caption, ViewCount, LikeCount, DislikeCount, FavoriteCount, CommentCount, Transcript, Analysis, IsProcessed, TokenCount, ApiCalls, LastApiCall, TranscriptCache)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (video_info['videoId'], video_info['publishedAt'], video_info['channelId'], video_info['title'], video_info['description'], str(video_info['thumbnails']), video_info['channelTitle'], str(video_info.get('tags', [])), video_info['categoryId'], video_info['duration'], video_info.get('aspectRatio'), video_info['definition'], video_info['caption'], video_info['viewCount'], video_info.get('likeCount'), video_info.get('dislikeCount'), video_info['favoriteCount'], video_info.get('commentCount'), transcript, analysis, is_processed, token_count, api_calls, last_api_call, transcript_cache))
        connection.commit()
    except pyodbc.Error as e:
        logging.error(f"An error occurred while inserting data into the database: {e}")
