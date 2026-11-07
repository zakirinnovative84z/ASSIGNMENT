# Task 15 - Integrated Order Fulfillment System

import json
import unittest


class Product:
    def __init__(self, product_id, name, price, stock):
        if price < 0 or stock < 0:
            raise ValueError("Price and stock cannot be negative")

        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock


class Cart:
    def __init__(self):
        self.items = {}

    def add_product(self, product_id, quantity):
        if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity <= 0:
            raise ValueError("Quantity must be a positive whole number")

        if product_id not in self.items:
            self.items[product_id] = 0

        self.items[product_id] += quantity


class Order:
    def __init__(self, order_id, items, total):
        self.order_id = order_id
        self.items = items
        self.total = total


class Inventory:
    def __init__(self, products):
        self.products = {}

        for product in products:
            if product.product_id in self.products:
                raise ValueError("Duplicate product ID")
            self.products[product.product_id] = product

    @classmethod
    def from_json(cls, path):
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)

        products = []
        for item in data:
            products.append(Product(
                item["product_id"], item["name"],
                item["price"], item["stock"]
            ))

        return cls(products)

    def place_order(self, cart, discount, orders_file="orders.json"):
        if not isinstance(discount, (int, float)) or discount < 0 or discount > 100:
            raise ValueError("Discount must be from 0 to 100")

        total = 0
        order_items = []

        for product_id, quantity in cart.items.items():
            if quantity <= 0:
                raise ValueError("Quantity must be positive")

            if product_id not in self.products:
                raise ValueError("Product does not exist")

            product = self.products[product_id]

            if quantity > product.stock:
                raise ValueError("Not enough stock for " + product.name)

            total += product.price * quantity
            order_items.append({
                "product_id": product_id,
                "quantity": quantity,
                "price": product.price
            })

        total = total - (total * discount / 100)
        # Read old orders. A missing file means there are no saved orders yet.
        try:
            with open(orders_file, "r", encoding="utf-8") as file:
                saved_orders = json.load(file)
        except FileNotFoundError:
            saved_orders = []

        if not isinstance(saved_orders, list):
            raise ValueError("Orders file must contain a list")

        # Make an ID that is not already used.
        order_number = len(saved_orders) + 1
        used_ids = []
        for old_order in saved_orders:
            used_ids.append(old_order["order_id"])
        order_id = "ORDER-" + str(order_number)
        while order_id in used_ids:
            order_number += 1
            order_id = "ORDER-" + str(order_number)

        order = Order(order_id, order_items, total)
        saved_orders.append({
            "order_id": order.order_id,
            "items": order.items,
            "total": order.total
        })

        # Save first. If saving fails, stock has not changed.
        with open(orders_file, "w", encoding="utf-8") as file:
            json.dump(saved_orders, file, indent=4)

        for product_id, quantity in cart.items.items():
            self.products[product_id].stock -= quantity

        return order

class OrderTests(unittest.TestCase):
    def setUp(self):
        self.inventory = Inventory([Product("P1", "Pen", 100, 5)])
        self.cart = Cart()

    def test_successful_order_and_discount(self):
        self.cart.add_product("P1", 2)
        order = self.inventory.place_order(self.cart, 10, "test_orders.json")
        self.assertEqual(order.total, 180)
        self.assertEqual(self.inventory.products["P1"].stock, 3)

    def test_rejects_out_of_stock(self):
        self.cart.add_product("P1", 6)
        with self.assertRaises(ValueError):
            self.inventory.place_order(self.cart, 0, "test_orders.json")
        self.assertEqual(self.inventory.products["P1"].stock, 5)

    def test_rejects_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.cart.add_product("P1", 0)


if __name__ == "__main__":
    unittest.main()