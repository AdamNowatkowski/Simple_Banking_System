import sqlite3
import random
# Setting up card database
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS card (id INTEGER PRIMARY KEY, number TEXT UNIQUE, pin TEXT, balance INTEGER DEFAULT 0);")
conn.commit()

# Assining input variable
user_input = None


# Menu Account displayed and processed after log in into account
def menu_account(card_id, balance):
    print("""1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit""")

    user_input = int(input())
# 1. Balance
    if user_input == 1:
        print(balance)
        menu_account(card_id, balance)
# 2. Add income
    elif user_input == 2:
        print("Enter income:")
        income = input()
        cur.execute('UPDATE card SET balance = balance + {0} WHERE id = {1};'.format(income, card_id))
        balance += int(income)
        conn.commit()
        print("Income was added")
        menu_account(card_id, balance)
# 3. Do transfer
    elif user_input == 3:
        print("Transfer")
        print("Ender card number:")
        transfering_card = str(input())
        luhn_sum = 0
        counter = 0

        # Verifying Tranfsering Card Number with LUHN Algorythm
        for digit in transfering_card:
            counter += 1
            y = int(digit)
            if counter % 2 != 0:
                y *= 2
                if y > 9:
                    y -= 9
            luhn_sum += y
        if luhn_sum % 10 != 0:
            print("Probably you made a mistake in the card number. Please try again!")
            menu_account(card_id, balance)

        cur.execute('SELECT * FROM card;')
        data_list = cur.fetchall()
        for idz in data_list:
            if card_id == idz[0]:
                balance = idz[3]
        card_number_list = []
        for card_data in data_list:
            card_number_list.append(card_data[1])
        if str(transfering_card) in card_number_list:
            for card_data in data_list:
                if card_data[1] == str(transfering_card):
                    print("Enter how much money you want to transfer:")
                    transfering_amount = int(input())
                    if transfering_amount > balance:
                        print("Not enough money!")
                        menu_account(card_id, balance)
                        break
                    elif transfering_amount <= balance:

                        cur.execute('UPDATE card SET balance = balance - {0} WHERE id = {1};'.format(transfering_amount, card_id))
                        conn.commit()
                        cur.execute('UPDATE card SET balance = balance + {0} WHERE number = {1};'.format(transfering_amount, transfering_card))
                        conn.commit()
                        balance -= int(transfering_amount)
                        print("Succes!")
                        menu_account(card_id, balance)
        else:
            print("Such a card does not exist")
            menu_account(card_id, balance)
# 4. Close account
    elif user_input == 4:
        cur.execute('DELETE FROM card WHERE id = {0};'.format(card_id))
        conn.commit()
        print("The account has been closed!")
        menu()
# 5. Log out
    elif user_input == 5:
        print("You have successfully logged out!")
        menu()
# 0. Exit
    elif user_input == 0:
        print("Bye!")
        exit()


# Banking system first menu
def banking_system():
    if user_input == 1:
        new_card_number = 0
        while len(str(new_card_number)) != 16:
            new_card_number = "400000" + (str(random.randint(0, 99999999)).zfill(9))
            # Verifying Tranfsering Card Number with LUHN Algorythm
            luhn_sum = 0
            counter = 0
            for digit in new_card_number:
                counter += 1
                y = int(digit)
                if counter % 2 != 0:
                    y *= 2
                    if y > 9:
                        y -= 9
                luhn_sum += y
            new_card_number = int(str(new_card_number) + str(10-luhn_sum % 10))

        new_pin_number = 0
        while len(str(new_pin_number)) < 4:
            new_pin_number = int(str(random.randint(0, 9999)).zfill(4))
        cur.execute("INSERT INTO card(number, pin) VALUES({0}, {1})".format(new_card_number, new_pin_number))
        conn.commit()
        print("Your card has been created\nYour card number:\n{0}\nYour card PIN:\n{1}".format(new_card_number, new_pin_number))
        menu()

    elif user_input == 2:
        cur.execute('SELECT * FROM card')
        data_list = cur.fetchall()
        print("Enter your card number:")
        card_input = str(input())
        print("Enter your PIN:")
        pin_input = str(input())
        for card_data in data_list:
            if card_data[1] == card_input and card_data[2] == pin_input:
                print("You have successfully logged in!")
                menu_account(card_data[0], card_data[3])
                break
            else:
                if card_data == data_list[-1]:
                    print("Wrong card number or PIN!")
                    menu()
                else:
                    continue
    elif user_input == 0:
        print("Bye!")


# Setting up program loop
def menu():
    print("""1. Create an account
2. Log into account
0. Exit""")
    try:
        global user_input
        user_input = int(input())
        banking_system()
    except:
        print("Please input value according to the menu")


menu()
