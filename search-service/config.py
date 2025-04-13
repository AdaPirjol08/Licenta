import os

class Config:
    YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY", "your_default_key_here")
