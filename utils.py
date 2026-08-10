import os
import re

from dotenv import load_dotenv
load_dotenv()

from groq import Groq
from pypdf import PdfReader

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import VideoUnavailable, TranscriptsDisabled

import fal_client
import requests

from huggingface_hub import InferenceClient


# ============================================================
# API CLIENTS
# ============================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is missing. "
        "Please add GROQ_API_KEY=your_key to your .env file."
    )

# This was missing in your original code.
groq_client = Groq(api_key=GROQ_API_KEY)


# ============================================================
# HUGGING FACE CLIENT
# ============================================================

def get_hf_client():
    token = os.getenv("HF_TOKEN")

    if not token:
        raise ValueError(
            "HF_TOKEN is missing. "
            "Please add HF_TOKEN=your_token to your .env file."
        )

    return InferenceClient(api_key=token)


# ============================================================
# TEXT CHUNKING
# ============================================================

def chunk_text(text, max_chars=3500):
    """
    Split large text into smaller chunks.
    """

    if not text:
        return []

    return [
        text[i:i + max_chars]
        for i in range(0, len(text), max_chars)
    ]


# ============================================================
# YOUTUBE VIDEO ID EXTRACTOR
# ============================================================

def extract_video_id(url: str):

    patterns = [
        r"v=([a-zA-Z0-9_-]{11})",
        r"youtu\.be/([a-zA-Z0-9_-]{11})",
        r"shorts/([a-zA-Z0-9_-]{11})"
    ]

    for pattern in patterns:

        match = re.search(pattern, url)

        if match:
            return match.group(1)

    return None


# ============================================================
# CHAT WITH GROQ LLM
# ============================================================

def chat_with_llm(messages):

    try:

        clean_messages = []

        for msg in messages[-10:]:

            # Only send valid chat messages
            if msg.get("role") in ["system", "user", "assistant"]:

                clean_messages.append({
                    "role": msg["role"],
                    "content": str(msg.get("content", ""))
                })

        if not clean_messages:
            return "Please enter a message."

        completion = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=clean_messages,
            temperature=0.7,
            max_tokens=1024
        )

        return completion.choices[0].message.content

    except Exception as e:

        return f"❌ Groq API Error: {str(e)}"


# ============================================================
# PDF SUMMARY
# ============================================================

def summarize_pdf(pdf_file):

    try:

        reader = PdfReader(pdf_file)

        text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        if not text.strip():

            return "⚠️ Could not extract text from this PDF."

        chunks = chunk_text(text)

        partial_summaries = []

        for chunk in chunks:

            prompt = f"""
Summarize the following section of a PDF clearly.

Focus on:
- Main ideas
- Important facts
- Key concepts
- Important conclusions

PDF SECTION:

{chunk}
"""

            response = groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=1024
            )

            partial_summaries.append(
                response.choices[0].message.content
            )

        combined_text = "\n\n".join(partial_summaries)

        final_prompt = f"""
Create one clear and well-structured summary
from the following PDF section summaries.

Use headings and bullet points where useful.

SECTION SUMMARIES:

{combined_text}
"""

        final_response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": final_prompt
                }
            ],
            temperature=0.3,
            max_tokens=2048
        )

        return final_response.choices[0].message.content

    except Exception as e:

        return f"❌ PDF Summary Error: {str(e)}"


# ============================================================
# YOUTUBE TRANSCRIPT CONVERSION
# ============================================================

def _transcript_items_to_text(items):

    parts = []

    for item in items:

        if hasattr(item, "text"):

            parts.append(item.text)

        elif isinstance(item, dict) and "text" in item:

            parts.append(item["text"])

        else:

            parts.append(str(item))

    return " ".join(parts)


# ============================================================
# YOUTUBE SUMMARY
# ============================================================

def summarize_youtube(url, output_language="English"):

    video_id = extract_video_id(url)

    if not video_id:

        return "❌ Invalid YouTube URL."

    try:

        transcript = None
        transcript_used = None

        # ----------------------------------------------------
        # Try Telugu transcript
        # ----------------------------------------------------

        try:

            transcript = YouTubeTranscriptApi().fetch(
                video_id,
                languages=["te"]
            )

            transcript_used = "Telugu"

        except Exception:

            transcript = None

        # ----------------------------------------------------
        # Fallback to English
        # ----------------------------------------------------

        if transcript is None:

            transcript = YouTubeTranscriptApi().fetch(
                video_id,
                languages=["en"]
            )

            transcript_used = "English"

        # ----------------------------------------------------
        # Convert transcript to text
        # ----------------------------------------------------

        text = _transcript_items_to_text(transcript)

        if not text.strip():

            return "⚠️ Transcript is empty or unavailable."

        # ----------------------------------------------------
        # Split transcript
        # ----------------------------------------------------

        chunks = chunk_text(text)

        summaries = []

        for chunk in chunks:

            prompt = f"""
Summarize this YouTube transcript section.

Keep the important information.
Remove unnecessary repetition.

TRANSCRIPT:

{chunk}
"""

            response = groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=1024
            )

            summaries.append(
                response.choices[0].message.content
            )

        combined = "\n\n".join(summaries)

        # ----------------------------------------------------
        # Final language formatting
        # ----------------------------------------------------

        if output_language == "Telugu":

            final_prompt = f"""
Create a simple and easy-to-understand Telugu summary
of this YouTube video.

Use Telugu with English technical words when appropriate.

VIDEO SUMMARY:

{combined}
"""

        else:

            final_prompt = f"""
Create a simple, clear and well-structured English
summary of this YouTube video.

VIDEO SUMMARY:

{combined}
"""

        final_response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": final_prompt
                }
            ],
            temperature=0.3,
            max_tokens=2048
        )

        final_summary = final_response.choices[0].message.content

        return f"""
### 📺 YouTube Video Summary

**Transcript Used:** {transcript_used}

**Summary Language:** {output_language}

---

{final_summary}
"""

    except TranscriptsDisabled:

        return "⚠️ Transcripts are disabled for this video."

    except VideoUnavailable:

        return "⚠️ The YouTube video is unavailable."

    except Exception as e:

        return f"❌ YouTube Summary Error: {str(e)}"


# ============================================================
# IMAGE GENERATION
# ============================================================

def generate_image(prompt, output_path="generated_image.png"):

    try:

        hf_token = os.getenv("HF_TOKEN")

        if hf_token:

            client = get_hf_client()

            image = client.text_to_image(
                prompt,
                model="stabilityai/stable-diffusion-3.5-large"
            )

            image.save(output_path)

            return output_path

        # ----------------------------------------------------
        # Fallback to FAL
        # ----------------------------------------------------

        fal_key = os.getenv("FAL_KEY")

        if not fal_key:

            return (
                "❌ Image generation requires either "
                "HF_TOKEN or FAL_KEY in your .env file."
            )

        os.environ["FAL_KEY"] = fal_key

        result = fal_client.subscribe(
            "fal-ai/flux/dev",
            arguments={
                "prompt": prompt,
                "image_size": "square_hd",
                "num_images": 1
            }
        )

        image_url = result["images"][0]["url"]

        response = requests.get(
            image_url,
            timeout=60
        )

        if response.status_code != 200:

            return "❌ Failed to download generated image."

        with open(output_path, "wb") as file:

            file.write(response.content)

        return output_path

    except Exception as e:

        return f"❌ Image Generation Error: {str(e)}"