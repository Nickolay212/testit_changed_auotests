import json

import motor.motor_asyncio


class ConnectionMongoDBMotor:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connect_db(self):
        return motor.motor_asyncio.AsyncIOMotorClient(self.host, self.port, serverSelectionTimeoutMS=5000)


class ActionMongoDBMotor:
    def __init__(self, collection):
        self.collection = collection

    async def insert_one_to_db(self, data: json):
        await self.collection.insert_one(document=data)

    async def insert_many_to_db(self, data: list):
        await self.collection.insert_many(documents=data)

    async def find_one_to_db(self, data: json):
        return await self.collection.find_one(data)

    async def delete_all_db(self):
        await self.collection.delete_many({})

    async def find_all_approve_autotests(self, data: json) -> list:
        cursor = self.collection.find(data)
        list_documents = [['global_id', 'external_id', 'name', 'namespace', 'classname']]
        for doc in await cursor.to_list(length=5000):
            global_id = doc['globalId']
            external_id = doc['externalId']
            name = doc['name']
            namespace = doc['namespace']
            classname = doc['classname']
            list_documents.append([global_id, external_id, name, namespace, classname])
        return list_documents
