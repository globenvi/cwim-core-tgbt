from services.DatabaseService import JSONService


class User(JSONService):
    def __init__(self, user=None, tgid=None, username=None, first_name=None, last_name=None, language_code=None,
                 is_premium=None, is_bot=None):
        super().__init__()  # Инициализация родительского класса

        if isinstance(user, dict):  # Если передан словарь с данными
            self.tgid = user.get('tgid')
            self.username = user.get('username')
            self.first_name = user.get('first_name')
            self.last_name = user.get('last_name')
            self.language_code = user.get('language_code')
            self.is_premium = user.get('is_premium')
            self.is_bot = user.get('is_bot')

        elif hasattr(user, 'id'):  # Если передан объект (например, из aiogram)
            self.tgid = user.id
            self.username = user.username
            self.first_name = user.first_name
            self.last_name = user.last_name
            self.language_code = user.language_code
            self.is_premium = user.is_premium
            self.is_bot = user.is_bot

        else:  # Если переданы отдельные параметры
            self.tgid = tgid
            self.username = username
            self.first_name = first_name
            self.last_name = last_name
            self.language_code = language_code
            self.is_premium = is_premium
            self.is_bot = is_bot

    async def init(self):
        """Инициализация базы данных."""
        await super().init()  # Вызов метода инициализации родительского класса

    async def create_user(self):
        """Создаёт новую запись пользователя в базе данных."""
        user_data = {
            'tgid': self.tgid,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'user_group': 'user',
            'steam_id': None,
            'language_code': self.language_code,
            'is_premium': self.is_premium,
            'is_bot': self.is_bot
        }

        # Создаем стандартные настройки.
        user_settings = {
            'tgid': self.tgid,
            'dark_mode': False,
            'notifications': False,
        }

        await self.create('users', user_data)
        await self.create('users_settings', user_settings)

    async def read_user(self):
        """Читает данные пользователя из базы данных по tgid."""
        if self.data is None:
            await self.init()  # Инициализация, если данные еще не загружены
        return await self.find_one('users', {'tgid': self.tgid})

    async def update_user(self, updated_data):
        """Обновляет данные пользователя в базе данных."""
        existing_user = await self.read_user()
        if existing_user:
            await self.update('users', existing_user['id'], updated_data)

    async def delete_user(self):
        """Удаляет запись пользователя из базы данных."""
        existing_user = await self.read_user()
        if existing_user:
            await self.delete('users', existing_user['id'])

    async def read_user_settings(self):
        """Читает настройки пользователя."""
        if self.data is None:
            await self.init()
        return await self.find_one('users_settings', {'tgid': self.tgid})

    async def update_user_settings(self, updated_data):
        """Обновляет данные пользователя в базе данных."""
        existing_user = await self.read_user()
        if existing_user:
            await self.update('users_settings', existing_user['id'], updated_data)
