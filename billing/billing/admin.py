from django.contrib import admin
from .models import Consumer, Payment, Subscribe, Filmwork, FilmworkSubscribe, ConsumerSubscribe


class SubscribeFilmworkInline(admin.TabularInline):
    model = FilmworkSubscribe
    autocomplete_fields = ('subscribe',)


class ConsumerSubscribeInline(admin.TabularInline):
    model = ConsumerSubscribe
    autocomplete_fields = ('subscribe',)


@admin.register(Consumer)
class ConsumerAdmin(admin.ModelAdmin):
    inlines = (ConsumerSubscribeInline,)
    search_fields = ('user_id',)


@admin.register(Payment)
class PaymentsAdmin(admin.ModelAdmin):
    pass


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    search_fields = ('title',)


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (SubscribeFilmworkInline, )
    search_fields = ('title',)
