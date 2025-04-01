import random
import datetime

def generate_stock_transactions(num_transactions=300, start_id=1220):
    """Generates SQL INSERT value rows for StockTransactions."""

    stock_codes = ['BUN001', 'BEEF001', 'LETT001', 'TOMA001', 'CHEESE001', 'SAUCE001', 'COLA001', 'FRIES001', 'WRAP001', 'ONION001', 'CHICK001', 'BACON001', 'JALA001', 'MAYO001', 'SODA001', 'PICKLE001', 'MUSTARD001', 'ORANGE001', 'RINGS001', 'BOX001']
    source_types = ['DELIVERY_INCREASE', 'ORDER', 'STOCKTAKE_INCREASE', 'WASTE', 'DELIVERY_DECREASE', 'STOCK_RETURN', 'CREDIT_NOTE_DECREASE', 'CREDIT_NOTE_INCREASE', 'REVERSE_TRANSFER_INCREASE', 'REVERSE_TRANSFER_DECREASE', 'REVERSE_WASTE', 'ROUNDING_ADJUSTMENT', 'STORE_SETUP_STOCKTAKE_INCREASE', 'TRANSFER_INCREASE', 'PRODUCTION_INCREASE', 'PRODUCTION_DECREASE', 'STOCKTAKE_DECREASE', 'VOID_ORDER']
    batch_ids = list(range(2200, 2209))  # batch_id range
    unit_type_ids = list(range(1, 5)) # unit_type_id range
    created_by_ids = [1, 2, 10] # ids of users who created the transactions
    stock_item_ids = [100, 125, 150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 425, 450, 475, 500, 525, 550, 575, 600]

    transactions = []
    start_date = datetime.date(2024, 2, 1)
    end_date = datetime.date(2024, 2, 29)

    for i in range(num_transactions):
        id_val = start_id + i
        source_id = 9710 # Example source id
        transaction_cost = round(random.uniform(0.5, 100), 2)
        quantity = round(random.uniform(0.1, 100), 2)
        random_days = random.randint(0, (end_date - start_date).days)
        date_of_capture = start_date + datetime.timedelta(days=random_days, hours=random.randint(0, 23), minutes=random.randint(0, 59), seconds=random.randint(0, 59))
        stock_code = random.choice(stock_codes)
        batch_id = random.choice(batch_ids)
        unit_type_id = random.choice(unit_type_ids)
        created_by = random.choice(created_by_ids)
        effective_tax = round(random.uniform(0, 50), 2)
        unit_cost = round(random.uniform(0, 50), 2)
        source_type = random.choice(source_types)
        stocktake_unit_cost = round(random.uniform(0, 50), 6)

        # Calculate txCost and txQty based on sourceType
        if source_type in ('DELIVERY_INCREASE', 'STORE_SETUP_STOCKTAKE_INCREASE', 'CREDIT_NOTE_INCREASE', 'TRANSFER_INCREASE', 'PRODUCTION_INCREASE', 'STOCKTAKE_INCREASE', 'REVERSE_WASTE', 'REVERSE_TRANSFER_DECREASE', 'VOID_ORDER'):
            tx_cost = round(stocktake_unit_cost * quantity, 3)
            tx_qty = round(quantity, 3)
        elif source_type in ('DELIVERY_DECREASE', 'CREDIT_NOTE_DECREASE', 'TRANSFER_DECREASE', 'PRODUCTION_DECREASE', 'STOCKTAKE_DECREASE', 'WASTE', 'STOCK_RETURN', 'REVERSE_TRANSFER_INCREASE', 'ORDER'):
            tx_cost = round(-(stocktake_unit_cost * quantity), 3)
            tx_qty = round(-quantity, 3)
        else:
            tx_cost = 0
            tx_qty = 0

        tx_unit_cost = round(stocktake_unit_cost, 6)
        stock_item_id = random.choice(stock_item_ids)

        transaction = f"""
({id_val}, {source_id}, {transaction_cost}, {quantity}, '{date_of_capture.strftime('%Y-%m-%d %H:%M:%S')}', NULL, '{date_of_capture.strftime('%Y-%m-%d %H:%M:%S')}', '{stock_code}', {batch_id}, {unit_type_id}, {created_by}, 0, NULL, 0, {effective_tax}, {unit_cost}, '{source_type}', {stocktake_unit_cost}, NULL, {tx_cost}, {tx_qty}, {tx_unit_cost}, NULL, {stock_item_id})"""
        transactions.append(transaction)

    return ",\n".join(transactions)

print(generate_stock_transactions())  