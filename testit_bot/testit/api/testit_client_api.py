""" Testit. Swagger: https://testit.zyfra.com/swagger/index.html. Группа методов для работы с testit через API. """
from aiohttp import ClientSession


class TestItClientApi:
    """
    Testit. Swagger: https://testit.zyfra.com/swagger/index.html. \n
    Группа методов для работы с testit через API.
    """
    def __init__(self, url, private_token):
        self.url = url
        self.private_token = private_token
        self.headers = {'Authorization': f'PrivateToken {self.private_token}'}

    async def get_autotests(self, session: ClientSession, project_id: str, skip: int, take: int):
        """
        GET/autoTests \n
        Получить список автотестов. \n
        :param session: открытая сессия клиента по aiohttp.
        :param project_id: ИД проекта.
        :param skip: граница пропущенных автотестов.
        :param take: количество выбранных для записи автотестов.
        """
        async with session.get(f'{self.url}/api/v2/autoTests',
                               headers=self.headers,
                               params={
                                   "projectId": project_id,
                                   "Skip": skip,
                                   "Take": take
                               }
                               ) as response:
            return await response.json()

    async def get_project_project_id(self, session, project_id: str):
        """
        GET/projects/project_id \n
        Получить проект по ИД. \n
        :param session: открытая сессия клиента по aiohttp.
        :param project_id: ИД проекта.
        """
        async with session.get(f'{self.url}/api/v2/projects/{project_id}',
                               headers=self.headers
                               ) as response:
            return await response.json()
