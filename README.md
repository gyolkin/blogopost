# Простой блог на Django
[![Version_of_Python](https://img.shields.io/badge/python-3.10-orange?style=flat&logo=python&logoColor=white)](#)
[![Version_of_Django](https://img.shields.io/badge/django-4.2-green?style=flat&logo=django&logoColor=white)](#)
[![Docker_Compose](https://img.shields.io/badge/docker-compose-blue?style=flat&logo=docker&logoColor=white)](#)
## Описание
«Blogopost» — это сайт, на котором пользователи могут обмениваться информацией, публикуя различные статьи. Текст может форматироваться с помощью markdown. Для упрощения работы с сайтом предусмотрены группы, создаваемые администратором и выступающие в качестве категорий. У каждой группы есть своя уникальная ссылка и текстовое описание. В разделе «избранное» отображаются статьи авторов, на которых подписался пользователь. Каждый пользователь может редактировать свой профиль, изменяя описание или аватарку. На сайте есть возможность комментирования записей, редактирования собственных статей. Главная страница кешируется с помощью locmem cache.

## Внешний вид
![Главная страница сайта](https://s144vlx.storage.yandex.net/rdisk/33b50443ed2148c3b91e362d22c727b1847d709c1f2a8ee320666bdadbf6b282/64413c72/k3Tw5lsORVidoeFyRcYqt1FdXhU7-2AvwVWwV17pmhNwHXixbB9b-PDUR9eJh4pJ68SRnhqxGUDoEtIZR_aBTQ==?uid=1425571490&filename=main-page.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng&owner_uid=1425571490&fsize=756382&hid=6d5dd484d3f66790351ba200ab8ea0a8&media_type=image&tknv=v2&etag=4b141f5181e3311f66ddeeaa8e60b95b&rtoken=EcWwn31H6wlN&force_default=yes&ycrid=na-935b6abc72ccf81f6e9e5b79908a3832-downloader17f&ts=5f9c46c928080&s=68475ea44013e78aa1862b2464c6ec33404936639455b49ce29abaf79a58f485&pb=U2FsdGVkX1-rZbltMd-h8TaEBG6CGR3JSOU2JY9Dlkv679RZzkp7u0kJViyQt5ps3p7cqsVYsPENEtPNSQWXqo2_8gCUPrCjrJcsyqcp0rQ)

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
