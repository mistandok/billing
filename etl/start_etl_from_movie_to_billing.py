"""Модуль отвечает за старт ETL процесса."""
import contextlib
from datetime import timedelta
from time import sleep

import psycopg2
from psycopg2.extras import DictCursor
from config.settings import redis_settings, movies_db_settings, billing_db_settings, settings
from etl.services.process.processes import ETLProcess
from etl.services.process.utils import get_movie_to_billing_etl_process_parameters
from services.decorators.resiliency import backoff
from services.context_managers.managers import redis_context


@backoff()
def main():
    """Основная функция, стартующая ETL-процессы."""
    connect = backoff()(psycopg2.connect)

    with (
        redis_context(redis_settings.host, redis_settings.port) as redis,
        contextlib.closing(connect(**movies_db_settings.dsl(), cursor_factory=DictCursor)) as movies_db,
        contextlib.closing(connect(**billing_db_settings.dsl(), cursor_factory=DictCursor)) as billing_db,
    ):
        process_parameters = get_movie_to_billing_etl_process_parameters(redis, movies_db, billing_db)
        while True:
            with ETLProcess(process_parameters) as process:
                process.start()

            sleep(timedelta(seconds=settings.time_to_restart_process).total_seconds())


if __name__ == '__main__':
    main()
