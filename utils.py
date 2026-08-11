import os
import re

import streamlit as st
from dotenv import load_dotenv

from groq import Groq
from pypdf import PdfReader

import fal_client
import requests

from huggingface_hub import InferenceClient


# ============================================================
# LOAD LOCAL .ENV
# ============================================================

load_dotenv()


# ============================================================
# HELPER: GET SECRET
# Supports:
# 1. Local .env
# 2. Streamlit Cloud Secrets
# ============================================================

def get_secret(name):
    value = os.getenv(name)

    if value:
        return value

    try:
        value = st.secrets.get(name)
        if value:
            return value
    except Exception:
        pass

    return None


# ============================================================
# API KEYS
# ============================================================

GROQ_API_KEY = get_secret("GROQ_API_KEY")
HF_TOKEN = get_secret("HF_TOKEN")
FAL_KEY = get_secret("FAL_KEY")


# ============================================================
# GROQ CLIENT
# ============================================================

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is missing. "
        "Add GROQ_API_KEY to Streamlit Cloud Secrets."
    )

groq_client = Groq(api_key=GROQ_API_KEY)


# ============================================================
# HUGGING FACE CLIENT
# ============================================================

def get_hf_client():

    if not HF_TOKEN:
        raise ValueError(
            "HF_TOKEN is missing. "
            "Add HF_TOKEN to Streamlit Cloud Secrets."
        )

    return InferenceClient(token=HF_TOKEN)


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

            if msg.get("role") in [
                "system",
                "user",
                "assistant"
            ]:

                clean_messages.append({
                    "role": msg["role"],
                    "content": str(
                        msg.get("content", "")
                    )
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

        # Use smaller chunks to reduce Groq token usage
        chunks = chunk_text(
            text,
            max_chars=2500
        )

        partial_summaries = []

        import time

        # ----------------------------------------------------
        # Summarize each PDF section
        # ----------------------------------------------------

        for chunk in chunks:

            prompt = f"""
Summarize the following PDF section briefly.

Focus only on:

- Main ideas
- Important facts
- Key concepts
- Important conclusions

Avoid unnecessary explanation.

PDF SECTION:

{chunk}
"""

            success = False

            for attempt in range(3):

                try:

                    response = groq_client.chat.completions.create(

                        model="llama-3.1-8b-instant",

                        messages=[
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],

                        temperature=0.2,

                        max_tokens=500
                    )

                    partial_summaries.append(
                        response.choices[0].message.content
                    )

                    success = True

                    break

                except Exception as e:

                    error_text = str(e)

                    # Groq rate limit
                    if (
                        "429" in error_text
                        or "rate_limit" in error_text
                        or "Rate limit" in error_text
                    ):

                        if attempt < 2:

                            time.sleep(4)

                        else:

                            return (
                                "⚠️ Groq rate limit reached. "
                                "Please wait a few seconds and "
                                "try the PDF again."
                            )

                    else:

                        raise e

            if not success:

                return (
                    "⚠️ Could not summarize the PDF section."
                )

        # ----------------------------------------------------
        # Combine section summaries
        # ----------------------------------------------------

        combined_text = "\n\n".join(
            partial_summaries
        )

        # Prevent the final request from becoming too large
        combined_text = combined_text[:7000]

        final_prompt = f"""
Create one concise and well-structured summary
from the PDF section summaries below.

Use:

- A short overview
- Headings where useful
- Bullet points for important information

SECTION SUMMARIES:

{combined_text}
"""

        # ----------------------------------------------------
        # Final summary request
        # ----------------------------------------------------

        for attempt in range(3):

            try:

                final_response = (
                    groq_client
                    .chat
                    .completions
                    .create(

                        model="llama-3.1-8b-instant",

                        messages=[
                            {
                                "role": "user",
                                "content": final_prompt
                            }
                        ],

                        temperature=0.2,

                        max_tokens=700
                    )
                )

                return (
                    final_response
                    .choices[0]
                    .message
                    .content
                )

            except Exception as e:

                error_text = str(e)

                if (
                    "429" in error_text
                    or "rate_limit" in error_text
                    or "Rate limit" in error_text
                ):

                    if attempt < 2:

                        time.sleep(4)

                    else:

                        return (
                            "⚠️ Groq rate limit reached while "
                            "creating the final summary. "
                            "Please wait a few seconds and try again."
                        )

                else:

                    raise e

    except Exception as e:

        return f"❌ PDF Summary Error: {str(e)}"


# ============================================================
# YOUTUBE TRANSCRIPT CONVERSION
# ============================================================
# ============================================================
# YOUTUBE TRANSCRIPT CONVERSION
# ============================================================

def _clean_youtube_transcript(text):
    """
    Clean transcript returned by youtube-transcript.ai.
    Removes metadata and timestamps.
    """

    if not text:
        return ""

    lines = text.splitlines()
    cleaned_lines = []

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # Remove metadata lines
        if line.startswith("# Transcript:"):
            continue

        if line.startswith("Source video:"):
            continue

        if line.startswith("Language:"):
            continue

        if line.startswith("Other available languages:"):
            continue

        if line.startswith("To request a specific language:"):
            continue

        # Remove timestamps like:
        # [00:01]
        # [1:25]
        # [01:20:30]

        line = re.sub(
            r"^\[\d{1,2}:\d{2}(?::\d{2})?\]\s*",
            "",
            line
        )

        if line:
            cleaned_lines.append(line)

    return " ".join(cleaned_lines).strip()


# ============================================================
# YOUTUBE SUMMARY
# ============================================================

def summarize_youtube(url, output_language="English"):

    video_id = extract_video_id(url)

    if not video_id:
        return "❌ Invalid YouTube URL."

    try:

        # ----------------------------------------------------
        # GET TRANSCRIPT
        # ----------------------------------------------------

        transcript_url = (
            f"https://youtube-transcript.ai/transcript/{video_id}.txt"
        )

        response = requests.get(
            transcript_url,
            params={"lang": "en"},
            timeout=30
        )

        # ----------------------------------------------------
        # CHECK RESPONSE
        # ----------------------------------------------------

        if response.status_code != 200:

            return (
                "❌ Could not retrieve the transcript for this "
                "YouTube video.\n\n"
                "Possible reasons:\n"
                "• The video has no captions\n"
                "• The video is private or unavailable\n"
                "• The transcript service is temporarily unavailable\n\n"
                "Please try another public YouTube video."
            )

        raw_text = response.text.strip()

        if not raw_text:

            return (
                "⚠️ The YouTube transcript is empty or unavailable."
            )

        # ----------------------------------------------------
        # CLEAN TRANSCRIPT
        # ----------------------------------------------------

        text = _clean_youtube_transcript(raw_text)

        if not text:

            return (
                "⚠️ Could not extract readable text "
                "from this YouTube transcript."
            )

        # ----------------------------------------------------
        # LIMIT EXTREMELY LARGE TRANSCRIPTS
        # ----------------------------------------------------

        chunks = chunk_text(
            text,
            max_chars=2500
        )

        summaries = []

        # ----------------------------------------------------
        # SUMMARIZE EACH CHUNK
        # ----------------------------------------------------

        for chunk in chunks:

            prompt = f"""
Summarize the following YouTube transcript section.

Focus on:

- Main ideas
- Important facts
- Key concepts
- Important conclusions

Keep the summary concise and accurate.

Do not add information that is not present
in the transcript.

TRANSCRIPT SECTION:

{chunk}
"""

            try:

                response = groq_client.chat.completions.create(

                    model="llama-3.1-8b-instant",

                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],

                    temperature=0.2,

                    max_tokens=500
                )

                summaries.append(
                    response.choices[0].message.content
                )

            except Exception as e:

                error_text = str(e)

                if "429" in error_text:

                    return (
                        "⚠️ Groq rate limit reached. "
                        "Please wait a few seconds and try again."
                    )

                return (
                    f"❌ Error while summarizing transcript: "
                    f"{error_text}"
                )

        # ----------------------------------------------------
        # COMBINE SUMMARIES
        # ----------------------------------------------------

        combined = "\n\n".join(summaries)

        # Keep final prompt within reasonable size
        combined = combined[:7000]

        # ----------------------------------------------------
        # FINAL SUMMARY PROMPT
        # ----------------------------------------------------

        if output_language == "Telugu":

            final_prompt = f"""
Create a simple and easy-to-understand Telugu
summary of this YouTube video.

Use Telugu with English technical words
where appropriate.

Use:

- Short overview
- Important points
- Key concepts
- Main conclusion

Do not add information that is not present
in the provided content.

VIDEO CONTENT:

{combined}
"""

        else:

            final_prompt = f"""
Create a clear and well-structured English
summary of this YouTube video.

Use:

- Short overview
- Important points
- Key concepts
- Main conclusion

Use headings and bullet points where useful.

Do not add information that is not present
in the provided content.

VIDEO CONTENT:

{combined}
"""

        # ----------------------------------------------------
        # FINAL GROQ REQUEST
        # ----------------------------------------------------

        final_response = groq_client.chat.completions.create(

            model="llama-3.1-8b-instant",

            messages=[
                {
                    "role": "user",
                    "content": final_prompt
                }
            ],

            temperature=0.2,

            max_tokens=1000
        )

        final_summary = (
            final_response
            .choices[0]
            .message
            .content
        )

        return f"""
### 📺 YouTube Video Summary

**Summary Language:** {output_language}

---

{final_summary}
"""

    except requests.exceptions.Timeout:

        return (
            "❌ YouTube transcript request timed out. "
            "Please try again."
        )

    except requests.exceptions.ConnectionError:

        return (
            "❌ Could not connect to the YouTube transcript "
            "service. Please try again later."
        )

    except Exception as e:

        error_text = str(e)

        if "429" in error_text:

            return (
                "⚠️ Groq rate limit reached. "
                "Please wait a few seconds and try again."
            )

        return (
            f"❌ YouTube Summary Error: {error_text}"
        )


# ============================================================
# YOUTUBE SUMMARY
# ============================================================

def summarize_youtube(url, output_language="English"):

    video_id = extract_video_id(url)

    if not video_id:
        return "❌ Invalid YouTube URL."

    try:
        # ----------------------------------------------------
        # Get transcript from hosted transcript service
        # ----------------------------------------------------

        transcript_url = (
            f"https://youtube-transcript.ai/transcript/{video_id}.txt"
        )

        response = requests.get(
            transcript_url,
            params={"lang": "en"},
            timeout=30
        )

        if response.status_code != 200:
            return (
                "❌ Could not retrieve the YouTube transcript. "
                "Please try another video."
            )

        text = response.text.strip()

        if not text:
            return "⚠️ Transcript is empty or unavailable."

        # ----------------------------------------------------
        # Remove timestamp formatting if present
        # ----------------------------------------------------

        lines = text.splitlines()

        cleaned_lines = []

        for line in lines:

            line = line.strip()

            if not line:
                continue

            # Skip markdown timestamp lines such as:
            # [00:01] text
            line = re.sub(
                r"^\[\d{1,2}:\d{2}(?::\d{2})?\]\s*",
                "",
                line
            )

            cleaned_lines.append(line)

        text = " ".join(cleaned_lines).strip()

        if not text:
            return "⚠️ Transcript is empty."

        # ----------------------------------------------------
        # Split transcript
        # ----------------------------------------------------

        chunks = chunk_text(
            text,
            max_chars=2500
        )

        summaries = []

        # ----------------------------------------------------
        # Summarize transcript sections
        # ----------------------------------------------------

        for chunk in chunks:

            prompt = f"""
Summarize this YouTube transcript section.

Focus on:
- Main ideas
- Important facts
- Key concepts
- Important conclusions

Keep the summary concise.

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
                temperature=0.2,
                max_tokens=500
            )

            summaries.append(
                response.choices[0].message.content
            )

        combined = "\n\n".join(summaries)

        # ----------------------------------------------------
        # Final summary
        # ----------------------------------------------------

        if output_language == "Telugu":

            final_prompt = f"""
Create a simple and easy-to-understand Telugu
summary of this YouTube video.

Use Telugu with English technical words
where appropriate.

VIDEO CONTENT:

{combined}
"""

        else:

            final_prompt = f"""
Create a clear and well-structured English
summary of this YouTube video.

Use headings and bullet points where useful.

VIDEO CONTENT:

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
            temperature=0.2,
            max_tokens=1000
        )

        final_summary = (
            final_response
            .choices[0]
            .message
            .content
        )

        return f"""
### 📺 YouTube Video Summary

**Summary Language:** {output_language}

---

{final_summary}
"""

    except Exception as e:

        error_text = str(e)

        if "429" in error_text:
            return (
                "⚠️ Groq rate limit reached. "
                "Please wait a few seconds and try again."
            )

        return f"❌ YouTube Summary Error: {error_text}"


# ============================================================
# IMAGE GENERATION
# ============================================================

def generate_image(
    prompt,
    output_path="generated_image.png"
):

    try:

        # ----------------------------------------------------
        # Try Hugging Face
        # ----------------------------------------------------

        if HF_TOKEN:

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

        if not FAL_KEY:

            return (
                "❌ Image generation requires "
                "HF_TOKEN or FAL_KEY."
            )

        os.environ["FAL_KEY"] = FAL_KEY

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

            return (
                "❌ Failed to download "
                "generated image."
            )

        with open(
            output_path,
            "wb"
        ) as file:

            file.write(response.content)

        return output_path

    except Exception as e:

        return (
            f"❌ Image Generation Error: {str(e)}"
        )