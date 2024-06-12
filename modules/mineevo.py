import asyncio
from telethon import events

mine_task = None

async def send_periodic_mine(client, bot_username):
    while True:
        await client.send_message(bot_username, 'коп')
        await asyncio.sleep(3)  # Ждем 4 секунды

def register(client, command_registry):
    command_registry.append('mine - .mstop - Остановить автоматическое копание')
    command_registry.append('mine - .mmine - Запустить автоматическое копание')

    @client.on(events.NewMessage(pattern='.mstop'))
    async def stop_mine(event):
        global mine_task
        if mine_task:
            mine_task.cancel()
            mine_task = None
            await event.respond('Автоматическое копание остановлено.')
        else:
            await event.respond('Автоматическое копание не было запущено.')

    @client.on(events.NewMessage(pattern='.mmine'))
    async def start_mine(event):
        global mine_task
        if mine_task:
            await event.respond('Автоматическое копание уже запущено.')
        else:
            bot_username = '@mine_evo_gold_bot'  # Укажите имя пользователя бота
            mine_task = asyncio.create_task(send_periodic_mine(client, bot_username))
            await event.respond('Автоматическое копание запущено.')
