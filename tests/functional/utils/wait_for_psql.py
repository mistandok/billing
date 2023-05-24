"""Модуль проверяет состояине Elasticsearch."""

import sys

import backoff
import psycopg2
from psycopg2 import OperationalError

from settings import BILLING_PG_DSL, AUTH_PG_DSL


@backoff.on_exception(backoff.expo, OperationalError)
def wait_psql(dsl: dict):
    conn = psycopg2.connect(**dsl)
    conn.close()


if __name__ == '__main__':
    print('waiting for AUTH PostgreSQL...', file=sys.stdout)
    wait_psql(AUTH_PG_DSL)
    print('AUTH PostgreSQL was started', file=sys.stdout)

    print('waiting for BILLING PostgreSQL...', file=sys.stdout)
    wait_psql(BILLING_PG_DSL)
    print('BILLING PostgreSQL was started', file=sys.stdout)
