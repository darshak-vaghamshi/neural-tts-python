import hashlib
import os
import re

from fastapi import Request


def generate_cache_key(news_id: str, text: str, lang: str) -> str:
    content = f"{news_id}{text}{lang}"
    return hashlib.md5(content.encode('utf-8')).hexdigest()

def _sanitize_path_segment(value: str, fallback: str) -> str:
    sanitized = re.sub(r'[^a-zA-Z0-9_-]', '_', (value or '').strip())
    return sanitized or fallback

def resolve_cache_paths(app, news_id: str, lang: str, cache_key: str) -> tuple[str, str, str]:
    base_dir = app.state.AUDIO_FOLDER
    static_folder = app.state.STATIC_FOLDER
    news_segment = _sanitize_path_segment(news_id, 'unknown')
    lang_segment = _sanitize_path_segment(lang, 'unknown')
    request_segment = cache_key

    audio_dir = os.path.join(base_dir, news_segment, lang_segment, request_segment)
    final_path = os.path.join(audio_dir, 'tts.mp3')
    relative_path = os.path.relpath(final_path, static_folder)
    relative_path = relative_path.replace('\\', '/')
    return audio_dir, final_path, relative_path

def get_cached_file(request: Request, news_id: str, lang: str, cache_key: str) -> str | None:
    app = request.app
    _, final_path, relative_path = resolve_cache_paths(app, news_id, lang, cache_key)
    if os.path.exists(final_path):
        return str(request.url_for('static', path=relative_path))

    return None

def register_audio_file(app, news_id: str, lang: str, filename: str) -> None:
    """Manifest persistence disabled; ensure legacy manifest file is removed."""
    manifest_path = os.path.join(app.state.AUDIO_FOLDER, "manifest.json")
    if os.path.exists(manifest_path):
        try:
            os.remove(manifest_path)
        except Exception as exc:
            logger = getattr(app.state, "logger", None)
            if logger:
                logger.warning(f"Failed to delete legacy manifest file: {exc}")