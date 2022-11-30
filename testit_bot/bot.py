import asyncio

from testit_bot.create_bot import bot, dp
from testit_bot.handlers.bot_commands import bot_commands
from testit_bot.handlers.client import register_client_command

from aiogram.types import BotCommand


async def main():
    register_client_command(dp)

    # Всплывающая подсказка
    commands_for_bot = []
    for cmd in bot_commands:
        commands_for_bot.append(BotCommand(command=cmd[0], description=cmd[1]))
    # активировать всплывающую подсказку
    await bot.set_my_commands(commands=commands_for_bot)

    # start
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped!")
