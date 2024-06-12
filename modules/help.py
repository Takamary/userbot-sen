# modules/help.py

from telethon import events

def register(client, command_registry):
    command_registry.append('.help - Показать список доступных команд')

    @client.on(events.NewMessage(pattern='.help'))
    async def help(event):
        # Группируем команды по модулю
        commands_by_module = {}
        for cmd in command_registry:
            parts = cmd.split(" - ")
            module_name = parts[0]
            command_description = " - ".join(parts[1:])
            if module_name not in commands_by_module:
                commands_by_module[module_name] = []
            commands_by_module[module_name].append(command_description)

        # Формируем сообщение с помощью
        help_message = "Доступные команды:\n\n"
        for module_name, commands in commands_by_module.items():
            help_message += f"{module_name}:\n"
            for command in commands:
                help_message += f"  - {command}\n"
            help_message += "\n"

        sent_message = await event.respond(help_message)

        # Удаляем сообщение с командой .help
        await client.delete_messages(event.chat_id, event.message)
