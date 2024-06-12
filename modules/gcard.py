# modules/gcard.py

import asyncio
from telethon import events

gcard_task = None

async def send_periodic_gcard(client, chat_id):
    while True:
        await client.send_message(chat_id, 'Получить карту')
        await asyncio.sleep(14460)  # Ждем 14460 секунд

def register(client, command_registry):
    command_registry.append('gcard - .gstop - Остановить получение карт')
    command_registry.append('gcard - .gcard - Запустить получение карт')

    @client.on(events.NewMessage(pattern='.gstop'))
    async def stop_gcard(event):
        global gcard_task
        if gcard_task:
            gcard_task.cancel()
            gcard_task = None
            await event.respond('Отправка карт остановлена и таймер сброшен.')
        else:
            await event.respond('Отправка карт не была запущена.')

    @client.on(events.NewMessage(pattern='.gcard'))
    async def start_gcard(event):
        global gcard_task
        if gcard_task:
            await event.respond('Отправка карт уже запущена.')
        else:
            gcard_task = asyncio.create_task(send_periodic_gcard(client, event.chat_id))
            await event.respond('Отправка карт запущена.')
