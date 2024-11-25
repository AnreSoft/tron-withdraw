# Tron Monitor and Transaction Automation

This script monitors balances and bandwidth usage on the TRON network using the Tronpy library. It supports automatic transfers between a SLAYER wallet and an OWNER wallet based on incoming transactions.

### Features:
- Monitors TRX balance and bandwidth on the SLAYER wallet.
- Automatically transfers funds to the OWNER wallet when specific conditions are met.
- Sends notifications via Telegram for key events (e.g., incoming transactions, successful transfers).
- Supports multiple API keys for interacting with the TRON network.

### Configuration:

Before running the script, update the following configuration settings in the script:

1. **BOT_TOKEN**: Your Telegram bot API token.
2. **LOG_CHAT_ID**: The Telegram chat ID where logs will be sent.
3. **API_KEYS**: List of API keys to interact with the TRON network.
4. **SLAYER**: The wallet address where incoming TRX will be received.
5. **OWNER**: The wallet address where the funds will be transferred.
6. **PRIVATE_KEY**: The private key corresponding to the wallet used for signing transactions. 

   **Important:** If permissions are transferred to the OWNER, **the `PRIVATE_KEY` should be the private key of the OWNER wallet**, not the SLAYER wallet.

7. **COUNT_OF_TRY_TO_WITHDRAW**: Number of attempts for withdrawing funds from the SLAYER wallet.
8. **START_FEE**: Initial transaction fee for the transfer.
9. **TRX_AMOUNT**: The amount of TRX to be transferred.
10. **BW_COST**: The bandwidth cost used for the transaction.

### Running the Script:

To run the script, follow these steps:

1. Install dependencies using pip:
    ```bash
    pip install -r requirements.txt

    ```

2. Set the configuration parameters (mentioned abSove) in the script.

3. Run the script:
    ```bash
    python main.py
    ```

### Telegram Notifications:
The script sends notifications to a specified Telegram chat using the Telegram Bot API. You will receive updates about:
- Incoming transactions.
- Successful transfers.
- Bandwidth usage and updates.

### Important Notes:
- **Private Key**: Ensure that the `PRIVATE_KEY` corresponds to the correct wallet, especially if permissions are transferred to the OWNER wallet. When the SLAYER wallet transfers its permissions to the OWNER, the private key used in the script should belong to the OWNER wallet, not SLAYER.
- **Security**: Keep your `PRIVATE_KEY` and other sensitive information secure. Avoid sharing them or exposing them in public repositories.
