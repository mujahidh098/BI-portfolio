import random
import datetime

# Creating random data for Orders and OrderMenuItems tables

def generate_orders(order_totals, num_orders=100, start_id=211):
    statuses = ['COMPLETED', 'ABANDONED', 'REFUNDED', 'VOIDED']  # Order statuses
    channels = ['COUNTER', 'CALL_IN']  # Different channels
    channel_groups = ['IN_STORE', '3RD_PARTY', 'CALL_ORDER']  # Different channel groups
    service_types = ['TAKE_AWAY', 'DINE_IN']  # Different service types
    stores = list(range(1, 6))

    orders = []
    start_date = datetime.date(2024, 2, 1)
    end_date = datetime.date(2024, 2, 29)

    for i in range(num_orders):
        order_id = start_id + i
        order_number = order_id * 10
        status = random.choice(statuses)
        subtotal = round(order_totals.get(order_id, random.uniform(50, 500)), 2)
        delivery_fee = round(random.uniform(0, 50), 2)
        discount = round(random.uniform(0, 30), 2)
        total = round(subtotal + delivery_fee - discount, 2)
        tendered = round(total + random.uniform(0, 20), 2)
        change_amt = round(tendered - total, 2)
        tip = round(random.uniform(0, 20), 2)
        driver_tip = round(random.uniform(0, 20), 2)
        outstanding = round(random.uniform(0, 20), 2)
        created_at = start_date + datetime.timedelta(days=random.randint(0, (end_date - start_date).days))
        store_id = random.choice(stores)
        channel = random.choice(channels)
        channel_group = random.choice(channel_groups)
        service_type = random.choice(service_types)

        order = f"({order_id}, '{created_at}', '{created_at}', {order_number}, '{status}', {subtotal}, {delivery_fee}, {discount}, NULL, NULL, {total}, NULL, NULL, {store_id}, NULL, '{channel}', '{channel_group}', '{service_type}', {tendered}, {change_amt}, {tip}, {driver_tip}, {outstanding}, NULL, NULL)"
        orders.append(order)

    return ",\n".join(orders)


def generate_order_menu_items(num_items=200, start_id=753):
    menu_item_prices = {
        1: 68.99,  # Single Beef
        2: 88.99, # Double Beef
        3: 65.99,  # Fried Chicken
        4: 99.99  # Combo Meal
    }
    order_totals = {}
    order_menu_items = []
    start_date = datetime.date(2024, 2, 1)
    end_date = datetime.date(2024, 2, 29)

    for i in range(num_items):
        item_id = start_id + i
        order_id = random.randint(211, 310)
        menu_item_id = random.choice(list(menu_item_prices.keys()))
        price = menu_item_prices[menu_item_id]
        quantity = random.randint(1, 5)
        total = round(price * quantity, 2)
        effective_tax = round(total * 0.15, 2)
        category_id = 1 if menu_item_id <= 3 else 2
        created_at = start_date + datetime.timedelta(days=random.randint(0, (end_date - start_date).days))

        # Track the total for each order
        if order_id in order_totals:
            order_totals[order_id] += total
        else:
            order_totals[order_id] = total

        item = f"({item_id}, '{created_at}', '{created_at}', {order_id}, {menu_item_id}, {total}, NULL, {effective_tax}, {category_id})"
        order_menu_items.append(item)

    return ",\n".join(order_menu_items), order_totals


order_menu_items, order_totals = generate_order_menu_items()
print("INSERT INTO OrderMenuItems VALUES\n" + order_menu_items + ";")
print("INSERT INTO Orders VALUES\n" + generate_orders(order_totals) + ";") 