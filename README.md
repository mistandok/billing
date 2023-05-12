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
    <li><a href="#запуск">Запуск</a></li>
  </ol>
</details>

## Запуск

Запуск текущих сервисов осуществляется из директории `/docker_app`

1) Старт проекта:

    ```docker
    docker-compose -f docker-compose.prod.yml down -v
    docker-compose -f docker-compose.prod.yml up -d --build
    ```
    Настройка кластера для mongodb сервиса user-profile
   - ```docker exec -it mongocfg1 bash -c 'mongosh < /scripts/init-configserver.js'```
   - ```docker exec -it mongors1n1 bash -c 'mongosh < /scripts/init-shard01.js'```
   - ```docker exec -it mongors2n1 bash -c 'mongosh < /scripts/init-shard02.js'```
   - ```docker exec -it mongos1 bash -c 'mongosh < /scripts/init-router.js'```

<p align="right"><a href="#readme-top">вверх</a></p>
