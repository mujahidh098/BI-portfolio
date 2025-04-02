import random
import datetime

# Creating random data for my orders and order menu items tables

def generate_orders(num_orders=1000, start_id=9711):
    statuses = ['COMPLETED', 'ABANDONED', 'REFUNDED', 'VOIDED']  #Order statuses
    channels = ['COUNTER', 'CALL_IN'] #Different channels
    channel_groups = ['IN_STORE', '3RD_PARTY', 'CALL_ORDER'] #Different channel groups
    service_types = ['TAKE_AWAY', 'DINE_IN'] #Different service types
    stores = list(range(1, 6))

    orders = []
    start_date = datetime.date(2024, 1, 1)
    end_date = datetime.date(2024, 3, 31)

    for i in range(num_orders):
        order_id = start_id + i
        order_number = order_id * 10
        status = random.choice(statuses)
        subtotal = round(random.uniform(50, 500), 2)
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


def generate_order_menu_items(num_items=3000, start_id=20753):
    menu_item_ids = list(range(1, 51))  # Assuming 50 menu items
    category_ids = list(range(1, 6))    # Assuming 5 categories

    order_menu_items = []
    for i in range(num_items):
        item_id = start_id + i
        order_id = random.randint(9711, 9711 + 999)  # Orders generated in previous function
        menu_item_id = random.choice(menu_item_ids)
        total = round(random.uniform(5, 100), 2)
        effective_tax = round(random.uniform(0, 20), 2)
        category_id = random.choice(category_ids)

        item = f"({item_id}, NOW(), NOW(), {order_id}, {menu_item_id}, {total}, NULL, {effective_tax}, {category_id})"
        order_menu_items.append(item)

    return ",\n".join(order_menu_items)


print("INSERT INTO Orders VALUES\n" + generate_orders() + ";")
print("INSERT INTO OrderMenuItems VALUES\n" + generate_order_menu_items() + ";")