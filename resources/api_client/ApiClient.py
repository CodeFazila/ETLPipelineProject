import aiohttp
import asyncio
import logging


class ApiClient:

    async def get(self, url):
        print("URL IS " + url)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.text()
                        return data
                    elif response.status == 429:
                        await asyncio.sleep(1)
                        return await self.get(url)
                    else:
                        logging.error(f"UNKNOWN ERROR")
        except aiohttp.ClientError as e:
            logging.error(f"HTTP client error: {str(e)}")
        except Exception as e:
            logging.error(f"General error when fetching data: {str(e)}")
