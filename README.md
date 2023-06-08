# Приложение «Магазин "Megano"»

### Установка:
1. Скачать репозиторий
2. Установить виртуальную среду `python -m venv <название>`
3. Установить зависимости: `pip install -r requirements.txt`
4. Прописать в `.env` логин и пароль административной панели (согласно `.env.template`)
5. Создать миграции: `python manage.py makemigrations`
6. Применить миграции: `python manage.py migrate --run-syncdb`
7. Запустить сервер: `python manage.py runserver`
8. Запустить команду создания суперпользователя из папки проекта `___shop___`: `python manage.py createadmin`
9. Запустить команду импорта фикстур из папки проекта `___shop___`: `python manage.py loaddata app_import/fixtures/main_data.json`

### Основные библиотеки:
* [Django == 4.1.4](https://docs.djangoproject.com/en/4.1/) - основной фреймворк
* [loguru == 0.6.0](https://github.com/Delgan/loguru) - логирование
* [python-dotenv == 0.21.0](https://pypi.org/project/python-dotenv/) - переменные среды
* [django-import-export == 3.0.2](https://django-import-export.readthedocs.io/en/latest/getting_started.html) - импорт/экспорт
* [django-mptt == 0.14.0](https://django-mptt.readthedocs.io/en/latest/overview.html) - это метод хранения иерархических данных в базе данных
* [Pillow == 9.3.0](https://pypi.org/project/Pillow/) - библиотека для работы с полями изображений/файлов в Django
* [django-rosetta == 0.9.8](https://django-rosetta.readthedocs.io/) - библиотека для работы с файлами перевода
* [django-filter == 22.1](https://django-filter.readthedocs.io/en/stable/index.html) - библиотека для работы с пользовательскими запросами
* [django-property-filter == 1.1.2](https://pypi.org/project/django-property-filter/) - работа с фильтрами
* [django-bootstrap-modal-forms == 2.2.0](https://pypi.org/project/django-bootstrap-modal-forms/) - работа с модальными формами
* [django-widget-tweaks == 1.4.12](https://pypi.org/project/django-widget-tweaks/) - рендеринг полей формы в шаблонах

### Структура Сайта
* `+` Главная страница.
* `н/т` Каталог с блоком «Популярные товары», фильтром, сортировкой, скидками.
* `+` Сам каталог товаров.
* `н/т` Сравнение.
* `+` Детальная страница товара с отзывами
  * `н/т` и сравнением цен продавцов.
* `н/т` Страница «О продавце».
* `н/т` Страница «О скидках».
* `н/т` Детальная страница скидки.
* `+` Оформление заказа.
* `+` Корзина.
* `+` Оплата.
* `+` Личный кабинет.
* `+` Профиль.
* `+` История просмотров.
* `+` История заказов.
* `+` Административный раздел.
* `+, ap` Просмотр и редактирование товаров.
* `+, ap` Просмотр и редактирование заказов.
* `+, ap` Просмотр и редактирование категорий каталога.
* `+, ap` Просмотр и редактирование скидок.
* `н/т` Страница проведения импорта.
* `+` Роли на сайте