# Интеграция MongoDB и графовых моделей данных

**Студент:** Зубикова Злата Павловна  
**Группа:** 5130203/50201  
**Тема:** Integration of MongoDB and Graph Data Models

## Описание проекта

Данный проект представляет собой исследование способов хранения графовых структур в документно-ориентированной базе данных MongoDB. В качестве предметной области выбрана сеть авиаперелетов между городами Азии.

### Цели и задачи
* Провести сравнительный анализ подходов к хранению графов в MongoDB.
* Спроектировать граф авиаперелетов (131 город, около 600 маршрутов).
* Реализовать загрузку данных и запросы на языке Python.
* Провести тестирование производительности MongoDB по сравнению с локальными структурами данных Python.
* Визуализировать граф и реализовать алгоритм Дейкстры для поиска кратчайшего пути.

## Структура проекта

```text
Integration_of_MongoDB_and_Graph_Data_Models/
│
├── data/
│   ├── cities.json            # 131 город (вершины)
│   └── routes.json            # около 600 маршрутов (ребра)
│
├── src/
│   ├── config.py              # Подключение к MongoDB
│   ├── generate_data.py       # Генерация тестовых данных
│   ├── load_data.py           # Загрузка данных в MongoDB
│   ├── queries.py             # Запросы 1 и 2 уровня
│   ├── p_test.py              # Тестирование производительности
│   └── visualize.py           # Визуализация и алгоритм Дейкстры
│
├── output/
│   └── asia_flights_graph.png # Визуализация графа
│
├── .env                       # Переменные окружения
├── .gitignore                 # Игнорируемые файлы
├── README.md                  # Описание проекта
└── requirements.txt           # Зависимости Python
```
# Запуск

## 1. Клонировать репозиторий

```bash
git clone https://github.com/zllataq/Integration_of_MongoDB_and_Graph_Data_Models.git
cd Integration_of_MongoDB_and_Graph_Data_Models
```
## 2. Создать и активировать виртуальное окружение

python3 -m venv venv
source venv/bin/activate

## 3. Установить зависимости

pip install -r requirements.txt

## 4. Настроить подключение к MongoDB

Создать файл .env:

echo "MONGO_URI=mongodb://localhost:27017/" > .env
echo "DATABASE_NAME=practice_graph" >> .env
Запустить MongoDB:

brew services start mongodb-community@8.0

## 5. Загрузить данные в MongoDB

python src/load_data.py

## 6. Выполнить запросы

python src/queries.py

## 7. Запустить тестирование производительности

python src/p_test.py

## 8. Визуализировать граф

python src/visualize.py