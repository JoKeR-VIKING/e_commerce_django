from store.models import Product

class Cart():
    def add(self, product, product_qty):
        product_id = str(product.id)

        if product_id in self.cart:
            self.total -= float(product.price * self.cart[product_id]['qty'])
            self.cart[product_id]['qty'] = product_qty
            self.total += float(product.price * product_qty)
        else:
            self.cart[product_id] = {'price': str(product.price), 'qty': product_qty}
            self.total += float(product.price * product_qty)

        self.session['total'] = self.total
        self.session['cart'] = self.cart

    def delete(self, product):
        product_id = str(product.id)

        if product_id in self.cart:
            self.total -= float(product.price * self.cart[product_id]['qty'])
            del self.cart[product_id]

        self.session['total'] = self.total
        self.session['cart'] = self.cart

    def update(self, product, product_qty):
        product_id = str(product.id)

        if product_id in self.cart:
            self.total -= float(product.price * self.cart[product_id]['qty'])
            self.cart[product_id]['qty'] = product_qty
            self.total += float(product.price * product_qty)

        self.session['total'] = self.total
        self.session['cart'] = self.cart

    def __len__(self):
        return sum(item['qty'] for item in self.cart.values())

    def __iter__(self):
        all_products_ids = list(self.cart.keys())
        products = Product.objects.filter(id__in=all_products_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            if type(item) == float:
                continue

            item['price'] = float(item['price'])
            item['total'] = item['price'] * item['qty']
            yield item

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        total = self.session.get('total')

        if 'cart' not in request.session:
            cart = self.session['cart'] = {}
            total = self.session['total'] = 0.0

        self.cart = cart
        self.total = total