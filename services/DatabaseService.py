import json
import os
import logging

# Настройка логгирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


class JSONService:
    def __init__(self, data_file_path=None):
        if data_file_path is None:
            # Получаем путь к директории, где находится этот файл
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Определяем полный путь к файлу JSON
            data_file_path = os.path.join(current_dir, "../datafiles/database.json")

        self.data_file_path = os.path.abspath(data_file_path)  # Приводим к абсолютному пути
        logger.info(f"Используемый путь к файлу данных: {self.data_file_path}")
        self.data = self.load_data()

    def load_data(self):
        """Загрузка данных из файла JSON"""
        if not os.path.exists(self.data_file_path):
            logger.info(f"Файл {self.data_file_path} не найден. Создаем новый файл.")
            with open(self.data_file_path, 'w') as f:
                json.dump({}, f)  # Создаем пустой JSON объект
        with open(self.data_file_path, 'r') as f:
            logger.info(f"Загружаем данные из {self.data_file_path}")
            return json.load(f)

    def save_data(self):
        """Сохранение данных в файл JSON"""
        with open(self.data_file_path, 'w') as f:
            json.dump(self.data, f, indent=4)
        logger.info(f"Данные успешно сохранены в {self.data_file_path}")

    def create(self, section, record):
        """Создание записи в указанном разделе JSON"""
        if section not in self.data:
            self.data[section] = []

        # Проверка на дубликаты по всем полям
        for existing_record in self.data[section]:
            if all(existing_record.get(key) == value for key, value in record.items()):
                logger.warning(f"Найдена дубликат записи: {record}. Запись не создана.")
                return

        # Генерация уникального ID
        record_id = self._generate_id(section)
        record['id'] = record_id

        self.data[section].append(record)
        self.save_data()
        logger.info(f"Запись создана в разделе '{section}': {record}")

    def read(self, section):
        """Чтение всех записей из указанного раздела JSON"""
        return self.data.get(section, [])

    def update(self, section, record_id, updated_record):
        """Обновление записи по ID в указанном разделе"""
        if section in self.data:
            for idx, record in enumerate(self.data[section]):
                if record['id'] == record_id:
                    self.data[section][idx].update(updated_record)
                    self.save_data()
                    logger.info(f"Запись обновлена в разделе '{section}': {self.data[section][idx]}")
                    return
        logger.warning(f"Запись с ID {record_id} не найдена в разделе '{section}'.")

    def delete(self, section, record_id):
        """Удаление записи по ID в указанном разделе"""
        if section in self.data:
            for idx, record in enumerate(self.data[section]):
                if record['id'] == record_id:
                    deleted_record = self.data[section].pop(idx)
                    self.save_data()
                    logger.info(f"Запись удалена из раздела '{section}': {deleted_record}")
                    return
        logger.warning(f"Запись с ID {record_id} не найдена в разделе '{section}'.")

    def find_one(self, section, query):
        """Поиск одной записи по критериям в указанном разделе"""
        if section in self.data:
            for record in self.data[section]:
                if all(record.get(key) == value for key, value in query.items()):
                    return record
        return None

    def find_all(self, section, query):
        """Поиск всех записей по критериям в указанном разделе"""
        if section in self.data:
            return [record for record in self.data[section] if
                    all(record.get(key) == value for key, value in query.items())]
        return []

    def _generate_id(self, section):
        """Генерация уникального ID для новой записи"""
        if section not in self.data or not self.data[section]:
            return 1
        return max(record['id'] for record in self.data[section]) + 1

    def test_connection(self):
        """Тестирует соединение с файлом JSON, проверяя его доступность и читаемость"""
        if os.path.exists(self.data_file_path) and os.access(self.data_file_path, os.R_OK | os.W_OK):
            logger.info(f"Файл {self.data_file_path} доступен для чтения и записи")
            return True
        logger.error(f"Файл {self.data_file_path} не доступен для чтения или записи")
        return False


# # Пример использования
# if __name__ == "__main__":
#     db_service = JSONService()
#
#     # Тестируем соединение
#     if db_service.test_connection():
#         # Создание записей
#         db_service.create('users', {'login': 'user1', 'password': 'pass1', 'email': 'user1@example.com'})
#         db_service.create('users', {'login': 'user1', 'password': 'pass2',
#                                     'email': 'user2@example.com'})  # Дубликат по login и email
#         db_service.create('users', {'login': 'user2', 'password': 'pass2', 'email': 'user2@example.com'})  # Новый
#
#         # Поиск одной записи
#         user_record = db_service.find_one('users', {'login': 'user1'})
#         print("Найдена запись:", user_record)
#
#         # Поиск всех записей с определённым условием
#         all_users = db_service.find_all('users', {'password': 'pass2'})
#         print("Все подходящие записи:", all_users)
#
#         # Чтение всех записей
#         records = db_service.read('users')
#         print("Текущие записи в 'users':", records)
#
#         # Обновление записи
#         if records:
#             db_service.update('users', records[0]['id'], {'password': 'new_password'})
#
#         # Удаление записи
#         if records:
#             db_service.delete('users', records[0]['id'])
