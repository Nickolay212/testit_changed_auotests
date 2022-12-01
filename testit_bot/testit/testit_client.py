import asyncio

import aiohttp
from aiohttp import ClientSession

from testit_bot.db.db import ActionMongoDBMotor, ConnectionMongoDBMotor
from testit_bot.testit.api.testit_client_api import TestItClientApi


class TestitClient:
    def __init__(self, url, private_token, project_id):
        self.__url = url
        self.__private_token = private_token
        self.testit_client_api = TestItClientApi(url=self.__url, private_token=self.__private_token)
        self.project_id = project_id

    async def create_entities_in_batches(self,
                                         function,
                                         entities_count: int,
                                         entities_per_account: int,
                                         **kwargs):
        """
        Создание сущностей по партиям. \n
        Нельзя пропустить через сессию разом весь датасет сущностей. \n
        Поэтому делим данные на партии. \n
        :param function: функция (корутина), в которой асинхронно создаем сущности по партиям.
        :param entities_count: общее количество сущностей.
        :param entities_per_account: количество сущностей, которое будет создаваться за один цикл.
        """
        tasks = []
        skip = 0  # количество пройденных сущностей
        loops = entities_count // entities_per_account  # за каждый цикл создается entities_per_account сущностей
        remainder = entities_count % entities_per_account  # остаток. Оставшееся количество сущностей для создания
        async with aiohttp.ClientSession() as session:
            for i, count in enumerate([loops, remainder]):
                if i == 1:
                    entities_per_account = remainder
                    count = 1
                for _ in range(count):
                    await asyncio.sleep(1)  # задержка между созданием очередной партии entities_per_account сущностей
                    # Корутина, которая содержит таски
                    tasks.append(asyncio.create_task(function(session,
                                                              skip,
                                                              entities_per_account,
                                                              **kwargs)))
                    await asyncio.gather(*tasks)
                    skip += entities_per_account

    async def write_autotests_to_db(self,
                                    session: ClientSession,
                                    skip: int,
                                    take: int,
                                    action_mongodb_motor: ActionMongoDBMotor):
        """
        Запись автотестов в БД (по проекту). \n
        :param session: открытая сессия клиента по aiohttp.
        :param skip: граница пропущенных автотестов.
        :param take: количество выбранных для записи автотестов.
        :param action_mongodb_motor: асинхронная библиотека для работы с коллекцией mongoDB.
        """
        # Запрашивает данные по автотестам в testit (по проекту)
        data = await self.testit_client_api.get_autotests(session=session,
                                                          project_id=self.project_id,
                                                          skip=skip,
                                                          take=take)
        # Записывает запрошенные данные по автотестам в mongoDB
        await action_mongodb_motor.insert_many_to_db(data=data)

    async def get_autotests_count(self):
        async with aiohttp.ClientSession() as session:
            response = await self.testit_client_api.get_project_project_id(session=session, project_id=self.project_id)
        # Общее количество кейсов
        return response['autoTestsCount']

    async def find_all_approve_autotests_to_testit(self, action_mongodb_motor: ActionMongoDBMotor):
        # Поиск кейсов, в которых есть изменения
        data = {'mustBeApproved': True}
        list_documents = await action_mongodb_motor.find_all_approve_autotests(data=data)
        return list_documents

    # async def find_all_approve_autotests_to_testit(self,
    #                                                connect_mongodb,
    #                                                entities_per_account: int = 400):
    #     """
    #     Поиск автотестов в testit, у которых имеется отметка об изменении. \n
    #     :param entities_per_account: количество сущностей, которое будет создаваться за один цикл.
    #     """
    #     # Создаем коллекцию
    #     collection = connect_mongodb.testit_approved_db.testit_approved_collection
    #     action_mongodb_motor = ActionMongoDBMotor(collection=collection)
    #
    #     # Очищаем коллекцию testit_approved_collection
    #     await action_mongodb_motor.delete_all_db()
    #
    #     async with aiohttp.ClientSession() as session:
    #         response = await self.testit_client_api.get_project_project_id(session=session,
    #                                                                        project_id=self.project_id)
    #     # Общее количество кейсов
    #     autotests_count = response['autoTestsCount']
    #
    #     await self.create_entities_in_batches(function=self.write_autotests_to_db,
    #                                           entities_count=autotests_count,
    #                                           entities_per_account=entities_per_account,
    #                                           action_mongodb_motor=action_mongodb_motor)
    #
    #     # Поиск кейсов, в которых есть изменения
    #     data = {'mustBeApproved': True}
    #     list_documents = await action_mongodb_motor.find_all_approve_autotests(data=data)
    #     return list_documents
