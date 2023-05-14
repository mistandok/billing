import stripe
from django.conf import settings

from billing.models import Consumer, Subscribe

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_customer(consumer: Consumer):
    customer = stripe.Customer.create(email=consumer.email)
    consumer.remote_consumer_id = customer.id
    consumer.save()


def create_product(subscribe: Subscribe):
    product = stripe.Product.create(name=subscribe.get_subscribe_type_display())
    price=stripe.Price.create(
        unit_amount=subscribe.price,
        currency="usd",
        recurring={"interval": "month"},
        product=product.id,
    )
    subscribe.payment_id=price.id
    subscribe.save()

def create_subscribe(consumer: Consumer, subscribe: Subscribe):
    checkout_session = stripe.checkout.Session.create(
        line_items=[
            {
                'price': subscribe.payment_id,
                'quantity': 1,
            },
        ],
        mode='subscription',
        success_url="http://localhost:8000/success",
        cancel_url="http://localhost:8000/cancel",
    )
    return checkout_session.url