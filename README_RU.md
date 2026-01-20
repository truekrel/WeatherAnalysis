# WeatherAnalysis
Интеррактивное web-приложение для анализа данных о погоде и климате в столицах различных стран мира 

[English version](README.md)
## Функции
- Интеррактивная визуализация данных о различных параметрах погоды
- Представлены данные для большинства столиц за несколько лет
- Отзывчивый и удобный в использовании интерфейс

## Быстрый старт

### Локальная установка
```bash
# Склонируйте репозиторий github
git clone https://github.com/YourUserName/WeatherAnalysis.git
cd WeatherAnalysis

# Установите зависимости
pip install -r requirements.txt

# Проведите первичную обработку данных
python preprocessData.py

# Запустите приложение
streamlit run app.py
```
Запустите в браузере: http://0.0.0.0:8501

### Локальная сборка в docker
```bash
# Сборка
docker build -t WeatherAnalysis .

# Запуск
docker run -p 8501:8501 WeatherAnalysis
```
## Структура проекта

```
.
├── app.py                  # Основное приложение Streamlit
├── preprocessData.py        # Первичная обработка данных
├── GlobalWeatherRepository.csv    # Начальный набор данных
├── requirements.txt        # Зависимости Python
├── Dockerfile             # Конфигурация Docker
└── .streamlit/
    └── config.toml        # Настройки Streamlit
```
## Технологии

- **Python 3.10+**
- **Streamlit** - Web интерфейс
- **Pandas** - Работа с данными
- **Plotly** - Интерактивные графики

## Лицензия

MIT License
