import datetime

bank_accounts = {
    1001: {
        "first_name": "Alice",
        "last_name": "Smith",
        "id_number": "123456789",
        "balance": 2500.50,
        "transactions_to_execute": [
            ("2024-08-17 14:00:00", 1001, 1002, 300), ("2024-08-17 15:00:00", 1001, 1003, 200)],
        "transaction_history": [
            ("2024-08-15 09:00:00", 1001, 1002, 500, "2024-08-15 09:30:00")]
    },
    1002: {
        "first_name": "Bob",
        "last_name": "Johnson",
        "id_number": "987654321",
        "balance": 3900.75,
        "transactions_to_execute": [],
        "transaction_history": []
    },
    1003: {
        "first_name": "Bob2",
        "last_name": "Johnson2",
        "id_number": "987654320",
        "balance": 3100.75,
        "transactions_to_execute": [],
        "transaction_history": []
    }
}


def create_trx(source_account_no: int, destination_account_no: int, amount: int) -> None:
    """
    Create a transaction tuple with the current timestamp, source, destination, and amount,
    then append it to the source account's 'transactions_to_execute' list

    arg:
    - source_account_no: int - The source bank account number.
    - destination_account_no: int - The destination bank account number.
    - amount: int - The amount to transfer.

    Returns:
    - None
    """
    source_account = bank_accounts.get(source_account_no)
    transactions_to_execute = source_account.get("transactions_to_execute")
    trx_tuple = (str(datetime.datetime.now()), source_account_no, destination_account_no, amount)
    transactions_to_execute.append(trx_tuple)


def perform_trx(account_no: int) -> None:
    """
    Processes all pending transactions for the account, transfers funds, logs them in the history, and clears pending transactions.

    arg:
    - account_no: int - The account number to process transactions for.

    Returns:
    - None
    """
    source_account = bank_accounts.get(account_no)
    transactions_to_execute = source_account.get("transactions_to_execute")
    for trx in transactions_to_execute:
        dest_account_no = trx[2]
        amount = trx[3]
        dest_account = bank_accounts.get(dest_account_no)
        dest_account["balance"] += amount
        source_account["balance"] -= amount
        source_account["transaction_history"].append(trx + (str(datetime.datetime.now()),))

    transactions_to_execute.clear()


def add_trx() -> None:
    """
    Prompt the user to input a source account, destination account, and transfer amount.
    Validate input and add the transaction to the respective account if valid.

    Returns:
    - None
    """
    while True:
        try:
            source_account_no = int(input("What's the source account? "))
            if bank_accounts.get(source_account_no) is None:
                print(f'Account {source_account_no} does not exist.')
                continue
            destination_account_no = int(input("What's the destination account? "))
            if bank_accounts.get(destination_account_no) is None:
                print(f'Account {destination_account_no} does not exist.')
                continue
            amount = int(input("What's the amount? "))
            if amount <= 50:
                print("Amount must be at least 50.")
                continue

            create_trx(source_account_no, destination_account_no, amount)
            print("Transaction added successfully.")
            break

        except Exception as e:
            print(f'Wrong data... ---{e}---')


def execute_trx() -> None:
    """
    Execute all pending transactions for a given account and display account details and transaction history.

    Returns:
    - None
    """
    while True:
        try:
            account_no = int(input("Please enter your account number: "))
            if bank_accounts.get(account_no) is None:
                print(f"Account number {account_no} doesn't exist. Try again.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid account number.")
    perform_trx(account_no)
    account_details = bank_accounts[account_no]
    print(f"Account Details for {account_no}:")
    print(f"Name: {account_details['first_name']} {account_details['last_name']}")
    print(f"Balance: {account_details['balance']}")
    print("Transaction History:")
    for trx in account_details['transaction_history']:
        print(trx)


def reports() -> None:
    """
    Generate and display a report of all bank accounts, transaction history, and accounts with negative balances.

    Returns:
    - None
    """
    all_bank_accounts = bank_accounts.keys()
    print("All Bank Account Numbers: ", list(all_bank_accounts))

    account_no = int(input("what is the the desired account number: "))
    if bank_accounts.get(account_no) is None:
        print("desired Bank account does not exist!")
    else:
        print("account details:")
        print(bank_accounts.get(account_no))

    id_number = input("Enter your ID number: ")
    account_found = None
    for account_no, details in bank_accounts.items():
        if details["id_number"] == id_number:
            account_found = details
            break

    if account_found:
        print("Account found for this ID number:")
        print(account_found)
    else:
        print("No bank account with this ID number!")

    first_name = input("Enter your first name: ").lower()
    account_found = None

    for account_no, details in bank_accounts.items():
        if first_name in details["first_name"].lower():
            account_found = details
            break

    if account_found:
        print("Account found for this name:")
        print(account_found)
    else:
        print("No bank account found with this name!")

    sorted_accounts = sorted(bank_accounts.items(), key=lambda item: item[1]['balance'])
    for account_no, details in sorted_accounts:
        print(f"Account Number: {account_no}, Balance: {details['balance']}")

    all_transactions = []
    for account_no2, details2 in bank_accounts.items():
        all_transactions.extend(details2['transaction_history'])

    def parse_datetime(date_str):
        try:
            return datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            return datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')

    all_transactions.sort(key=lambda trx: parse_datetime(trx[0]))

    for trx1 in all_transactions:
        print(
            f"Transaction Time: {trx1[0]}, Source Account: {trx1[1]}, Destination Account: {trx1[2]}, Amount: {trx1[3]}, Executed At: {trx1[4]}")

    all_transactions = []
    for account_no3, details3 in bank_accounts.items():
        all_transactions.extend(details3['transaction_history'])

    today = datetime.datetime.now().date()
    todays_transactions = [
        trx for trx in all_transactions
        if datetime.datetime.strptime(trx[0], '%Y-%m-%d %H:%M:%S').date() == today
    ]
    for trx in todays_transactions:
        print(
            f"Transaction Time: {trx[0]}, Source Account: {trx[1]}, Destination Account: {trx[2]}, Amount: {trx[3]}, Executed At: {trx[4]}")

    for account_no, details in bank_accounts.items():
        if details["balance"] < 0:
            print(
                f"Account Number: {account_no}, Name: {details['first_name']} {details['last_name']}, Balance: {details['balance']}")

    total = 0
    for account_no, details in bank_accounts.items():
        total += details["balance"]
    print(total)


def get_by_name(bank_accounts2, first_name: str):
    """
    Search for bank accounts by the first name (case-insensitive) and return matching accounts.

    arg:
    - bank_accounts2: dict - The dictionary containing bank accounts data.
    - first_name: str - The first name to search for.

    Returns:
    - matching_accounts: dict - A dictionary of accounts with matching first names.
    """
    first_name_lower = first_name.lower()
    matching_accounts = {}

    for account_no, details in bank_accounts2.items():
        if first_name_lower in details["first_name"].lower():
            matching_accounts[account_no] = details

    return matching_accounts


def show_main_menu() -> None:
    """
    Display the main menu for bank operations: create, execute transactions, generate reports, or exit.

    Returns:
    - None
    """
    while True:
        print('1. Create trx')
        print('2. Execute trx')
        print('3. reports')
        print('4. exit')
        choice = input("what's your choice?")
        if choice == "4":
            break
        match choice:
            case "1":
                add_trx()
            case "2":
                execute_trx()
            case "3":
                reports()
            case _:
                print("wrong choice .... try again")
