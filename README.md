## YADISK - REST API сервис, который позволяет пользователям загружать и обновлять информацию о файлах и папках.
### Задание для Школы Бэкенд Разработки Яндекс
![example workflow](https://github.com/potapovjakov/Yadisk/actions/workflows/yadisk_workflow.yml/badge.svg)  

## Стек технологий

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)

## Запуск проекта локально из репозитория
- Склонируйте репозиторий `git clone git@github.com:potapovjakov/Yadisk.git`
- Перейдите в папку с проектом `cd Yadisk`
- Установите виртуальное окружение `python -m venv venv `
- Активируйте виртуальное окружение ` . venv/bin/activate`
- Создайте в папке `infra` файл .env `touch ./infra/.env`
- Заполните `.env` действительными для вашей БД переменными:
```python
DB_NAME=YOUR_DB_NAME
POSTGRES_USER=YOUR_POSTGRES_USER
POSTGRES_PASSWORD=YOR_POSTGRES_PASSWORD
DB_HOST=db
DB_PORT='5432'
```
- Обновите pip командой ` python -m pip install --upgrade pip`
- Установите зависимости из файла requirements.txt `pip install -r requirements.txt`
- Удостоверьтесь что на локальной машине запущена база данных PostgreSQL по адресу 127.0.0.1 порт 5432
- Запустите uvicorn `uvicorn main:app --host 0.0.0.0, --port 80`
#### Теперь проект будет доступен для подключения по адресу 127.0.0.1:80
Спецификация REST API лежит в папке `docs` файл `openapi.yaml`

## Запуск проекта на удаленном сервере (Ubuntu)
- Убедитесь что никакое другое ПО не использует 80 порт
- Установите Docker
```bash
sudo apt update && sudo apt upgrade -y && sudo apt install curl -y
sudo curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh && sudo rm get-docker.sh
sudo curl -SL https://github.com/docker/compose/releases/download/v2.6.0/docker-compose-linux-x86_64 -o /usr/bin/docker-compose
sudo chmod +x /usr/bin/docker-compose
```
- Перенесите файл docker-compose.yml из папки `infra` на удаленный сервер:
```bash
scp docker-compose.yml username@server_ip:/home/<username>/
```
- Создайте в рабочей папке файл .env `touch .env`
- Заполните `.env` действительными для БД переменными:
```python
DB_NAME=YOUR_DB_NAME
POSTGRES_USER=YOUR_POSTGRES_USER
POSTGRES_PASSWORD=YOR_POSTGRES_PASSWORD
DB_HOST=db
DB_PORT='5432'
```
- Выполните команду для сборки образа
```bash
sudo docker-compose up -d --build
```
Можно выполнять запросы

Выполнил
[Яков Потапов](https://github.com/potapovjakov)