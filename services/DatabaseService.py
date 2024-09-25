import aiomysql
import motor.motor_asyncio
import asyncpg
import aiosqlite
import json
import os

class DatabaseService:
    def __init__(self, config_path="cwim-core-tgbt/config.json"):
        self.config = None
        self.connection_pool = None
        self.mongo_client = None
        self.mongo_db = None
        self.sqlite_connection = None
        self.config_path = config_path
        self.active_db = None  # Для хранения информации о текущей активной базе данных

    async def load_config(self):
        """Загрузка конфигурации из файла"""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Config file {self.config_path} not found")

        with open(self.config_path, 'r') as config_file:
            config_data = json.load(config_file)

        # Проверка наличия секции databases
        if 'databases' not in config_data:
            raise ValueError("No databases configuration found")

        # Проверка доступных баз данных и выбора активной
        if 'mysqldb' in config_data['databases'] and config_data['databases']['mysqldb'].get('enabled', False):
            self.config = config_data['databases']['mysqldb']
            self.active_db = 'mysql'
            print("Using MySQL database")
        elif 'mongodb' in config_data['databases'] and config_data['databases']['mongodb'].get('enabled', False):
            self.config = config_data['databases']['mongodb']
            self.active_db = 'mongodb'
            print("Using MongoDB database")
        elif 'postgresql' in config_data['databases'] and config_data['databases']['postgresql'].get('enabled', False):
            self.config = config_data['databases']['postgresql']
            self.active_db = 'postgresql'
            print("Using PostgreSQL database")
        else:
            # Если ни одна база не активна, переключаемся на SQLite
            self.active_db = 'sqlite'
            db_path = "cwim-core-tgbt/datafiles/sqlite.db"
            os.makedirs(os.path.dirname(db_path), exist_ok=True)  # Создание директорий, если их нет
            self.sqlite_connection = await aiosqlite.connect(db_path)
            print(f"SQLite database created at {db_path}")

    async def init_connection(self):
        """Инициализация соединений с базой данных"""
        if self.active_db == 'mysql':
            self.connection_pool = await aiomysql.create_pool(
                user=self.config.get("user"),
                password=self.config.get("password"),
                db=self.config.get("database"),
                host=self.config.get("host", "localhost"),
                port=self.config.get("port", 3306),
                minsize=1,
                maxsize=10,
            )
        elif self.active_db == 'mongodb':
            self.mongo_client = motor.motor_asyncio.AsyncIOMotorClient(
                self.config.get("host", "localhost"),
                self.config.get("port", 27017)
            )
            self.mongo_db = self.mongo_client[self.config.get("database")]
            print(f"Connected to MongoDB: {self.config.get('database')}")
        elif self.active_db == 'postgresql':
            self.connection_pool = await asyncpg.create_pool(
                user=self.config.get("user"),
                password=self.config.get("password"),
                database=self.config.get("database"),
                host=self.config.get("host", "localhost"),
                port=self.config.get("port", 5432),
            )
        else:
            print("SQLite connection already initialized")

    async def execute_query(self, query, *args):
        """Выполнение запроса для MySQL или PostgreSQL"""
        if self.active_db == 'mysql':
            async with self.connection_pool.acquire() as connection:
                async with connection.cursor() as cursor:
                    await cursor.execute(query, args)
                    await connection.commit()
        elif self.active_db == 'postgresql':
            async with self.connection_pool.acquire() as connection:
                async with connection.transaction():
                    await connection.execute(query, *args)

    async def insert_document(self, collection_name, document):
        """Вставка документа в MongoDB"""
        if self.active_db == 'mongodb':
            collection = self.mongo_db[collection_name]
            result = await collection.insert_one(document)
            return result.inserted_id

    async def fetch_all(self, query=None, collection_name=None):
        """Получение всех документов из базы данных"""
        if self.active_db == 'mongodb':
            collection = self.mongo_db[collection_name]
            documents = await collection.find().to_list(length=None)
            return documents
        elif self.active_db in ('mysql', 'postgresql'):
            async with self.connection_pool.acquire() as connection:
                if self.active_db == 'mysql':
                    async with connection.cursor(aiomysql.DictCursor) as cursor:
                        await cursor.execute(query)
                        result = await cursor.fetchall()
                        return result
                else:  # PostgreSQL
                    async with connection.transaction():
                        return await connection.fetch(query)

    async def fetch_one(self, query, *args):
        """Получение одной строки результата для MySQL или PostgreSQL"""
        if self.active_db == 'mysql':
            async with self.connection_pool.acquire() as connection:
                async with connection.cursor(aiomysql.DictCursor) as cursor:
                    await cursor.execute(query, args)
                    result = await cursor.fetchone()
                    return result
        elif self.active_db == 'postgresql':
            async with self.connection_pool.acquire() as connection:
                async with connection.transaction():
                    return await connection.fetchrow(query, *args)

    async def close(self):
        """Закрытие соединений"""
        if self.active_db == 'mysql' and self.connection_pool:
            self.connection_pool.close()
            await self.connection_pool.wait_closed()
        elif self.active_db == 'mongodb':
            self.mongo_client.close()
        elif self.active_db == 'postgresql' and self.connection_pool:
            self.connection_pool.close()
            await self.connection_pool.wait_closed()
        elif self.sqlite_connection:
            await self.sqlite_connection.close()


# Пример использования
async def main():
    db_service = DatabaseService()

    try:
        # Загрузка конфигурации
        await db_service.load_config()

        # Инициализация соединений
        await db_service.init_connection()

        # Пример выполнения запроса (для MySQL/PostgreSQL)
        if db_service.active_db in ('mysql', 'postgresql'):
            await db_service.execute_query(
                "CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name TEXT)"
            )
            await db_service.execute_query(
                "INSERT INTO users (name) VALUES ($1)", "John Doe"
            )

            # Получение данных
            rows = await db_service.fetch_all("SELECT * FROM users")
            for row in rows:
                print(row)

        # Пример вставки документа в MongoDB
        elif db_service.active_db == 'mongodb':
            await db_service.insert_document("users", {"name": "John Doe"})
            documents = await db_service.fetch_all(collection_name="users")
            print("MongoDB Documents:", documents)

    finally:
        # Закрытие соединений
        await db_service.close()


# Запуск программы
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
