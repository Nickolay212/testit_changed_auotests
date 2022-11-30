import os

import requests as requests
from aiogram.types import Message
from aiogram.dispatcher.filters import CommandObject, Command
from aiogram import Router

from testit_bot.create_bot import connect_mongodb, testit_client, bot, config
from testit_bot.db.db import ActionMongoDBMotor
from testit_bot.handlers.bot_commands import bot_commands
from testit_bot.utils.utils import write_to_csv, get_project_root, get_path_file


async def help_command(message: Message, command: CommandObject):
    if command.args:
        for cmd in bot_commands:
            if cmd[0] == command.args:
                return await message.answer(f"{cmd[0]} - {cmd[1]}\n\n{cmd[2]}")
        return await message.answer("Введена неправильная команда")
    return await message.answer("Помощь и справка о боте\n"
                                "Чтобы получить информацию о команде\n"
                                "Введите: /help <команда> \n")


async def testit_find_all_changed_autotest_command(message: Message):
    # возвращать сообщения о подключениях и т.д.
    entities_per_account = 400

    await message.answer('Происходит выполнение операций...')
    await message.answer('* Создаем коллекцию в mongodb')
    collection = connect_mongodb.testit_approved_db.testit_approved_collection
    action_mongodb_motor = ActionMongoDBMotor(collection=collection)

    # Очищаем коллекцию testit_approved_collection
    await action_mongodb_motor.delete_all_db()

    await message.answer('* Получаем общее количество автотестов')
    autotests_count = await testit_client.get_autotests_count()

    await message.answer(f'* Добавляем все автотесты ({autotests_count}) в mongodb')
    await testit_client.create_entities_in_batches(function=testit_client.write_autotests_to_db,
                                                   entities_count=autotests_count,
                                                   entities_per_account=entities_per_account,
                                                   action_mongodb_motor=action_mongodb_motor)

    await message.answer('* Ищем измененные автотесты')
    result = await testit_client.find_all_approve_autotests_to_testit(action_mongodb_motor=action_mongodb_motor)

    [write_to_csv(name_file='testit_changed_autotests', values=row) for row in result]

    await message.answer('* Выгружаем файл в формате csv')
    path = get_path_file(path=get_project_root(),
                         name='testit_changed_autotests',
                         ext='csv')
    url = 'https://api.telegram.org/bot{}/sendDocument'.format(config.tg_bot.token)
    data = {'chat_id': message.from_user.id, 'caption': 'Результат парсинга'}
    with open(path, 'rb') as f:
        files = {'document': f}
        requests.post(url, data=data, files=files)

    # удаляем файл
    if os.path.isfile(path):
        os.remove(path)


def register_client_command(router: Router) -> None:
    router.message.register(help_command, Command(commands=['help']))
    router.message.register(testit_find_all_changed_autotest_command, Command(commands=['testit_changed_autotests']))
