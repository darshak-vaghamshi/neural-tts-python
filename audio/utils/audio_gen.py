import asyncio
import uuid
from typing import Iterable, List

import edge_tts
from pydub import AudioSegment

async def synthesize_edge(text: str, voice: str) -> str:
    temp_mp3 = f"temp_{uuid.uuid4().hex}.mp3"
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(temp_mp3)
    return temp_mp3

async def synthesize_chunks(
    text_chunks: Iterable[str],
    voice: str,
    max_concurrency: int = 2,
) -> List[str]:
    """Synthesize a batch of text chunks with optional concurrency control."""
    chunks = list(text_chunks)
    if not chunks:
        return []

    semaphore = asyncio.Semaphore(max(1, max_concurrency))

    async def _synthesize(index: int, chunk: str):
        async with semaphore:
            path = await synthesize_edge(chunk, voice)
            return index, path

    tasks = [asyncio.create_task(_synthesize(idx, chunk)) for idx, chunk in enumerate(chunks)]
    results = await asyncio.gather(*tasks)
    return [path for _, path in sorted(results, key=lambda item: item[0])]

def concatenate_mp3(mp3_files: list) -> str:
    combined = AudioSegment.empty()
    for mp3 in mp3_files:
        combined += AudioSegment.from_mp3(mp3)
    final_mp3 = f"final_{uuid.uuid4().hex}.mp3"
    combined.export(final_mp3, format="mp3", bitrate="128k")
    return final_mp3