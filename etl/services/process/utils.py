"""Различные утилиты для ETL-процессов."""
import psycopg2

from etl.config.settings import QueryType, ETLProcessType, settings
from etl.services.process.extractors.adapters import MoviesToBillingAdapter
from etl.services.process.extractors.extractors import PostgresExtractor
from etl.services.process.loaders.loaders import PostgresLoader
from etl.services.process.processes import ETLProcessParameters
from etl.services.process.queries.queries import ETLQueryFactory
from etl.services.process.validators.pydantic_models import BillingMovie
from etl.services.storages.utils import get_backoff_key_value_storage


def get_movie_to_billing_etl_process_parameters(
        state_storage_client,
        movies_db: psycopg2,
        billing_db: psycopg2,
) -> ETLProcessParameters:
    """
    Функция получает параметры для процесса по перегонке данных из movie-admin в billing.

    Args:
        state_storage_client: клиент хранилища состояний.
        movies_db: соединение с базой movie
        billing_db: соединение с базой billing

    Returns:
        ETLProcessParameters
    """
    state_storage = get_backoff_key_value_storage(state_storage_client)
    select_query = ETLQueryFactory.query_by_type(
        QueryType.MOVIE_FILMWORK_SELECT,
        process_type=ETLProcessType.MOVIE_FILMWORK,
        state_storage=state_storage,
    )
    extractor = MoviesToBillingAdapter(PostgresExtractor(
        connection=movies_db,
        query=select_query,
        buffer_size=settings.db_buffer_size,
    ))
    loader = PostgresLoader(
        client=billing_db,
        target_model=BillingMovie,
        target_table_name='billing.filmwork',
        conflict_fields=['id'],
    )
    return ETLProcessParameters(
        process_type=ETLProcessType.MOVIE_FILMWORK,
        state_storage=state_storage,
        extractor=extractor,
        loader=loader,
    )
