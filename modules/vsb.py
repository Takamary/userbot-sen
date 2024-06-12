# modules/vsb.py

import asyncio
from telethon import events

vsb_task = None

async def send_periodic_messages(client, chat_id):
    while True:
        await client.send_message(chat_id, '/beer')
        await client.send_message(chat_id, '/vino')
        await client.send_message(chat_id, '/sushi')
        await asyncio.sleep(3660)  # Ждем час и 1 минуту (3660 секунд)

def register(client, command_registry):
    command_registry.append('vsb - .vsbstop - Остановить отправку периодических сообщений')
    command_registry.append('vsb - .vsbstart - Запустить отправку периодических сообщений')

    @client.on(events.NewMessage(pattern='.vsbstop'))
    async def stop_vsb(event):
        global vsb_task
        if vsb_task:
            vsb_task.cancel()
            vsb_task = None
            await event.respond('Периодическая отправка сообщений остановлена и таймер сброшен.')
        else:
            await event.respond('Периодическая отправка сообщений не была запущена.')

    @client.on(events.NewMessage(pattern='.vsbstart'))
    async def start_vsb(event):
        global vsb_task
        if vsb_task:
            await event.respond('Периодическая отправка сообщений уже запущена.')
        else:
            vsb_task = asyncio.create_task(send_periodic_messages(client, event.chat_id))
            await event.respond('Периодическая отправка сообщений запущена.')
