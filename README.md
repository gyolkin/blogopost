# Простой блог на Django
[![Version_of_Python](https://img.shields.io/badge/python-3.10-orange?style=flat&logo=python&logoColor=white)](#)
[![Version_of_Django](https://img.shields.io/badge/django-4.2-green?style=flat&logo=django&logoColor=white)](#)
[![Docker_Compose](https://img.shields.io/badge/docker-compose-blue?style=flat&logo=docker&logoColor=white)](#)
## Описание
«Blogopost» — это сайт, на котором пользователи могут обмениваться информацией, публикуя различные статьи. Текст может форматироваться с помощью markdown. Для упрощения работы с сайтом предусмотрены группы, создаваемые администратором и выступающие в качестве категорий. У каждой группы есть своя уникальная ссылка и текстовое описание. В разделе «избранное» отображаются статьи авторов, на которых подписался пользователь. Каждый пользователь может редактировать свой профиль, изменяя описание или аватарку. На сайте есть возможность комментирования записей, редактирования собственных статей. Главная страница кешируется с помощью locmem cache.
## Внешний вид
![Главная страница сайта](https://3.downloader.disk.yandex.ru/preview/18c9b85be30fdc29531b8a0f35314db23d39e884b999429deb137dccdc93fed9/inf/sQwkSpxhpTlFEFL8fWMF-V_m0q-OCQw8JeWFt0Q6lx2CmauiVQ0gQ1BGYePEsC1KDVhQABQ1IMBuAnOm3XVZdw%3D%3D?uid=1425571490&filename=main-page.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng&owner_uid=1425571490&tknv=v2&size=1920x897)
Остальные изображения доступны здесь: [Yandex Disk](https://disk.yandex.ru/d/I7yAlevdJAFy4w)
## Технологический стек
- Python
- Django
- Docker
- PostgreSQL
- nginx
## Зависимости
Файл с зависимостями requirements.txt находится в папке *blogopost*. 
## Запуск на локальном компьютере
Помимо стандартного запуска Django-проекта предусмотрена возможность запуска проекта в Docker (с docker-compose). Для этого необходимо создать в папке *infra* файл .env и заполнить его данными по примеру файла .env.example. Далее, находясь в папке *infra*, требуется выполнить следующие команды:
```
docker-compose up -d
```
Проект будет собран в «тихом режиме», после чего необходимо последовательно выполнить следующие команды: 
```
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py collectstatic
```
Можно также сразу создать администратора с помощью команды:
```
docker-compose exec backend python manage.py createsuperuser
```
При успешном запуске проект и администраторская панель буудт доступны здесь:
```
http://localhost
http://localhost/admin
```
