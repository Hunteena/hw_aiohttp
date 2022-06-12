import asyncio

import aiohttp

HOST = 'http://127.0.0.1:8080'


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.post(
                f"{HOST}/advs/",
                json={
                    'title': 'new title 2',
                    'desc': 'new description',
                    'owner': 1000
                }
        ) as response:
            print(response.status)
            print(await response.json())

        async with session.get(f"{HOST}/advs/1/") as response:
            print(response.status)
            print(await response.json())

        async with session.get(f"{HOST}/advs/30/") as response:
            print(response.status)
            print(await response.json())

        async with session.patch(
                f"{HOST}/advs/2/",
                json={
                    'title': 'newer title',
                    'desc': 'new description 1'
                }
        ) as response:
            print(response.status)
            print(await response.json())

        async with session.delete(f"{HOST}/advs/2/") as response:
            print(response.status)
            print(await response.json())


asyncio.run(main())
