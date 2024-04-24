import streamlit as st
import requests
import os
import logging

# Initialize logging
logging.basicConfig(level=logging.ERROR, filename='app_error.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')

# Set up the page
st.set_page_config(page_title="Whisper Speech Recognition", page_icon=":studio_microphone:")
st.title(":studio_microphone: Speech Recognition")
st.markdown("Upload an audio file you wish to have translated")

# Set up the endpoint
endpoint = os.getenv("MODEL_ENDPOINT", default="http://0.0.0.0:8001/inference")

# File uploader widget
audio = st.file_uploader("", type=["wav"], accept_multiple_files=False)

# Process the uploaded audio file
if audio:
    audio_bytes = audio.read()
    st.audio(audio_bytes, format='audio/wav', start_time=0)
    files = {'file': audio_bytes}

    # Make the POST request within a try-except block
    try:
        response = requests.post(endpoint, files=files)
        # Check if the response status code is 200 (OK)
        if response.status_code == 200:
            response_json = response.json()
            st.subheader(f"Translated Text")
            st.text_area(label="Result", value=response_json['text'], height=300)
        else:
            # Log the error
            logging.error(f'Failed to get a valid response: Status Code {response.status_code}')
            st.error(f"Failed to get a valid response. The server returned status code {response.status_code}.")
    except requests.exceptions.RequestException as e:
        # Log the request exception
        logging.error(f'Request exception: {e}')
        st.error("Failed to send the request. Please check the server and the endpoint.")
    except ValueError as e:
        # Log the JSON decoding error
        logging.error(f'JSON decoding failed: {e}')
        st.error("Failed to decode the server response. Please check the server response format.")
else:
    st.write("Input not provided")
