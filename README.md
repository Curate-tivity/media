# Content Generator 3000

An automated YouTube video aggregation and AI-powered summarization pipeline that helps you stay up-to-date with AI news.

This project fetches videos from configured YouTube channels, extracts transcripts, generates AI summaries using OpenAI, and stores everything in a SQL Server database for easy access and analysis.

## Features

- Monitor multiple YouTube channels automatically
- Extract video transcripts using YouTube Transcript API
- Generate AI-powered summaries with configurable OpenAI models
- Store video metadata, transcripts, and summaries in SQL Server
- Flexible configuration system via YAML
- Easy channel management with CLI tool
- Token usage tracking for API cost monitoring

## Prerequisites

- Python 3.7+
- Microsoft SQL Server
- YouTube Data API Key ([Get one here](https://developers.google.com/youtube/v3/getting-started))
- OpenAI API Key ([Get one here](https://platform.openai.com/api-keys))

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Curate-tivity/media.git
cd media
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your API keys:
```env
YOUTUBE_API_KEY=your_youtube_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

4. Create your configuration file:
```bash
cp config.example.yaml config.yaml
```

5. Edit `config.yaml` to customize:
   - Database connection details
   - OpenAI model settings (model, temperature, prompts)
   - YouTube settings (max results per channel)
   - YouTube channels to monitor

## Configuration

### config.yaml Structure

```yaml
youtube:
  max_results: 20  # Videos to fetch per channel

openai:
  model: gpt-3.5-turbo-16k  # or gpt-4, gpt-4-turbo
  temperature: 0  # 0 = deterministic, 1 = creative
  system_prompt: "Your custom system prompt..."
  user_prompt_template: "Your prompt with {transcript} placeholder"

database:
  server: your_server
  database: your_database
  driver: "{ODBC Driver 17 for SQL Server}"

channels:
  - id: CHANNEL_ID_1
    name: "Channel Name"
    enabled: true
  - id: CHANNEL_ID_2
    name: "Another Channel"
    enabled: false
```

## Channel Management

Use the `manage_channels.py` CLI tool to manage your YouTube channels:

### List all channels
```bash
python3 manage_channels.py list           # Enabled channels only
python3 manage_channels.py list --all     # All channels
```

### Add a new channel
```bash
python3 manage_channels.py add CHANNEL_ID "Channel Name"
python3 manage_channels.py add CHANNEL_ID "Channel Name" --disabled
```

### Remove a channel
```bash
python3 manage_channels.py remove CHANNEL_ID
```

### Enable/Disable a channel
```bash
python3 manage_channels.py enable CHANNEL_ID
python3 manage_channels.py disable CHANNEL_ID
```

### Rename a channel
```bash
python3 manage_channels.py rename CHANNEL_ID "New Name"
```

## Usage

Run the main script to fetch and process videos:

```bash
python3 youtube.py
```

The script will:
1. Load configuration from `config.yaml`
2. Process all enabled channels
3. Fetch recent videos (based on max_results setting)
4. Extract transcripts
5. Generate AI summaries
6. Store everything in the database
7. Log any errors to console and `failed_inserts.txt`

## Database Schema

The application expects a SQL Server table with the following structure:

```sql
CREATE TABLE dbo.youtube (
    VideoId NVARCHAR(50),
    PublishedAt DATETIME,
    ChannelId NVARCHAR(50),
    Title NVARCHAR(255),
    Description NVARCHAR(MAX),
    Thumbnails NVARCHAR(MAX),
    ChannelTitle NVARCHAR(255),
    Tags NVARCHAR(MAX),
    CategoryId NVARCHAR(50),
    Duration NVARCHAR(50),
    AspectRatio NVARCHAR(50),
    Definition NVARCHAR(50),
    Caption NVARCHAR(50),
    ViewCount INT,
    LikeCount INT,
    DislikeCount INT,
    FavoriteCount INT,
    CommentCount INT,
    Transcript NVARCHAR(MAX),
    Analysis NVARCHAR(MAX),
    IsProcessed BIT,
    TokenCount INT,
    ApiCalls INT,
    LastApiCall DATETIME,
    TranscriptCache NVARCHAR(MAX)
);
```

## Project Structure

```
media/
├── youtube.py              # Main application
├── manage_channels.py      # Channel management CLI
├── requirements.txt        # Python dependencies
├── config.example.yaml     # Example configuration
├── config.yaml            # Your configuration (gitignored)
├── .env                   # API keys (gitignored)
├── utils/
│   ├── sql.py            # Database utilities
│   └── config.py         # Configuration manager
└── README.md             # This file
```

## Tips

- Start with `gpt-3.5-turbo-16k` for cost-effective summaries
- Upgrade to `gpt-4o` or `gpt-4o-mini` for higher quality summaries
- Use `temperature: 0` for consistent, deterministic summaries
- Adjust `max_results` based on your API rate limits and processing needs
- Disable channels temporarily instead of removing them to preserve your configuration

## Troubleshooting

- **Configuration not found**: Make sure you've copied `config.example.yaml` to `config.yaml`
- **No channels found**: Add channels using `python3 manage_channels.py add CHANNEL_ID "Name"`
- **Database connection failed**: Check your database settings in `config.yaml`
- **API errors**: Verify your API keys in `.env` file
- **Failed inserts**: Check `failed_inserts.txt` for details

## Future Enhancements

- Multi-platform support (podcasts, articles, etc.)
- Web UI for browsing summaries
- Scheduled automation with cron
- Email digest generation
- Topic extraction and trending analysis
- Search and filtering capabilities

## License

MIT License - see LICENSE file for details

## Contributing

This is a collaborative project. Contributions are welcome!