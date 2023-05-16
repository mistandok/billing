"""Модуль содержит различные кастомные ошибки."""


class MissBearerAuthorization(Exception):
    """Исключение выбрасывается при некорректной авторизации по токену."""


class MissTokenUserData(Exception):
    """Ислючение выбрасывается, при важных данных о пользователе."""


class MissTokenPayloadAttribute(Exception):
    """
    Исключение выбрасывается, при использовании декоратора на аутентификацию через bearer auth при отсутствии
    необходимого атрибута.
    """


class MissPaymentSystemRealisation(Exception):
    """Отсутствует реализация для платежной системы."""