# modules/ping.py

import time
from telethon import events

def register(client, command_registry):
    command_registry.append('.ping - Показать задержку в миллисекундах')

    @client.on(events.NewMessage(pattern='.ping'))
    async def ping(event):
        start_time = time.time()
        sent_message = await event.respond('Pong!')
        end_time = time.time()
        latency = (end_time - start_time) * 1000  # Convert to milliseconds
        await sent_message.edit(f'Pong! Задержка: {latency:.2f} ms')
        # Удаляем сообщение с командой .ping
        await client.delete_messages(event.chat_id, event.message)
