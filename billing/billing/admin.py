from django.contrib import admin
from .models import Consumer, Payment, Subscribe, Filmwork, FilmworkSubscribe


# Register your models here.
@admin.register(Consumer)
class ConsumerAdmin(admin.ModelAdmin):
    pass


# @admin.register(Subscription)
# class SubscriptionAdmin(admin.ModelAdmin):
#     pass


class SubscribeFilmworkInline(admin.TabularInline):
    model = FilmworkSubscribe
    autocomplete_fields = ('subscribe',)


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
