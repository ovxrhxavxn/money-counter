import asyncio

import uvicorn

from src.database.sqlalchemy import create_tables


async def main():
    await create_tables()

    uvicorn.run(
        app='src.app:app',
        host='localhost',
        reload=True
    )


if __name__ == "__main__":
    asyncio.run(main())