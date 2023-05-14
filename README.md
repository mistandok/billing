<a name="readme-top"></a>

Авторы:
 - [Антон](https://github.com/mistandok)
 - [Михаил](https://github.com/Mikhail-Kushnerev)
 - [Илья](https://github.com/Bexram)
 - [Евгений](https://github.com/ME-progr)

<details>
  <summary>
    <h1>Оглавление</h1>
  </summary>
  <ol>
    <li><a href="#репозитории">Репозитории</a></li>
    <li><a href="#описание">Описание</a></li>
    <li><a href="#запуск">Запуск</a></li>
    <li><a href="#список-доступных-урлов">Список доступных урлов</a></li>
    <li><a href="#использование">Использование</a></li>
  </ol>
</details>

## Репозитории
- [Сервис биллинга](https://github.com/mistandok/graduate_work)

## Описание

Общую архитектуру взаимодействия сервисов можно посмотреть на схеме `----------`, ее можно найти в папке `./architecture`

В данном спринте реализованы:
- сервис [профилей пользоваетлей](https://github.com/mistandok/graduate_work/tree/main/user-profile) для хранения купленных пользователем фильмов
  Подробности в README сервиса
- сервис [биллинга](https://github.com/mistandok/graduate_work/tree/main/billing) для осуществления пользователями платежей


## Запуск

Запуск текущих сервисов осуществляется из директории `/docker_app`

1) Старт проекта:

    ```docker
    docker-compose -f docker-compose.prod.yml down -v
    docker-compose -f docker-compose.prod.yml up -d --build
    docker-compose -f docker-compose.prod.yml exec movie-admin python manage.py loaddata dumpdata.json
    ```
    Настройка кластера для mongodb сервиса user-profile
   - ```docker exec -it mongocfg1 bash -c 'mongosh < /scripts/init-configserver.js'```
   - ```docker exec -it mongors1n1 bash -c 'mongosh < /scripts/init-shard01.js'```
   - ```docker exec -it mongors2n1 bash -c 'mongosh < /scripts/init-shard02.js'```
   - ```docker exec -it mongos1 bash -c 'mongosh < /scripts/init-router.js'```

<p align="right"><a href="#readme-top">вверх</a></p>

## Список доступных урлов

  1) [Swagger](http://127.0.0.1/api/openapi) сервиса [профилей пользоваетлей](https://github.com/mistandok/graduate_work/tree/main/user-profile). Для проверки API можно использовать токен из README сервиса.

<p align="right"><a href="#readme-top">вверх</a></p>

## Использование

<p align="right"><a href="#readme-top">вверх</a></p>
