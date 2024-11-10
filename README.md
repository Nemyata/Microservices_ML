# Проект: Автоматизация обработки данных с использованием микросервисов

## Описание проекта

Этот проект включает несколько микросервисов, которые выполняют обработку данных и анализ, используя очереди сообщений для передачи информации между сервисами. Основные шаги задачи включают отправку данных в очередь сообщений, логирование метрик, а также создание графиков распределения ошибок.

Микросервисы взаимодействуют через RabbitMQ, и каждый из них выполняет отдельную функцию:
1. **features.py** — генерирует данные и отправляет их в очередь.
2. **predictor.py** — получает данные, делает предсказания с использованием загруженной модели и отправляет результаты в очередь.
3. **metric.py** — получает данные, рассчитывает метрики и сохраняет их в CSV-файл.
4. **plot.py** — строит графики распределения ошибок, используя данные из CSV-файла.

Каждый сервис запускается в контейнере Docker и использует Docker Compose для настройки всех сервисов и их зависимостей.

## Задача

1. **Шаг 1**: В файле `features.py` реализована отправка вектора признаков и ответов с уникальными идентификаторами в очередь сообщений. Используется задержка после каждой итерации для отслеживания процесса.

2. **Шаг 2**: В сервисе `predictor.py` осуществляется получение данных, выполнение предсказания с помощью предварительно загруженной модели и отправка результатов в очередь.

3. **Шаг 3**: В сервисе `metric.py` добавляется логирование метрик в CSV-файл. Расчёт абсолютной ошибки осуществляется для каждого сообщения, и результаты сохраняются в файл `metric_log.csv`.

4. **Шаг 4**: Сервис `plot.py` читает данные из `metric_log.csv`, строит гистограмму распределения ошибок и сохраняет её в файл `logs/error_distribution.png`.

## Структура проекта

```plaintext
/
├── docker-compose.yml       # Файл для настройки всех сервисов
├── Dockerfile               # Dockerfile для каждого сервиса
├── requirements.txt         # Список зависимостей для каждого сервиса
├── features.py              # Микросервис для отправки данных
├── predictor.py             # Микросервис для получения данных, предсказания и отправки результатов
├── metric.py                # Микросервис для обработки и логирования метрик
├── plot.py                  # Микросервис для построения графиков
├── myfile.pkl               # Моделька в формате .pkl
├── logs/                    # Папка для хранения логов и графиков
│   └── metric_log.csv       # Лог с метриками
│   └── error_distribution.png # График распределения ошибок
└── start.sh                 # Скрипт для запуска всех сервисов
```
## Установка

1. Клонируйте репозиторий на ваш компьютер.

```bash
git clone https://github.com/Nemyata/Microservices_ML.git
cd your-repository-directory
```
2. Убедитесь, что на вашем компьютере установлен Docker и Docker Compose.
3. Установите зависимости для каждого сервиса:
```bash
pip install -r requirements.txt
```
## Запуск проекта

### Сборка и запуск контейнеров с помощью Docker Compose:
```bash
docker-compose up --build
```
Эта команда соберет образы для всех сервисов и запустит их в контейнерах. Все сервисы будут работать в бесконечном цикле, выполняя задачи по отправке данных, логированию метрик и построению графиков.

### Просмотр логов:

Логи для каждого контейнера можно просматривать с помощью команды:
```bash
docker-compose logs -f
```
Это позволит отслеживать активность сервисов в реальном времени.


