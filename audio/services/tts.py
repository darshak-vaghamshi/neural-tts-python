import os

from fastapi import Request

from ..config import FEMALE_VOICES
from ..services.cache import (
    get_cached_file,
    generate_cache_key,
    register_audio_file,
    resolve_cache_paths,
)
from ..utils.audio_gen import synthesize_chunks, concatenate_mp3
from ..utils.cleanup import cleanup_files
from ..utils.text import chunk_text


async def generate_audio(request: Request, text: str, lang: str, news_id: str = "unknown"):
    app = request.app
    logger = app.state.logger

    voice = FEMALE_VOICES.get(lang)
    if not voice:
        raise ValueError(f"Unsupported language: {lang}")

    cache_key = generate_cache_key(news_id, text, lang)
    cached_url = get_cached_file(request, news_id, lang, cache_key)

    if cached_url:
        return {"audio_url": cached_url, "cached": True}

    audio_dir, final_mp3_path, relative_path = resolve_cache_paths(
        app, news_id, lang, cache_key
    )
    os.makedirs(audio_dir, exist_ok=True)
    temp_files = []

    try:
        chunks = chunk_text(text, max_chars=2000)

        mp3_files = await synthesize_chunks(
            chunks,
            voice,
            max_concurrency=min(4, len(chunks) or 1),
        )
        temp_files.extend(mp3_files)

        if len(mp3_files) > 1:
            final_mp3 = concatenate_mp3(mp3_files)
        else:
            final_mp3 = mp3_files[0]

        if os.path.exists(final_mp3_path):
            try:
                os.remove(final_mp3_path)
            except Exception as exc:
                logger.warning(
                    f"Failed to replace existing audio {final_mp3_path}: {exc}"
                )
        os.rename(final_mp3, final_mp3_path)

        register_audio_file(app, news_id, lang, os.path.basename(final_mp3_path))

        audio_url = request.url_for('static', path=relative_path)
        return {"audio_url": audio_url, "cached": False}

    except Exception as e:
        # Better error logging
        logger.error(f"TTS Error for lang {lang}: {str(e)}")
        raise  # Re-raise for API to catch

    finally:
        cleanup_files(temp_files)