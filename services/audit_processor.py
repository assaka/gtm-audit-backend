import json, zipfile, io, os, uuid
from datetime import datetime
from fastapi import UploadFile
from fastapi.responses import StreamingResponse
import google.generativeai as genai
import asyncio

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

session_data = {}

async def analyze_uploaded_file(file: UploadFile, user_id: str) -> str:
    contents = await file.read()
    try:
        if file.filename.endswith(".zip"):
            with zipfile.ZipFile(io.BytesIO(contents)) as z:
                for name in z.namelist():
                    if name.endswith(".json"):
                        data = json.loads(z.read(name))
                        break
                else:
                    raise Exception("No JSON file found in ZIP.")
        elif file.filename.endswith(".json"):
            data = json.loads(contents)
        else:
            raise Exception("Unsupported file type.")
    except Exception as e:
        raise Exception("Failed to parse file: " + str(e))

    container = data.get("containerVersion")
    if not container:
        raise Exception("Invalid GTM JSON: Missing 'containerVersion'.")

    input_text = json.dumps(container, indent=2)
    prompt = f"You are a GTM auditor. Analyze this GTM container:\n{input_text}"

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")  # or gemini-1.0-pro if 1.5 unavailable
        stream = model.generate_content(prompt, stream=True)
    except Exception as e:
        raise Exception("Gemini generation failed: " + str(e))

    session_id = str(uuid.uuid4())
    session_data[session_id] = {
        "stream": stream,
        "result_lines": [],
        "filename": file.filename,
        "user_id": user_id,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }

    return session_id


def stream_response(session_id: str):
    async def event_generator():
        if session_id not in session_data:
            yield f"data: Session {session_id} not found.\n\n"
            return

        session = session_data[session_id]
        stream = session["stream"]
        result_lines = []

        try:
            # Gemini returns a synchronous generator, not async. So we can't use `async for`.
            for chunk in stream:
                if hasattr(chunk, "text") and chunk.text:
                    for line in chunk.text.splitlines():
                        result_lines.append(line)
                        yield f"data: {line}\n\n"
                        await asyncio.sleep(0.02)
        except Exception as e:
            yield f"data: [Stream error] {str(e)}\n\n"

        record = {
            "filename": session["filename"],
            "result": "\n".join(result_lines),
            "timestamp": session["timestamp"]
        }
        history_path = f"history/{session['user_id']}.json"
        if os.path.exists(history_path):
            with open(history_path, "r") as f:
                history = json.load(f)
        else:
            history = []
        history.append(record)
        with open(history_path, "w") as f:
            json.dump(history, f, indent=2)

    return StreamingResponse(event_generator(), media_type="text/event-stream")
