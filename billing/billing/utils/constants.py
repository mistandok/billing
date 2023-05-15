"""Модуль константных значений"""

from enum import Enum


class Price(str, Enum):
    """Класс описывает денежный интервал"""
    STANDART = '199-259'
    DELUXE = '399-799'
    ULTIMATE = '1_500-3_200'
