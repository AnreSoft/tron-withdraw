from tronpy import Tron
from tronpy.providers import HTTPProvider
from tronpy.keys import PrivateKey
import time
import requests
from datetime import datetime
from decimal import Decimal
import logging  # noqa
import builtins

# Configuration Section
BOT_TOKEN = '732...11:AAExcR7HGX...htiWEdoDos'
LOG_CHAT_ID = '-455...8'

API_KEYS = [
    "5ed32...7cd",
    "e7702...8f5",
    "e879...dfd"
]

SLAYER = 'TMW...41Ek'  # Address of the SLAYER wallet
OWNER = 'TNzG...ZYi9'  # Address of the OWNER wallet

PRIVATE_KEY = "a31f...c322c"  # Private key of the OWNER wallet
COUNT_OF_TRY_TO_WITHDRAW = 10  # Number of attempts for fund transfer
START_FEE = 267_000  # Initial transaction fee in SUN

TRX_AMOUNT = 1  # TRX value for transactions
BW_COST = 265  # Bandwidth threshold

TRX_LIMIT_WITHDRAW = 120  # Maximum amount for withdrawal in TRX

# Calculated values
api_function_count = 4
sleep_between_api = round(1 * api_function_count / len(API_KEYS), 7)
print(f'DELAY: {sleep_between_api}')

expiration_time = 24 * 3600 * 1000  # 24 hours in milliseconds
private_key = PrivateKey(bytes.fromhex(PRIVATE_KEY))  # Convert the private key string to bytes
amount = TRX_AMOUNT * 1_000_000  # Convert TRX to SUN (1 TRX = 1,000,000 SUN)
api_requests_count = 0

# Custom print function with timestamps
def custom_print(*args, **kwargs):
    now = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    message = ' '.join(map(str, args))
    builtins.print(f"{now} {message}", **kwargs)

print = custom_print

# Initialize Tron client with an API key
def client_initialize(api_key):
    provider = HTTPProvider(api_key=api_key)
    client = Tron(provider=provider, network='tronex')
    return client

# Function to transfer funds between wallets
def withdraw(client, transaction_value, sender, recipient):
    try:
        txn_builder = client.trx.transfer(sender, recipient, transaction_value)                                                                                                                                                                                                                                                 
        expiration_timestamp = int(time.time() * 1000) + expiration_time
        txn_builder._raw_data['expiration'] = expiration_timestamp
        txn = txn_builder.build().sign(private_key)
        result = txn.broadcast()
        print(f'TRANSACTION COMPLETED: {transaction_value / 1_000_000} TRX {sender} --> {recipient} | {result}')
        return True
    except Exception as e:
        print(f'ERROR DURING TRANSACTION: {e}')
        return False

# Function to monitor and manage wallet balances and bandwidth
def ultimate_checker(client, trx_slayer_balance):
    is_transaction_received = False

    # Check SLAYER wallet balance
    trx_current_balance_slayer = client.get_account_balance(SLAYER)
    print(f'TRX-SLAYER BALANCE: {trx_current_balance_slayer}')

    # If funds are received on the SLAYER wallet
    if trx_current_balance_slayer > trx_slayer_balance:
        is_transaction_received = True
        received_trx_value = trx_current_balance_slayer - Decimal(trx_slayer_balance)
        bot_text = f'💵 INCOMING TRANSACTION: {received_trx_value} TRX to SLAYER-address: {SLAYER}'
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                      data={"chat_id": LOG_CHAT_ID, "text": bot_text})
        print(bot_text)

        # Transfer funds to the OWNER wallet
        for i in range(COUNT_OF_TRY_TO_WITHDRAW):
            bot_text = f'💸 ATTEMPT #{i + 1} TO TRANSFER FUNDS TO OWNER: {OWNER}'
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                          data={"chat_id": LOG_CHAT_ID, "text": bot_text})
            print(bot_text)

            fee = Decimal(START_FEE) + Decimal(i) / Decimal(1000)
            trx_value_for_withdraw = (received_trx_value * Decimal(1_000_000)) - Decimal(fee)
            is_withdraw_done = withdraw(client, int(trx_value_for_withdraw), SLAYER, OWNER)

            if is_withdraw_done:
                withdraw_value = int(trx_value_for_withdraw) / 1_000_000
                fee = int(fee) / 1_000_000
                bot_text = (f'✅ SUCCESSFUL TRANSFER!\n\n'
                            f'📤 Transferred: {withdraw_value} TRX\n'
                            f'🪫 Fee: {fee} TRX\n'
                            f'📬 Recipient: {OWNER}')
                requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                              data={"chat_id": LOG_CHAT_ID, "text": bot_text})
                print(bot_text)
                break
        else:
            bot_text = f'❌ FAILED TO TRANSFER FUNDS!'
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                          data={"chat_id": LOG_CHAT_ID, "text": bot_text})
            print(bot_text)

        trx_slayer_balance = client.get_account_balance(SLAYER)

    # Check bandwidth and maintain minimum
    bandwidth_amount_slayer = client.get_bandwidth(SLAYER)
    print(f"BW-SLAYER: {bandwidth_amount_slayer} BW")
    if BW_COST < bandwidth_amount_slayer:
        is_transfer_to_slayer = withdraw(client, 1, OWNER, SLAYER)
        trx_slayer_balance += 0.000001
        if is_transfer_to_slayer:
            is_transfer_to_owner = withdraw(client, 1, SLAYER, OWNER)
            if is_transfer_to_owner:
                trx_slayer_balance -= 0.000001
                bot_text = f'🔥 Bandwidth successfully reduced!\nBW-SLAYER: {bandwidth_amount_slayer} BW'
                requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                              data={"chat_id": LOG_CHAT_ID, "text": bot_text})
                print(bot_text)
    time.sleep(sleep_between_api)
    return trx_slayer_balance, is_transaction_received

# Main function
def main():
    clients = [client_initialize(api_key) for api_key in API_KEYS]
    trx_slayer_balance = clients[0].get_account_balance(SLAYER)

    bot_text = (f'✅ TRON Monitor started.\n\n'
                f'⛓️ SLAYER-address: {SLAYER}\n'
                f'📬 OWNER-address: {OWNER}\n'
                f'🏁 Starting TRX Balance: {trx_slayer_balance}\n'
                f'📊 API Key Count: {len(API_KEYS)}\n'
                f'⏳ Checker Delay: {sleep_between_api} seconds')
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                  data={"chat_id": LOG_CHAT_ID, "text": bot_text})
    print(bot_text)

    while True:
        for client in clients:
            try:
                trx_slayer_balance, is_transaction_received = ultimate_checker(client, trx_slayer_balance)
                print(f'🏁 Updated TRX Balance: {trx_slayer_balance}')
            except Exception as e:
                print(f'ERROR: {e}')

if __name__ == '__main__':
    main()
