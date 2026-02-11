import stripe
from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY

def create_stripe_product(name):
    """Создает продукт в Stripe."""
    product = stripe.Product.create(name=name)
    return product.id

def create_stripe_price(amount, product_id):
    """Создает цену в Stripe (сумма передается в рублях)."""
    return stripe.Price.create(
        currency="rub",
        unit_amount=int(amount * 100),
        product=product_id,
    )

def create_stripe_session(price_id):
    """Создает сессию оплаты и возвращает объект сессии."""
    return stripe.checkout.Session.create(
        success_url="http://127.0.0.1",
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
    )
