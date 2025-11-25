import pytest
import asyncio
import aiosqlite
import os
from database import init_db, add_visit, get_stats

TEST_DB = "test.db"

@pytest.mark.asyncio
async def test_add_and_get_stats():

    os.remove(TEST_DB)
    await init_db(TEST_DB)
    await add_visit("127.0.0.1", "Test-Agent", TEST_DB)
    await add_visit("127.0.0.2", "Test-Agent", TEST_DB)
    await add_visit("127.0.0.1", "Another-Agent", TEST_DB)  # Повторный IP

    stats = await get_stats("all", TEST_DB)
    
    assert stats['total'] == 3

    assert stats['unique'] == 2
