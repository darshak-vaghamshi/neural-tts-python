from fastapi import APIRouter
from ..config import SUPPORTED_LANGUAGES

router = APIRouter(prefix="/languages", tags=["languages"])

@router.get("")
async def get_languages():
    return {"languages": SUPPORTED_LANGUAGES}