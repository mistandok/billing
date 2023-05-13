"""Модуль интерфейса админки"""

from django.contrib import admin
from .models import Consumer, Payment, Subscribe, Filmwork, FilmworkSubscribe, ConsumerSubscribe


class SubscribeFilmworkInline(admin.TabularInline):
    """Интерфейс подписок у кинопроизведения в админке"""
    model = FilmworkSubscribe
    autocomplete_fields = ('subscribe',)


class ConsumerSubscribeInline(admin.TabularInline):
    """Интерфейс подписок у покупателя в админке"""
    model = ConsumerSubscribe
    autocomplete_fields = ('subscribe',)


@admin.register(Consumer)
class ConsumerAdmin(admin.ModelAdmin):
    """Интерфейс покупателя в админке"""
    inlines = (ConsumerSubscribeInline,)
    search_fields = ('user_id',)


@admin.register(Payment)
class PaymentsAdmin(admin.ModelAdmin):
    """Интерфейс платежа в админке"""
    pass


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    """Интерфейс подписки в админке"""
    search_fields = ('title',)


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    """Интерфейс кинопроизведения в админке"""
    inlines = (SubscribeFilmworkInline, )
    search_fields = ('title',)
