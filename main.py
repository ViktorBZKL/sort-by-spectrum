import os
import cv2
import shutil
import zipfile
import warnings
from sort import sort
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types

load_dotenv()

warnings.filterwarnings("ignore")

bot = Bot(token=os.environ.get('TOKEN'))
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer("Для сортировки изображений по цветам спектра отправьте мне архив zip с картинками внутри. Следите за тем, чтобы внутри архива находились только изображения формата jpg и названия файлов не содержали кириллические символы.")
    user_id = str(message.from_user.id)

    if not os.path.exists(f"{user_id}/output"):
        os.makedirs(f"{user_id}/output")


@dp.message_handler(content_types=types.ContentTypes.DOCUMENT)
async def handle_documet(message: types.Message):
    if not message.document.file_name.endswith('.zip'):
        await message.answer('Вы отправили не zip архив')
        return

    await message.answer('Процесс сортировки начался...')
    user_id = str(message.from_user.id)
    await message.document.download(f"{user_id}/archive.zip")

    input_path = f"{user_id}/unpacked"

    try:
        with zipfile.ZipFile(f'{user_id}/archive.zip', 'r') as zip_ref:
            zip_ref.extractall(f'{user_id}/unpacked')

        output_path = f"{user_id}/output"
        sort(input_path, output_path)
        zip_file = f'{user_id}/output.zip'
        with zipfile.ZipFile(zip_file, 'w') as zip_ref:
            for root, dirs, files in os.walk(output_path):
                for file in files:
                    zip_ref.write(os.path.join(root, file), os.path.relpath(
                        os.path.join(root, file), output_path))

        await bot.send_document(user_id, types.InputFile(zip_file))
        os.remove(zip_file)
        files = os.listdir(output_path)

        for file in files:
            # await message.answer_document(open(f"{output_path}/{file}", 'rb'))
            os.remove(f"{output_path}/{file}")
        os.rmdir(f'{user_id}/unpacked')

    except cv2.error:
        await message.answer('Что-то пошло не так. Убедитесь, что архив соответствует требованиям')
        shutil.rmtree(f'{user_id}/unpacked')
    except Exception:
        await message.answer('Произошла ошибка, убедитесь, что вы отправили один архив zip и файлы в нем соответствую требованиям')
        shutil.rmtree(f'{user_id}/unpacked')

    os.remove(f'{user_id}/archive.zip')


@dp.message_handler(content_types=types.ContentTypes.PHOTO)
async def handle_documet(message: types.Message):
    await message.answer('Вы отправили фотографию, а не архив')

if __name__ == '__main__':
    executor.start_polling(dp)
