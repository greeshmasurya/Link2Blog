import re
from youtube_transcript_api import YouTubeTranscriptApi

def extract_video_id(url):
    regex = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(regex, url)
    if match:
        return match.group(1)
    return None

def fetch_transcript(video_url):
    video_id = extract_video_id(video_url)
    if not video_id:
        raise ValueError("Invalid YouTube URL")

    try:
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)
        
        transcript = None
        try:
            transcript = transcript_list.find_transcript(['en', 'en-US', 'en-GB'])
        except:
            for t in transcript_list:
                transcript = t
                break
        
        if not transcript:
            raise Exception("No transcript found")

        fetched_data = transcript.fetch()
        full_text = " ".join([item.text for item in fetched_data])
        return " ".join(full_text.split())

    except Exception as e:
        raise Exception(f"Failed to fetch transcript: {str(e)}")
