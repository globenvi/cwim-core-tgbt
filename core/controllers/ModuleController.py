from services.DatabaseService import JSONService

class Module(JSONService):
    def __init__(self, module_name=None):
        super().__init__()  # Инициализация родительского класса
        self.module_name = module_name

    async def init(self):
        """Инициализация базы данных."""
        await super().init()

    async def create_module(self):
        """Создаёт новую запись модуля в базе данных."""
        module_data = {
            'module_name': self.module_name,
            'status': 'installed'
        }
        await self.create('modules', module_data)

    async def read_module(self):
        """Читает данные модуля из базы данных по имени."""
        if self.data is None:
            await self.init()
        return await self.find_one('modules', {'module_name': self.module_name})

    async def update_module(self, updated_data):
        """Обновляет данные модуля в базе данных."""
        existing_module = await self.read_module()
        if existing_module:
            await self.update('modules', existing_module['id'], updated_data)

    async def delete_module(self):
        """Удаляет запись модуля из базы данных."""
        existing_module = await self.read_module()
        if existing_module:
            await self.delete('modules', existing_module['id'])

    async def list_modules(self):
        """Получает список всех модулей."""
        if self.data is None:
            await self.init()
        return await self.find('modules')
