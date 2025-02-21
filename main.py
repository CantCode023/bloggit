from src.agents.blogger import run

import asyncio
import nest_asyncio
nest_asyncio.apply()

async def main():
    await run("Generate a blog about my github repository, https://github.com/CantCode023/evoke")
    
if __name__ == "__main__":
    asyncio.run(main())