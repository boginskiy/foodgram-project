# **Продуктовый помощник «Foodgram»**

![example workflow](https://github.com/boginskiy/foodgram-project-react/actions/workflows/main.yml/badge.svg?event=push)

### **Описание проекта**
На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

### **Технологии**
Python, Django Rest Framework, PostgreSQL, gunicorn, nginx, Docker

### **Шаблон наполнения env-файла**
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=пароль для подключения к БД
DB_HOST=db
DB_PORT=5432
SECRET_KEY = 'ключ django проекта. файл settings.py'
```

### **Запуск проекта на Docker-Compose**
* _Перед запуском у вас должен быть установлен Docker, Docker-Compose_

Запуск файла __docker-compose.yml__

```
sudo docker compose up -d
```

Миграции
```
sudo docker compose exec <name_web> python manage.py migrate
```

Создание суперпользователя
```
sudo docker compose exec <name_web> python manage.py createsuperuser
```

Статика
```
sudo docker compose exec <name_web> python manage.py collectstatic --no-input
```

Загрузка данных в БД
```
sudo docker-compose exec <name_web> python manage.py loaddata <dump.json>
```

### **Запускаем проект в dev режиме на OC Linux**
Клонировать репозиторий с GitHub
```
git clone git@github.com:boginskiy/foodgram-project-react.git
```

Установить виртуальное окружение venv
```
python3 -m venv venv
```

Aктивировать виртуальное окружение venv
```
source venv/bin/activate
```

Обновить менеджер пакетов pip
```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt
```
pip install -r requirements.txt
```

Выполнить миграции
```
python3 manage.py migrate
```

Создать суперпользователя
```
python3 manage.py createsuperuser
```

Запустить проект
```
python3 manage.py runserver
```

### **Примеры запросов API**
#### **Запросы для Пользователей (users)**

Получить спискок пользователей (GET): `http://127.0.0.1:8000/api/v1/users/`

* _При запросах доступны параметры:_
_page - номер страницы (тип integer);_
_limit - количество объектов на странице (тип integer);_
* _Допустимы анонимные запросы от пользователей_
---

###### Запрос к users
Регистрация пользователя (POST): `http://127.0.0.1:8000/api/users/`

```
    {
        "email": "string",
        "username": "string",
        "first_name": "string",
        "last_name": "string",
        "password": "string"
    }
```

* _email - адрес электронной почты_
* _username - уникальный юзернейм_
* _first_name - имя_
* _last_name - фамилия_
* _password - пароль_
---

###### Запрос к users
Получить профиль пользователя (GET): `http://127.0.0.1:8000/api/users/{users_id}/`

* _{users_id} - id пользователя_
* _Допустимы анонимные запросы от пользователей_
---

###### Запрос к users
Получить текущего пользователя (GET): `http://127.0.0.1:8000/api/users/me/`

* _Доступно авторизованному пользователю_
---

###### Запрос к users
Изменение пароля текущего пользователя (POST): `http://127.0.0.1:8000/api/users/set_password/`

```
    {
        "new_password": "string",
        "current_password": "string",
    }

```
* _new_password - новый пароль_
* _current_password - старый пароль_
* _Изменить пароль может только текущий пользователь_
---

#### **Запросы для токена авторизации (auth/token)**

Получить спискок пользователей (POST): `http://127.0.0.1:8000/api/auth/token/login/`

```
    {
        "password": "string",
        "email": "string",
    }

```

* _Токен используется для авторизации по емейлу и паролю, чтобы далее использовать токен при запросах._
---

###### Запрос к auth/token
Удаление токена (POST): `http://127.0.0.1:8000/api/auth/token/logout/`

* _Доступно авторизованному пользователю_
---

#### **Запросы для тегов (tags)**
Получение списка тегов (GET): `http://127.0.0.1:8000/api/tags/`

* _Допустимы анонимные запросы от пользователей_
---

###### Запрос к tags
Получение тега (GET): `http://127.0.0.1:8000/api/tags/{tags_id}`

* _{tags_id} - id тега_
* _Допустимы анонимные запросы от пользователей_
---

#### **Запросы по рецептам (recipes)**

Получение списка рецептов (GET): `http://127.0.0.1:8000/api/recipes/`

* _При запросах доступны параметры:_
_page - номер страницы (тип integer);_
_limit - количество объектов на странице (тип integer);_
_is_favorited - показывать только рецепты, находящиеся в списке избранного (Enum: 0 1);_
_is_in_shopping_cart - показывать только рецепты, находящиеся в списке покупок (Enum: 0 1);_
_author - показывать рецепты только автора с указанным id (тип integer);_
_tags - Example: tags=lunch&tags=breakfast. Показывать рецепты только с указанными тегами (по slug)_
* _Допустимы анонимные запросы от пользователей_
---

###### Запрос к recipes
Создание рецепта (POST): `http://127.0.0.1:8000/api/recipes/`

```
    {
        "ingredients": [
            {
                "id": "integer",
                "amount": "integer"
            },
        ]
        "tags": "array of integers",
        "image": "string <binary>",
        "name": "string",
        "text": "string",
        "cooking_time": "integer"
    }
```

* _ingredients - список ингредиентов_
_id - уникальный id (тип integer), amount - количество в рецепте (тип integer);_
* _tags - cписок id тегов (тип integer);_
* _image - картинка, закодированная в Base64_
* _name - (тип string)_
* _text - описание_
* _cooking_time - время приготовления (в минутах)_
* _Доступно только авторизованному пользователю_
---

###### Запрос к recipes
Получение рецепта по id (GET): `http://127.0.0.1:8000/api/recipes/{recipes_id}/`

* _{recipes_id} - уникальный идентификатор этого рецепта_
* _Допустимы анонимные запросы от пользователей_
---

###### Запрос к recipes
Обновление рецепта по id (PUTCH): `http://127.0.0.1:8000/api/recipes/{recipes_id}/`

```
    {
        "ingredients": [
            {
                "id": "integer",
                "amount": "integer"
            },
        ]
        "tags": "array of integers",
        "image": "string <binary>",
        "name": "string",
        "text": "string",
        "cooking_time": "integer"
    }
```

* _{recipes_id} - уникальный идентификатор этого рецепта_
* _ingredients - список ингредиентов_
_id - уникальный id (тип integer), amount - количество в рецепте (тип integer);_
* _tags - cписок id тегов (тип integer);_
* _image - картинка, закодированная в Base64_
* _name - (тип string)_
* _text - описание_
* _cooking_time - время приготовления (в минутах)_
* _Доступно только автору данного рецепта_
---

###### Запрос к recipes
Удаление рецепта по id (DELETE): `http://127.0.0.1:8000/api/recipes/{recipes_id}/`

* _{recipes_id} - уникальный идентификатор этого рецепта_
* _Доступно только автору данного рецепта_
---

#### **Запросы к списка покупок (shopping_cart):**

Скачать список покупок. (GET): `http://127.0.0.1:8000/api/recipes/download_shopping_cart/`

* _Доступно только авторизованным пользователям_
---

###### Запрос к shopping_cart
Добавить рецепт в список покупок. (POST): `http://127.0.0.1:8000/api/recipes/{recipes_id}/shopping_cart/`

* _{recipes_id} - уникальный идентификатор этого рецепта._
* _Доступно только авторизованным пользователям_
---

###### Запрос к shopping_cart
Удалить рецепт из списка покупок по id. (DELETE): `http://127.0.0.1:8000/api/recipes/{recipes_id}/shopping_cart/`

* _{recipes_id} - уникальный идентификатор этого рецепта._
* _Доступно только авторизованным пользователям_
---

#### **Запросы к избранным рецептам (favorite):**

Добавить рецепт в избранное. (POST): `http://127.0.0.1:8000/api/recipes/{recipes_id}/favorite/`

* _{recipes_id} - уникальный идентификатор рецепта._
* _Доступно только авторизованным пользователям_
---

###### Запрос к favorite
Удалить рецепт из избранного (DELETE): `http://127.0.0.1:8000/api/recipes/{recipes_id}/favorite/`

* _{recipes_id} - уникальный идентификатор рецепта._
* _Доступно только авторизованным пользователям_
---

#### **Запросы к подпискам пользователя (subscriptions):**

Мои подписки (GET): `http://127.0.0.1:8000/api/users/subscriptions/`

* _Возвращает пользователей, на которых подписан текущий пользователь. В выдачу добавляются рецепты_
* _При запросах доступны параметры:_
_page - номер страницы (тип integer);_
_limit - количество объектов на странице (тип integer);_
_recipes_limit - количество объектов внутри поля recipes (тип integer);_
* _Доступно только авторизованным пользователям_
---

###### Запрос к subscriptions
Подписаться на пользователя (POST): `http://127.0.0.1:8000/api/users/{users_id}/subscribe/`

* _При запросах доступны параметры:_
_recipes_limit - количество объектов внутри поля recipes (тип integer);_
* _{users_id} - уникальный идентификатор пользователя._
* _Доступно только авторизованным пользователям_
---

###### Запрос к subscriptions
Отписаться от пользователя (DELETE): `http://127.0.0.1:8000/api/users/{users_id}/subscribe/`

* _{users_id} - уникальный идентификатор пользователя._
* _Доступно только авторизованным пользователям_
---

#### **Запросы к ингредиентам (ingredients):**

Список ингредиентов (GET): `http://127.0.0.1:8000/api/ingredients/`

* _При запросах доступны параметры:_
_name - Поиск по частичному вхождению в начале названия ингредиента. (тип string);_
* _Допустимы анонимные запросы от пользователей_
---

###### Запрос к ingredients
Получение ингредиента (GET): `http://127.0.0.1:8000/api/ingredients/{ingredients_id}/`

* _{ingredients_id} - уникальный идентификатор ингредиента._
* _Допустимы анонимные запросы от пользователей_
---

### **Автор**
[Богинский Дмитрий](https://github.com/boginskiy) - python разработчик
