import asyncio
import shutil
from pathlib import Path
from argparse import ArgumentParser
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


async def copy_file(file: Path, output_folder: Path):
    try:
        ext = file.suffix.lower()[1:]
        if not ext:
            ext = "unknown"

        target_folder = output_folder / ext
        target_folder.mkdir(parents=True, exist_ok=True)

        target_path = target_folder / file.name
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, shutil.copy, file, target_path)

        logging.info(f"Копійовано: {file} → {target_path}")
    except Exception as e:
        logging.error(f"Помилка при копіюванні {file}: {e}")


async def read_folder(source_folder: Path, output_folder: Path):
    try:
        tasks = []

        for item in source_folder.rglob("*"):
            if item.is_file():
                tasks.append(copy_file(item, output_folder))

        await asyncio.gather(*tasks)

        logging.info("Сортування завершено.")
    except Exception as e:
        logging.error(f"Помилка при читанні папки {source_folder}: {e}")


async def main():
    parser = ArgumentParser(description="Асинхронне сортування файлів за розширеннями.")
    parser.add_argument("source", type=str, help="Шлях до вихідної папки")
    parser.add_argument("output", type=str, help="Шлях до папки призначення")

    args = parser.parse_args()
    source_folder = Path(args.source)
    output_folder = Path(args.output)

    if not source_folder.exists() or not source_folder.is_dir():
        logging.error(f"Вихідна папка {source_folder} не існує або не є директорією.")
        return

    output_folder.mkdir(parents=True, exist_ok=True)

    await read_folder(source_folder, output_folder)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Скрипт завершено користувачем.")
