from django.core.management.base import BaseCommand

from billing.models import Subscribe


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--subscribe_type', required=True)
        parser.add_argument('--description', required=True)
        parser.add_argument('--price', required=True)
        parser.add_argument('--currency', required=True)
        parser.add_argument('--interval', required=True)

        # --- our

        # parser.add_argument('--product_id', required=True) # prod_NvLh9jF7gIPTYJ
        # parser.add_argument('--payment_id', required=True) # price_1N9UzfLMJMPXrLqCr5sFR5tC
        #
        # # --media
        #
        # parser.add_argument('--product_id', required=True) # prod_Nw19IApZUG0frs
        # parser.add_argument('--payment_id', required=True) # price_1NA96yLMJMPXrLqCf1yMayBS

    def handle(self, *args, **options):

        sub_type = Subscribe.objects.get(subscribe_type='US')

        if sub_type.objects.exists():
            return

        sub_type = options['subscribe_type']
        description = options['description']
        price = options['price']
        currency = options['currency']
        interval = options['interval']

        Subscribe.objects.create_superuser(
            sub_type=sub_type,
            description=description,
            price=price,
            currency=currency,
            interval=interval

        )

