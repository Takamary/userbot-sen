# modules/server_info.py

import psutil
import platform
from datetime import datetime
from telethon import events

def get_system_info():
    uname = platform.uname()
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    memory_total = memory.total / (1024 ** 3)  # Convert to GB
    memory_used = memory.used / (1024 ** 3)  # Convert to GB
    memory_free = memory.free / (1024 ** 3)  # Convert to GB

    info = (
        f"Система: {uname.system} {uname.release}\n"
        f"Название узла: master\n"
        f"Версия: 1.0\n"
        f"Процессор: {uname.processor}\n"
        f"Загрузка ЦП: {cpu_usage}%\n"
        f"Всего ОЗУ: {memory_total:.2f} GB\n"
        f"Использовано ОЗУ: {memory_used:.2f} GB\n"
        f"Свободно ОЗУ: {memory_free:.2f} GB\n"
        f"Время с момента загрузки: {boot_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
    )

    return info

def register(client, command_registry):
    command_registry.append('.info - Показать информацию о сервере')

    @client.on(events.NewMessage(pattern='.info'))
    async def server_info(event):
        info = get_system_info()
        await event.respond(info)
        # Удаляем сообщение с командой .info
        await client.delete_messages(event.chat_id, event.message)
