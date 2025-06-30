# services/audit_processor.py

import os
import json
import zipfile
import io
import uuid
import asyncio
from datetime import datetime

from fastapi import UploadFile, HTTPException
from fastapi.responses import StreamingResponse
import google.generativeai as genai
from dotenv import load_dotenv

from .gtm_parser import parse_gtm_file

# Load environment and configure Gemini
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# In-memory store for streaming sessions
session_data = {}

async def analyze_uploaded_file(file: UploadFile, user_id: str) -> str:
    """
    1. Read the uploaded ZIP or JSON.
    2. Extract containerVersion and parse it.
    3. Kick off a Gemini stream to audit the parsed data.
    4. Store the stream under a session_id.
    """
    raw = await file.read()
    try:
        if file.filename.lower().endswith(".zip"):
            with zipfile.ZipFile(io.BytesIO(raw)) as z:
                for name in z.namelist():
                    if name.lower().endswith(".json"):
                        data = json.loads(z.read(name))
                        break
                else:
                    raise HTTPException(400, "No JSON in ZIP.")
        else:
            data = json.loads(raw)
    except Exception as e:
        raise HTTPException(400, f"Failed to parse upload: {e}")

    container = data.get("containerVersion")
    if not container:
        raise HTTPException(400, "Missing containerVersion in JSON.")

    # Pre-parse the structure for counts & details
    parsed = parse_gtm_file({"containerVersion": container})

    # Build the Gemini prompt
    prompt = (
        "You are a Google Tag Manager auditor. Here is the parsed container data:\n"
        f"{json.dumps(parsed, indent=2)}\n"
        "Please provide a concise audit summary."
    )

    # **Use a valid model** from list_models.py output
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        stream = model.generate_content(prompt, stream=True)
    except Exception as e:
        raise HTTPException(502, f"Gemini generation failed: {e}")

    # Store for streaming
    session_id = str(uuid.uuid4())
    session_data[session_id] = {
        "stream": stream,
        "result_lines": [],
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "user_id": user_id,
    }
    return session_id

def stream_response(session_id: str) -> StreamingResponse:
    """
    Returns a Server-Sent-Events response that yields each line
    produced by the Gemini stream.
    """
    async def event_generator():
        session = session_data.get(session_id)
        if not session:
            yield f"data: Session {session_id} not found\n\n"
            return
        try:
            for chunk in session["stream"]:
                text = getattr(chunk, "text", None)
                if text:
                    for line in text.splitlines():
                        session["result_lines"].append(line)
                        yield f"data: {line}\n\n"
                await asyncio.sleep(0.01)
        except Exception as e:
            yield f"data: [stream error] {e}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

def process_audit(data: dict) -> dict:
    """
    A simple sync endpoint: parse and return GTM structure
    without streaming.
    """
    return parse_gtm_file(data)


