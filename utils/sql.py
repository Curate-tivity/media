
import pyodbc

def create_connection():
    server = 'server'
    database = 'database'
    driver= '{ODBC Driver 17 for SQL Server}'
    try:
        connection = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes;')
        return connection
    except pyodbc.Error as e:
        print(f"Error: {e}")
        return None


def insert_data(connection, video_info, transcript, analysis):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO dbo.youtube (VideoId, PublishedAt, ChannelId, Title, Description, Thumbnails, ChannelTitle, Tags, CategoryId, Duration, AspectRatio, Definition, Caption, ViewCount, LikeCount, DislikeCount, FavoriteCount, CommentCount, Transcript, Analysis)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (video_info['videoId'], video_info['publishedAt'], video_info['channelId'], video_info['title'], video_info['description'], str(video_info['thumbnails']), video_info['channelTitle'], str(video_info.get('tags', [])), video_info['categoryId'], video_info['duration'], video_info.get('aspectRatio'), video_info['definition'], video_info['caption'], video_info['viewCount'], video_info.get('likeCount'), video_info.get('dislikeCount'), video_info['favoriteCount'], video_info.get('commentCount'), transcript, analysis))
        connection.commit()
    except pyodbc.Error as e:
        print(f"An error occurred while inserting data into the database: {e}")