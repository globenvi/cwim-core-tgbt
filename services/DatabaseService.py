import json
import os


class JSONService:
    def __init__(self, data_file_path="./cwim-core-tgbt/datafiles/database.json"):
        self.data_file_path = data_file_path
        self.data = self.load_data()

    def load_data(self):
        """Загрузка данных из файла JSON"""
        if not os.path.exists(self.data_file_path):
            with open(self.data_file_path, 'w') as f:
                json.dump({}, f)  # Создаем пустой JSON объект
        with open(self.data_file_path, 'r') as f:
            return json.load(f)

    def save_data(self):
        """Сохранение данных в файл JSON"""
        with open(self.data_file_path, 'w') as f:
            json.dump(self.data, f, indent=4)

    def create(self, section, record):
        """Создание записи в указанном разделе JSON"""
        if section not in self.data:
            self.data[section] = []

        # Проверка на дубликаты по всем полям
        for existing_record in self.data[section]:
            if all(existing_record.get(key) == value for key, value in record.items()):
                print(f"Duplicate record found: {record}. Record not created.")
                return

        # Генерация уникального ID
        record_id = self._generate_id(section)
        record['id'] = record_id

        self.data[section].append(record)
        self.save_data()
        print(f"Record created in section '{section}': {record}")

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
                    print(f"Record updated in section '{section}': {self.data[section][idx]}")
                    return
        print(f"Record with ID {record_id} not found in section '{section}'.")

    def delete(self, section, record_id):
        """Удаление записи по ID в указанном разделе"""
        if section in self.data:
            for idx, record in enumerate(self.data[section]):
                if record['id'] == record_id:
                    deleted_record = self.data[section].pop(idx)
                    self.save_data()
                    print(f"Record deleted from section '{section}': {deleted_record}")
                    return
        print(f"Record with ID {record_id} not found in section '{section}'.")

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
            return [record for record in self.data[section] if all(record.get(key) == value for key, value in query.items())]
        return []

    def _generate_id(self, section):
        """Генерация уникального ID для новой записи"""
        if section not in self.data or not self.data[section]:
            return 1
        return max(record['id'] for record in self.data[section]) + 1


# # Пример использования
# async def main():
#     db_service = JSONService()
#
#     # Создание записей
#     db_service.create('users', {'login': 'user1', 'password': 'pass1', 'email': 'user1@example.com'})
#     db_service.create('users', {'login': 'user1', 'password': 'pass2', 'email': 'user2@example.com'})  # Дубликат по login и email
#     db_service.create('users', {'login': 'user2', 'password': 'pass2', 'email': 'user2@example.com'})  # Новый
#
#     # Поиск одной записи
#     user_record = db_service.find_one('users', {'login': 'user1'})
#     print("Found record:", user_record)
#
#     # Поиск всех записей с определённым условием
#     all_users = db_service.find_all('users', {'password': 'pass2'})
#     print("All matching records:", all_users)
#
#     # Чтение всех записей
#     records = db_service.read('users')
#     print("Current records in 'users':", records)
#
#     # Обновление записи
#     if records:
#         db_service.update('users', records[0]['id'], {'password': 'new_password'})
#
#     # Удаление записи
#     if records:
#         db_service.delete('users', records[0]['id'])
#
#
# # Запуск примера
# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(main())
