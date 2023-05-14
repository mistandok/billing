"""Модуль содержит шаблоны SQL запросов для PostgreSQL."""

MOVIES_QUERY = """
    SELECT
        film_work.id,
        film_work.title,
        film_work.modified as modified_state
    FROM
        content.film_work film_work
    {where_condition}
    ORDER BY film_work.modified
"""
