import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# Configure genai
genai.configure(api_key=st.secrets["API_KEY"])

# Set up prompt
prompt="""You are Youtube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Please provide the summary of the text given here:  """

# Youtube video transcript getter
def extract_transcript(youtube_url):
    try:
        video_id = youtube_url.split("v=")[1].split('&')[0]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = ""
        for i in transcript_text:
            transcript = transcript + " " + i["text"]
        return transcript
    except Exception as e:
        raise e
    
# Get summary from gemini pro model
def generate_summary(transcript, prompt):
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    response = model.generate_content(prompt+transcript)
    return response.text 

# Streamlit application
def application():
    st.set_page_config(page_title="Youtube Video Summarizer")
    st.title("Youtube Summarizer - Utkarsh")
    youtube_link = st.text_input("Enter Youtube video link : ")

    if youtube_link:
        video_id = youtube_link.split("v=")[1].split('&')[0]
        st.image(f"https://i3.ytimg.com/vi/{video_id}/hqdefault.jpg")

    if st.button("Get Summary"):
        with st.spinner("responding..."):
            transcript = extract_transcript(youtube_link)
            if transcript is not None:
                    summary = generate_summary(transcript, prompt)
                    st.subheader("Youtube Video Summary :")
                    st.write(summary)
                    st.success("Done")

# Run the application
if __name__ == '__main__':
    application()