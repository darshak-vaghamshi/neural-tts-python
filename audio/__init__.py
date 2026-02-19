import asyncio
import logging
import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .utils.cleanup import cleanup_old_files

CACHE_TTL_SECONDS = 9 * 60
CLEANUP_INTERVAL_SECONDS = 60


def create_app() -> FastAPI:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_folder = os.path.join(base_dir, 'static')
    audio_folder = os.path.join(static_folder, 'audio_cache')

    app = FastAPI()
    app.mount('/static', StaticFiles(directory=static_folder), name='static')

    os.makedirs(audio_folder, exist_ok=True)
    app.state.AUDIO_FOLDER = audio_folder
    app.state.STATIC_FOLDER = static_folder
    app.state.logger = logging.getLogger('uvicorn.error')
    app.state.cleanup_task = None

    from .api.speak import router as speak_router
    from .api.languages import router as languages_router

    app.include_router(speak_router)
    app.include_router(languages_router)

    @app.on_event("startup")
    async def start_cleanup_task():
        async def _cleanup_loop():
            while True:
                try:
                    cleanup_old_files(audio_folder, CACHE_TTL_SECONDS)
                except Exception as exc:
                    app.state.logger.warning(f"Cleanup task error: {exc}")
                await asyncio.sleep(CLEANUP_INTERVAL_SECONDS)

        app.state.cleanup_task = asyncio.create_task(_cleanup_loop())

    @app.on_event("shutdown")
    async def stop_cleanup_task():
        task = app.state.cleanup_task
        if task:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
            app.state.cleanup_task = None

    return app