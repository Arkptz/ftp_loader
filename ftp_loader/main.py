import asyncio
import os

import aiofiles
import aiohttp

from ftp_loader.config import SETTINGS


async def launch(full_path):
    print(f"adding {full_path}....")
    data = aiohttp.FormData()
    # Используем aiofiles для асинхронного чтения файла
    async with aiofiles.open(full_path, "rb") as file:
        file_content = await file.read()  # Асинхронное чтение содержимого файла
        data.add_field(
            "file",
            file_content,
            filename="random",
            content_type="application/octet-stream",
        )

    url = "https://cdn.vitrinagram.ru/api/ftp/files/load_file"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as resp:
            print(await resp.json())
            if resp.status == 200:
                print(f"Success added {full_path}....")


async def start():
    files_to_add = []
    files = os.listdir(SETTINGS.path_with_images)
    for file_name in files:
        full_path = os.path.join(SETTINGS.path_with_images, file_name)
        if os.path.isfile(full_path):
            files_to_add.append(full_path)
    tasks = [asyncio.create_task(launch(full_path=path)) for path in files_to_add]
    await asyncio.wait(tasks)


def main():
    asyncio.run(start())


if __name__ == "__main__":
    main()
