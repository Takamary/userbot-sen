import os
import importlib
from telethon import TelegramClient, events
from telethon.tl.types import DocumentAttributeFilename
from config import API_ID, API_HASH, BOT_TOKEN, SESSION_NAME, MODULES_FOLDER

client = TelegramClient(SESSION_NAME, API_ID, API_HASH).start(bot_token=BOT_TOKEN)

command_registry = []

def load_modules(folder):
    for filename in os.listdir(folder):
        if filename.endswith('.py'):
            module_name = filename[:-3]
            module = importlib.import_module(f'{folder}.{module_name}')
            if hasattr(module, 'register'):
                module.register(client, command_registry)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond('Бот запущен и готов к работе!')
    raise events.StopPropagation

@client.on(events.NewMessage(incoming=True, func=lambda e: e.file))
async def handler_file(event):
    # Проверяем, что файл является модулем Python
    if event.document and any(isinstance(attr, DocumentAttributeFilename) and attr.file_name.endswith('.py') for attr in event.document.attributes):
        # Сохраняем файл в папку modules
        path = os.path.join(MODULES_FOLDER, event.file.name)
        await client.download_media(event.message, path)
        await event.respond(f'Файл {event.file.name} получен и сохранен.')
        # Перезагружаем модули после получения нового файла
        command_registry.clear()
        load_modules(MODULES_FOLDER)
        await event.respond('Новый модуль загружен и активирован.')

# Загружаем модули
load_modules(MODULES_FOLDER)

# Запуск бота
print("Бот запущен...")
client.run_until_disconnected()
