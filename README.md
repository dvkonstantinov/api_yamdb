# api_yamdb
api_yamdb

# Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/dvkonstantinov/api_yamdb.git
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:
```
python3 -m venv env
source env/bin/activate
```

Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

Выполнить миграции:
```
python3 manage.py migrate
```

Запустить проект:
```
python3 manage.py runserver
```

Описание проекта:
```
Проект представляет из себя социальную сеть в которой можно оставлять отзывы на 
фильмы или книги и ставить оценки.
А так же комментировать отзывы.
```

Автор:
```
Мыши Рокеры
```

Технологии которые использовались:
```
-Python
-Django
-rest_framework
-djoser
```
