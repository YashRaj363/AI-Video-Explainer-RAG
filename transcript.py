
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled

video_id = "T_X4XFwKX8k"

try:
    api = YouTubeTranscriptApi()

    transcript_list = api.fetch(video_id,languages=["en"]
    )

    transcript = " ".join(chunk.text for chunk in transcript_list)

    print(transcript)

    # Save transcript to a text file
    with open("transcript.txt", "w", encoding="utf-8") as file:
        file.write(transcript)

    print("\nTranscript saved successfully!")

except TranscriptsDisabled:
    print("Captions are disabled for this video.")

except Exception as e:
    print(type(e).__name__, ":", e)
