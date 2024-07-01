import aiohttp
import asyncio
import logging


class ApiClient:

    async def get(self, url):

        max_retries = 5
        retry_count = 0

        print(f'URL IS {url}')
        while retry_count <= max_retries:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        if response.status == 200:
                            data = await response.text()
                            return data
                        elif response.status == 429:
                            if retry_count == max_retries:
                                logging.error(f'Max retries reached for URL {url}')
                                return None
                            retry_count += 1
                            print('\nSTART------------------')
                            print(f'Retrying..')
                            print(f'URL -> {url}')
                            print(f'RETRY COUNT -> {retry_count}')
                            print('END-----------------\n')
                            await asyncio.sleep(1)
                        else:
                            logging.error(f'Unexpected error code {response.status} from {url}')
                            return None
            except aiohttp.ClientError as e:
                logging.error(f'HTTP client error: {str(e)}')
                return None
            except Exception as e:
                logging.error(f'General error when fetching data: {str(e)}')
                return None
