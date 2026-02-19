from fastapi import APIRouter, HTTPException, Request

from ..config import SUPPORTED_LANGUAGES
from ..services.tts import generate_audio
from ..utils.text import clean_text, detect_language

router = APIRouter(prefix="/tts", tags=["tts"])


@router.post("")
async def text_to_speech(request: Request):
    data = await request.json()
    if not data or "text" not in data:
        raise HTTPException(status_code=400, detail={"error": "Missing text"})

    text = clean_text(data["text"])
    if not text:
        raise HTTPException(status_code=400, detail={"error": "Text empty after cleaning"})

    news_id = data.get("newsId", "unknown")
    lang = data.get("lang")
    if not lang:
        lang = detect_language(text)

    if lang not in SUPPORTED_LANGUAGES:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Unsupported language",
                "supported": list(SUPPORTED_LANGUAGES.keys()),
            },
        )

    try:
        result = await generate_audio(request, text, lang, news_id)
        result["success"] = True
        result["language"] = SUPPORTED_LANGUAGES[lang]
        return result
    except Exception as exc:
        logger = request.app.state.logger
        logger.error(f"TTS Error: {exc}")
        raise HTTPException(status_code=500, detail={"error": "Audio generation failed"})