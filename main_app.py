import sqlite3
import hashlib
import datetime
import re
from getpass import getpass 
import cv2
import numpy as np
import pandas as pd
from collections import defaultdict
import numpy as np

import os

# Get the current working directory (cwd) of the Jupyter notebook
cwd = os.getcwd()

# Update paths to reference files in the local directory
DB_PATH = os.path.join(cwd, 'user_auth.db')
PRODUCT_DB_PATH = os.path.join(cwd, 'product_information.db')
HEALTH_DB_PATH = os.path.join(cwd, 'health_form.db')
SHOP_DB_PATH = os.path.join(cwd, 'shopping_list.db')
FAV_DB_PATH = os.path.join(cwd, 'fav_list.db')
REC_PRODUCT_PATH = os.path.join(cwd, 'rec_file.csv')

def add_to_shopping_list(username, product, quantity_shop):
    conn = sqlite3.connect(SHOP_DB_PATH)
    cursor = conn.cursor()
    try:
        # Create table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS shopping_list (
            username TEXT,
            id INTEGER,
            barcode_num TEXT PRIMARY KEY,
            product_name TEXT,
            ingredients TEXT,
            energy REAL,
            proteins REAL,
            carbohydrates REAL,
            cholesterol REAL,
            sugars REAL,
            total_fat REAL,
            saturated_fat REAL,
            trans_fat REAL,
            sodium REAL,
            fruits_vegetables_nuts REAL,
            dietary_fibre REAL DEFAULT 0,
            allergens TEXT,
            nutrition_grade TEXT,
            calcium REAL DEFAULT 0,
            iodine REAL DEFAULT 0,
            zinc REAL DEFAULT 0,
            phosphorous REAL DEFAULT 0,
            magnesium REAL DEFAULT 0,
            vitamin_A REAL DEFAULT 0,
            vitamin_B REAL DEFAULT 0,
            vitamin_C REAL DEFAULT 0,
            vitamin_D REAL DEFAULT 0,
            vitamin_E REAL DEFAULT 0,
            vitamin_K REAL DEFAULT 0,
            other TEXT DEFAULT "",
            quantity_shop INT
            )
        ''')
        
        # Ensure quantity_shop is an integer
        quantity_shop = int(quantity_shop)
        
        # Check if the product with the same barcode already exists
        cursor.execute('SELECT quantity_shop FROM shopping_list WHERE barcode_num = ?', (product[1],))
        existing_record = cursor.fetchone()
        
        if existing_record:
            # If barcode exists, update the quantity
            new_quantity = existing_record[0] + quantity_shop
            cursor.execute('UPDATE shopping_list SET quantity_shop = ? WHERE barcode_num = ?', (new_quantity, product[1]))
            print(f'Updated quantity for product "{product[2]}" to {new_quantity}.')
        else:
            # If barcode doesn't exist, insert a new record
            product_data = product + (quantity_shop,)
            cursor.execute('''
                INSERT INTO shopping_list (username, id, barcode_num, product_name, ingredients, energy, proteins, carbohydrates, cholesterol, sugars, total_fat, saturated_fat,
                                          trans_fat, sodium, fruits_vegetables_nuts, dietary_fibre, allergens, nutrition_grade, calcium, iodine, zinc, phosphorous, magnesium, vitamin_A, vitamin_B, vitamin_C, vitamin_D, vitamin_E, vitamin_K, other, quantity_shop)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (username,) + product_data)
            print(f'Product "{product[2]}" added to shopping list with quantity {quantity_shop}.')
        
        conn.commit()
        
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

def add_to_fav_list(username, product, quantity_favourite):
    conn = sqlite3.connect(FAV_DB_PATH)
    cursor = conn.cursor()
    try:
        # Create table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fav_list (
            username TEXT,
            id INTEGER,
            barcode_num TEXT PRIMARY KEY,
            product_name TEXT,
            ingredients TEXT,
            energy REAL,
            proteins REAL,
            carbohydrates REAL,
            cholesterol REAL,
            sugars REAL,
            total_fat REAL,
            saturated_fat REAL,
            trans_fat REAL,
            sodium REAL,
            fruits_vegetables_nuts REAL,
            dietary_fibre REAL DEFAULT 0,
            allergens TEXT,
            nutrition_grade TEXT,
            calcium REAL DEFAULT 0,
            iodine REAL DEFAULT 0,
            zinc REAL DEFAULT 0,
            phosphorous REAL DEFAULT 0,
            magnesium REAL DEFAULT 0,
            vitamin_A REAL DEFAULT 0,
            vitamin_B REAL DEFAULT 0,
            vitamin_C REAL DEFAULT 0,
            vitamin_D REAL DEFAULT 0,
            vitamin_E REAL DEFAULT 0,
            vitamin_K REAL DEFAULT 0,
            other TEXT DEFAULT "",
            quantity_favourite INT
            )
        ''')
        
        # Ensure quantity_favourite is an integer
        quantity_favourite = int(quantity_favourite)
        
        # Check if the product with the same barcode already exists
        cursor.execute('SELECT quantity_favourite FROM fav_list WHERE barcode_num = ?', (product[1],))
        existing_record = cursor.fetchone()
        
        if existing_record:
            # If barcode exists, update the quantity
            new_quantity = existing_record[0] + quantity_favourite
            cursor.execute('UPDATE fav_list SET quantity_favourite = ? WHERE barcode_num = ?', (new_quantity, product[1]))
            print(f'Updated quantity for product "{product[2]}" to {new_quantity}.')
        else:
            # If barcode doesn't exist, insert a new record
            product_data = product + (quantity_favourite,)
            cursor.execute('''
                INSERT INTO fav_list (username, id, barcode_num, product_name, ingredients, energy, proteins, carbohydrates, cholesterol, sugars, total_fat, saturated_fat,
                                          trans_fat, sodium, fruits_vegetables_nuts, dietary_fibre, allergens, nutrition_grade, calcium, iodine, zinc, phosphorous, magnesium, vitamin_A, vitamin_B, vitamin_C, vitamin_D, vitamin_E, vitamin_K, other, quantity_favourite)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (username,) + product_data)
            print(f'Product "{product[2]}" added to fav list with quantity {quantity_favourite}.')
        
        conn.commit()
        
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()


def view_fav_list(username):

    conn = sqlite3.connect(FAV_DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM fav_list WHERE username=?', (username,))
        products = cursor.fetchall()
        if products:
            print("\nFavourite List:")
            for item in products:
                print(f"- Product Name: {item[3]} , Quantity: {item[30]} ")
        else:
            print("Your favourite list is empty.")
    except sqlite3.Error as e:
            print(f"An error occurred: {e}. It might be caused by an invalid column name or unexpected characters.")
    finally:
        conn.close() 


def view_shopping_list(username):
    conn = sqlite3.connect(SHOP_DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM shopping_list WHERE username=?', (username,))
        products = cursor.fetchall()
        if products:
            print("\nShopping List:")
            for item in products:
                print(f"- Product Name: {item[3]} , Quantity: {item[30]} ")
        else:
            print("Your shopping list is empty.")
    except sqlite3.Error as e:
            print(f"An error occurred: {e}. It might be caused by an invalid column name or unexpected characters.")
    finally:
        conn.close()

def delete_from_fav_list(username, product_name_fav, quantity_to_delete_fav):
    conn = sqlite3.connect(FAV_DB_PATH)
    cursor = conn.cursor()
    try:
        # First, check if the product exists by product name
        cursor.execute('''
            SELECT product_name, quantity_favourite 
            FROM fav_list 
            WHERE username = ? AND product_name = ?
        ''', (username, product_name_fav))
        
        product = cursor.fetchone()
        
        if product:
            current_quantity = product[1]  # Get the current quantity (second column is quantity_favourite)
            new_quantity = current_quantity - int(quantity_to_delete_fav)  # Ensure quantity_to_delete_favis an integer
            
            if new_quantity > 0:
                # Update the quantity in the database if the new quantity is greater than zero
                cursor.execute('''
                    UPDATE fav_list 
                    SET quantity_favourite = ? 
                    WHERE username = ? AND product_name = ?
                ''', (new_quantity, username, product_name_fav))  # Use only product_name for the update
                print(f'Updated quantity for product "{product[0]}" to {new_quantity}.')
            else:
                # If new quantity is 0 or less, remove the product from the list
                cursor.execute('''
                    DELETE FROM fav_list 
                    WHERE username = ? AND product_name = ?
                ''', (username, product_name_fav))  # Use only product_name for the deletion
                print(f'Removed product "{product[0]}" from the favourite list.')
                
            conn.commit()
        else:
            print(f'Product "{product_name_fav}" not found in the favourite list.')

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

def delete_from_shopping_list(username, product_name, quantity_to_delete_shop):
    conn = sqlite3.connect(SHOP_DB_PATH)
    cursor = conn.cursor()
    try:
        # First, check if the product exists by product name
        cursor.execute('''
            SELECT product_name, quantity_shop 
            FROM shopping_list 
            WHERE username = ? AND product_name = ?
        ''', (username, product_name))
        
        product = cursor.fetchone()
        
        if product:
            current_quantity = product[1]  # Get the current quantity (second column is quantity_shop)
            new_quantity = current_quantity - int(quantity_to_delete_shop)  # Ensure quantity_to_delete_shop_shop is an integer
            
            if new_quantity > 0:
                # Update the quantity in the database if the new quantity is greater than zero
                cursor.execute('''
                    UPDATE shopping_list 
                    SET quantity_shop = ? 
                    WHERE username = ? AND product_name = ?
                ''', (new_quantity, username, product_name))  # Use only product_name for the update
                print(f'Updated quantity for product "{product[0]}" to {new_quantity}.')
            else:
                # If new quantity is 0 or less, remove the product from the list
                cursor.execute('''
                    DELETE FROM shopping_list 
                    WHERE username = ? AND product_name = ?
                ''', (username, product_name))  # Use only product_name for the deletion
                print(f'Removed product "{product[0]}" from the shopping list.')
                
            conn.commit()
        else:
            print(f'Product "{product_name}" not found in the shopping list.')

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()


def calculate_nutrition_summary_fav():
    conn = sqlite3.connect(FAV_DB_PATH)
    cursor = conn.cursor()
    total_carbohydrates = 0
    total_proteins = 0
    total_sugars = 0
    total_fat = 0
    total_sodium = 0

    try:
        cursor.execute('SELECT carbohydrates, proteins, sugars, total_fat, sodium FROM fav_list')
        products = cursor.fetchall()
        
        for product in products:
            total_carbohydrates += product[0] if product[0] is not None else 0
            total_proteins += product[1] if product[1] is not None else 0
            total_sugars += product[2] if product[2] is not None else 0
            total_fat += product[3] if product[3] is not None else 0
            total_sodium += product[4] if product[4] is not None else 0
        
        print("\nNutrition Summary of Favourite List:")
        print(f"Total Carbohydrates: {total_carbohydrates:.2f} g")
        print(f"Total Proteins: {total_proteins:.2f} g")
        print(f"Total Sugars: {total_sugars:.2f} g")
        print(f"Total Fat: {total_fat:.2f} g")
        print(f"Total Sodium: {total_sodium:.2f} g")
        
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

def calculate_nutrition_summary_shopping():
    conn = sqlite3.connect(SHOP_DB_PATH)
    cursor = conn.cursor()
    total_carbohydrates = 0
    total_proteins = 0
    total_sugars = 0
    total_fat = 0
    total_sodium = 0

    try:
        cursor.execute('SELECT carbohydrates, proteins, sugars, total_fat, sodium FROM shopping_list')
        products = cursor.fetchall()
        
        for product in products:
            total_carbohydrates += product[0] if product[0] is not None else 0
            total_proteins += product[1] if product[1] is not None else 0
            total_sugars += product[2] if product[2] is not None else 0
            total_fat += product[3] if product[3] is not None else 0
            total_sodium += product[4] if product[4] is not None else 0
        
        print("\nNutrition Summary of Shopping List:")
        print(f"Total Carbohydrates: {total_carbohydrates:.2f} g")
        print(f"Total Proteins: {total_proteins:.2f} g")
        print(f"Total Sugars: {total_sugars:.2f} g")
        print(f"Total Fat: {total_fat:.2f} g")
        print(f"Total Sodium: {total_sodium:.2f} g")
        
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

def preprocess_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresholded = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return thresholded

def read_barcodes(frame):
    try:
        barcodes = pyzbar.decode(frame)
        for barcode in barcodes:
            barcode_info = barcode.data.decode('utf-8')
            if barcode_info.isdigit():
                return barcode_info
    except Exception as e:
        print(f"Error decoding barcode: {e}")
    return None

def scan_barcode(username, stream_url=None):
    if stream_url is None:
        # Get user input for the IP address
        ip_address = input("Enter the IP address of your phone (e.g., 192.168.1.100): ")
        stream_url = f'http://{ip_address}:8080/video'

    cap = cv2.VideoCapture(stream_url)
    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return

    print("Scanning barcode... Press 'q' to quit.")
    scanned_barcodes = set()  # Keep track of scanned barcodes to avoid duplicates

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Process the frame and read the barcode
        processed_frame = preprocess_frame(frame)
        barcode = read_barcodes(processed_frame)

        if barcode and barcode not in scanned_barcodes:
            scanned_barcodes.add(barcode)
            print(f"\nBarcode detected: {barcode}")
            display_product_info(username, barcode)  # Pass the barcode directly to display_product_info

        cv2.imshow('Barcode Scanner', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Scanning cancelled by user")
            break

    cap.release()
    cv2.destroyAllWindows()

def get_product_info(barcode):
    # Connect to the SQLite database
    conn = sqlite3.connect(PRODUCT_DB_PATH)
    cursor = conn.cursor()
    try:
        # Query to fetch all columns for the matching barcode
        query = """
        SELECT id, barcode_num, product_name, ingredients, energy, proteins, carbohydrates, cholesterol, sugars, total_fat, saturated_fat,
                                       trans_fat, sodium, fruits_vegetables_nuts, dietary_fibre, allergens, nutrition_grade, calcium, iodine, zinc, phosphorous, magnesium, vitamin_A, vitamin_B, vitamin_C, vitamin_D, vitamin_E, vitamin_K, other
        FROM products
        WHERE barcode_num = ?
        """
        # Execute the query with the scanned barcode
        cursor.execute(query, (barcode,))
        # Fetch the result
        result = cursor.fetchone()
        return result
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the database connection
        conn.close()
    return None

def display_product_info(username, barcode):
    result = get_product_info(barcode)
    if result:
        # Display the product information
        print("\nProduct Information:")
        print(f"ID: {result[0]}")
        print(f"Barcode: {result[1]}")
        print(f"Product Name: {result[2]}")
        print(f"Ingredients: {result[3]}")
        print(f"Energy: {result[4]} kcal")
        print(f"Proteins: {result[5]} g")
        print(f"Carbohydrates: {result[6]} g")
        print(f"Cholesterol: {result[7]} g")
        print(f"Sugars: {result[8]} g")
        print(f"Total Fat: {result[9]} g")
        print(f"Saturated Fat: {result[10]} g")
        print(f"Trans Fat: {result[11]} g")
        print(f"Sodium: {result[12]} g")
        print(f"Fruits/Vegetables/Nuts: {result[13]} g")
        print(f"Dietary fibre: {result[14]} g")
        print(f"Allergens: {result[15]}")
        print(f"Nutrition Grade: {result[16]}")

        # Only display these values if they are not 0
        if result[17] != 0:
            print(f"Calcium: {result[17]} g")
        if result[18] != 0:
            print(f"Iodine: {result[18]} g")
        if result[19] != 0:
            print(f"Zinc: {result[19]} g")
        if result[20] != 0:
            print(f"Phosphorous: {result[20]} g")
        if result[21] != 0:
            print(f"Magnesium: {result[21]} g")
        if result[22] != 0:
            print(f"Vitamin A: {result[22]} g")
        if result[23] != 0:
            print(f"Vitamin B: {result[23]} g")
        if result[24] != 0:
            print(f"Vitamin C: {result[24]} g")
        if result[25] != 0:
            print(f"Vitamin D: {result[25]} g")
        if result[26] != 0:
            print(f"Vitamin E: {result[26]} g")
        if result[27] != 0:
            print(f"Vitamin K: {result[27]} g")
        if result[28]:  # Assuming 'other' is a string and we want to display it if it's not empty
            print(f"Other: {result[28]}")

        # Rest of the function remains the same
        allergens = result[15]  # Assuming this is a list of allergens
        if 'milk' in allergens.lower():
            print("\n⚠️ WARNING: This product contains dairy!")
        if 'wheat' in allergens.lower():
            print("\n⚠️ WARNING: This product contains wheat!")
        if 'soy' in allergens.lower():
            print("\n⚠️ WARNING: This product contains soy!")
        if 'peanut' in allergens.lower():
            print("\n⚠️ WARNING: This product contains peanut!")
        if 'nut' in allergens.lower():
            print("\n⚠️ WARNING: This product contains nuts!")
        if 'sulphite' in allergens.lower():
            print("\n⚠️ WARNING: This product contains sulphite!")

        # Nutritional tags based on specified conditions
        sugars = result[8]
        sodium = result[12]
        energy_kcal = result[4]
        fats = result[9]
        saturated_fat = result[10]
        proteins = result[5]

        if sugars > 22.5:
            print("\n⚠️ WARNING: This product is high in sugar!")
        elif sugars <= 5:
            print("\n🍎 NOTE: This product is low in sugar!")

        if sodium > 0.6:
            print("\n⚠️ WARNING: This product is high in sodium!")
        elif sodium <= 0.1:
            print("\n🥗 NOTE: This product is low in sodium!")

        if energy_kcal > 0:
            protein_energy_percentage = (proteins * 4 / energy_kcal) * 100
            if protein_energy_percentage >= 20:
                print("\n💪 NOTE: This product is high in protein!")

        if fats > 17.5:
            print("\n🍔 WARNING: This product is high in total fat!")
        elif fats < 0.5:
            print("\n🥬 NOTE: This product is fat-free!")
        elif fats < 3:
            print("\n🥗 NOTE: This product is low in fat!")

        if saturated_fat > 5:
            print("\n🥓 WARNING: This product is high in saturated fat!")
        elif saturated_fat < 0.1:
            print("\n🌱 NOTE: This product is free of saturated fat!")
        elif saturated_fat < 1.5:
            print("\n🥑 NOTE: This product is low in saturated fat!")

        # Retrieve the user's health data
        conn = sqlite3.connect(HEALTH_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM health_form WHERE username = ?", (username,))
        user_health_data = cursor.fetchone()
        conn.close()

        if user_health_data:
            # Prepare user health data for score calculation
            user_data = {
                'age': user_health_data[1],
                'height': user_health_data[2],
                'weight': user_health_data[3],
                'diet_type': user_health_data[4],
                'chronic_illnesses': user_health_data[5],
                'dietary_restrictions': user_health_data[6],
                'trigger_ingredients': user_health_data[7],
                'health_goals': user_health_data[8]
            }

            # Prepare product data for score calculation
            product_data = {
                'energy': result[4],
                'proteins': result[5],
                'carbohydrates': result[6],
                'cholesterol': result[7],
                'sugars': result[8],
                'total_fat': result[9],
                'saturated_fat': result[10],
                'trans_fat': result[11],
                'sodium': result[12],
                'dietary_fibre': result[14],
                'allergens': result[15]
            }

            # Calculate the health score
            health_score = calculate_health_score(user_data, product_data)
            print(f"\n🧑‍⚕️ Health Score (for {username}): {health_score}/5")

        # Ask if the user wants to add the product to the shopping list
        add_to_shop_list = input("\nDo you want to add this product to your shopping list? (yes/no): ").strip().lower()
        if add_to_shop_list == 'yes':
            quantity_shop = input("\n Enter quantity of product (int): ")
            add_to_shopping_list(username, result, quantity_shop)  # Pass all fields of the product

        view_shop_list = input("Do you want to view your shopping list? (yes/no): ").strip().lower()
        if view_shop_list == 'yes':
            view_shopping_list(username)

        nut_sum_shop = input("Do you want to view nutrition summary of your shopping list? (yes/no): ").strip().lower()
        if nut_sum_shop == 'yes':
            calculate_nutrition_summary_shopping()

        add_to_favorite_list = input("\nDo you want to add this product to your favourite list? (yes/no): ").strip().lower()

        if add_to_favorite_list == 'yes':
            quantity_favourite = input("\n Enter quantity of product (int): ")
            add_to_fav_list(username, result, quantity_favourite)  # Pass all fields of the product

        view_favourite_list = input("Do you want to view your favourite list? (yes/no): ").strip().lower()
        if view_favourite_list == 'yes':
            view_fav_list(username)

        nut_sum_fav = input("Do you want to view nutrition summary of your favourite list? (yes/no): ").strip().lower()
        if nut_sum_fav == 'yes':
            calculate_nutrition_summary_shopping()
    else:
        print(f"No product found with barcode: {barcode}")

def display_filters():
    print("Select a filter option:")
    print("1. Carbohydrates")
    print("2. Proteins")
    print("3. Sugars")
    print("4. Total Fat")
    print("5. Saturated Fat")

def check_db_validity():
    """Check the validity of both user auth and product databases."""
    def check_user_auth_db():
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        try:
            cursor.execute("PRAGMA table_info(Users);")
            columns = cursor.fetchall()
            expected_columns = {'username', 'password', 'email', 'phone_number', 'registration_date'}
            actual_columns = {column[1] for column in columns}
            if not expected_columns.issubset(actual_columns):
                print("User auth DB is missing some expected columns.")
                return False
        except sqlite3.Error as e:
            print("User auth DB validation failed:", e)
            return False
        finally:
            conn.close()
        return True

    def check_product_db():
        conn = sqlite3.connect(PRODUCT_DB_PATH)
        cursor = conn.cursor()
        try:
            cursor.execute("PRAGMA table_info(Products);")
            columns = cursor.fetchall()
            expected_columns = {'barcode_num', 'product_name', 'ingredients', 'energy', 'proteins', 'carbohydrates', 'cholesterol', 'sugars', 'total_fat', 'saturated_fat',
                                       'trans_fat', 'sodium', 'fruits_vegetables_nuts', 'dietary_fibre', 'allergens', 'nutrition_grade', 'calcium', 'iodine', 'zinc', 'phosphorous', 'magnesium', 'vitamin_A', 'vitamin_B', 'vitamin_C', 'vitamin_D', 'vitamin_E', 'vitamin_K', 'other'
                                       }
        
            
            actual_columns = {column[1] for column in columns}
            if not expected_columns.issubset(actual_columns):
                print("Product DB is missing some expected columns.")
                return False
        except sqlite3.Error as e:
            print("Product DB validation failed:", e)
            return False
        finally:
            conn.close()
        return True

    user_db_valid = check_user_auth_db()
    product_db_valid = check_product_db()

    if not user_db_valid or not product_db_valid:
        print("One or both databases are not valid. Please check the database setup.")
        return False
    return True

def initialize_product_db():
    """Initialize the product database and ensure the Products table exists."""
    conn = sqlite3.connect(PRODUCT_DB_PATH)
    cursor = conn.cursor()
    
    # Drop table if it exists
    cursor.execute("DROP TABLE IF EXISTS Products")
    
    # Create the Products table with the specified schema
    cursor.execute("""
       CREATE TABLE IF NOT EXISTS Products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            barcode_num TEXT UNIQUE,
            product_name TEXT,
            ingredients TEXT,
            energy REAL,
            proteins REAL,
            carbohydrates REAL,
            cholesterol REAL,
            sugars REAL,
            total_fat REAL,
            saturated_fat REAL,
            trans_fat REAL,       
            sodium REAL,
            fruits_vegetables_nuts REAL,
            dietary_fibre REAL DEFAULT 0,
            allergens TEXT,
            nutrition_grade TEXT,
            calcium REAL DEFAULT 0,
            iodine REAL DEFAULT 0,
            zinc REAL DEFAULT 0,
            phosphorous REAL DEFAULT 0,
            magnesium REAL DEFAULT 0,
            vitamin_A REAL DEFAULT 0,
            vitamin_B REAL DEFAULT 0,
            vitamin_C REAL DEFAULT 0,
            vitamin_D REAL DEFAULT 0,
            vitamin_E REAL DEFAULT 0,
            vitamin_K REAL DEFAULT 0,
            other TEXT DEFAULT ""
        )
    """)
    
    conn.commit()
    conn.close()
    print("Product database initialized and schema created.")

def get_valid_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

def get_valid_int(prompt, max_choice):
    while True:
        try:
            choice = int(input(prompt))
            if 1 <= choice <= max_choice:
                return choice
            else:
                print(f"Invalid choice. Please enter a number between 1 and {max_choice}.")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

def collect_form_data(username):
    """Collect and store health data from the user."""
    conn = sqlite3.connect(HEALTH_DB_PATH)
    cursor = conn.cursor()

    age = get_valid_int("Enter your age: ", 100)
    height = get_valid_float("Enter your height (in cm): ")
    weight = get_valid_float("Enter your weight (in kg): ")

    print("What is your dietary type?")
    print("1. Eggetarian 2. Vegetarian 3. Non-vegetarian 4. Jain")
    diet_choice = get_valid_int("Your choice: ", 4)
    diet_type = ['Eggetarian', 'Vegetarian', 'Non-vegetarian', 'Jain'][diet_choice-1]

    print("What chronic illnesses do you have? (separate multiple answers with commas)")
    print("1. Diabetes 2. Obesity 3. High blood pressure 4. Heart diseases 5. Lactose intolerance/food allergies 6. None")
    chronic_illness_choices = input("Your choices: ").split(',')
    illness_map = ['Diabetes', 'Obesity', 'High blood pressure', 'Heart diseases', 'Lactose intolerance/food allergies', 'None']
    try:
        chronic_illnesses = [illness_map[int(choice.strip())-1] for choice in chronic_illness_choices]
    except (IndexError, ValueError):
        print("Invalid choice(s). Defaulting to 'None'.")
        chronic_illnesses = ['None']

    print("What specific dietary restrictions do you follow? (separate multiple answers with commas)")
    print("1. Low-sugar 2. Low-fat 3. Low-salt 4. Protein-rich 5. Anti-inflammatory 6. Gluten-free")
    dietary_restriction_choices = input("Your choices: ").split(',')
    restriction_map = ['Low-sugar', 'Low-fat', 'Low-salt', 'Protein-rich', 'Anti-inflammatory', 'Gluten-free']
    try:
        dietary_restrictions = [restriction_map[int(choice.strip())-1] for choice in dietary_restriction_choices]
    except (IndexError, ValueError):
        print("Invalid choice(s). No dietary restrictions recorded.")
        dietary_restrictions = []

    print("Are there specific ingredients that trigger your condition(s) or cause discomfort? (separate multiple answers with commas)")
    print("1. Sugar 2. Fats 3. Salt 4. Lactose 5. Wheat 6. None")
    trigger_choices = input("Your choices: ").split(',')

    # Define the mapping including 'None'
    trigger_map = ['Sugar', 'Fats', 'Salt', 'Lactose', 'Wheat', 'None']
    try:
        # Use list comprehension to gather selected triggers
        trigger_ingredients = [trigger_map[int(choice.strip()) - 1] for choice in trigger_choices]
        
        # Check if 'None' was selected, if so clear the list
        if 'None' in trigger_ingredients:
            trigger_ingredients = ['None']
    except (IndexError, ValueError):
        print("Invalid choice(s). No trigger ingredients recorded.")
        trigger_ingredients = []

    print("What health goal do you have? (separate multiple answers with commas)")
    print("1. Blood sugar control 2. Weight maintenance 3. Manage cholesterol 4. Blood pressure control 5. Bodybuilding 6. Control symptoms of your chronic illness 7. None")
    health_goal_choices = input("Your choices: ").split(',')
    goal_map = ['Blood sugar control', 'Weight maintenance', 'Manage cholesterol', 'Blood pressure control', 'Bodybuilding', 'Control symptoms of your chronic illness', 'None']
    try:
        health_goals = [goal_map[int(choice.strip())-1] for choice in health_goal_choices]
    except (IndexError, ValueError):
        print("Invalid choice(s). Defaulting to 'None'.")
        health_goals = ['None']

    cursor.execute('''
    INSERT INTO health_form (username, age, height, weight, diet_type, chronic_illnesses, dietary_restrictions, trigger_ingredients, health_goals)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (username, age, height, weight, diet_type,','.join(chronic_illnesses),','.join(dietary_restrictions), ','.join(trigger_ingredients), ','.join(health_goals)))

    conn.commit()
    conn.close()

    return {
        'What is your dietary type?': [diet_type],
        'What chronic illnesses do you have? (separate multiple answers with commas)': chronic_illnesses,
        'What specific dietary restrictions do you follow? (separate multiple answers with commas)': dietary_restrictions,
        'Are there specific ingredients that trigger your condition(s) or cause discomfort? (separate multiple answers with commas)': trigger_ingredients,
        'What health goal do you have? (separate multiple answers with commas)': health_goals
    }

def calculate_probabilities(user_input, data):
    total_count = len(data)
    ingredient_counts = defaultdict(int)
    conditional_counts = defaultdict(lambda: defaultdict(int))

    for _, row in data.iterrows():
        ingredients_str = row['What are some healthy alternatives/ingredients you include in your diet?']
        if pd.notna(ingredients_str) and isinstance(ingredients_str, str):
            ingredients = [ing.strip().lower() for ing in ingredients_str.split(',')]
            for ingredient in ingredients:
                ingredient_counts[ingredient] += 1
                for column, values in user_input.items():
                    if pd.notna(row[column]):
                        row_values = set(val.strip().lower() for val in str(row[column]).split(','))
                        if any(value.lower() in row_values for value in values):
                            conditional_counts[ingredient][column] += 1

    probabilities = {}
    smoothing_factor = 0.1  # Laplace smoothing
    for ingredient, count in ingredient_counts.items():
        prior = (count + smoothing_factor) / (total_count + smoothing_factor * len(ingredient_counts))
        likelihood = 1
        for column, values in user_input.items():
            cond_count = conditional_counts[ingredient][column]
            likelihood *= (cond_count + smoothing_factor) / (count + smoothing_factor * 2)
        probabilities[ingredient] = prior * likelihood

    return probabilities

def recommend_ingredients(username):
    # Fetch user data from the health database
    user_input = fetch_health_data(username)

    # Load the CSV file
    df = pd.read_csv(REC_PRODUCT_PATH)
    
    df.columns = [
        'What is your dietary type?',
        'What chronic illnesses do you have? (separate multiple answers with commas)',
        'What specific dietary restrictions do you follow? (separate multiple answers with commas)',
        'Are there specific ingredients that trigger your condition(s) or cause discomfort? (separate multiple answers with commas)',
        'What are some healthy alternatives/ingredients you include in your diet?',
        'What health goal do you have? (separate multiple answers with commas)'
    ]

    # Calculate probabilities
    probabilities = calculate_probabilities(user_input, df)
    
    # Sort ingredients by probability and filter those with confidence >= 0.010
    recommended_ingredients = sorted(
        [(ingredient, prob) for ingredient, prob in probabilities.items() if prob >= 0.010],
        key=lambda x: x[1],
        reverse=True
    )

    print("\nRecommended healthy alternatives/ingredients for your diet:")
    if recommended_ingredients:
        for i, (ingredient, _) in enumerate(recommended_ingredients, 1):
            print(f"{i}. {ingredient.capitalize()}")
    else:
        print("No recommendations were found based on your input.")

    # Ensure recommended_ingredients is a list and process each item
    if isinstance(recommended_ingredients, tuple):
        recommended_ingredients = list(recommended_ingredients)
    elif not isinstance(recommended_ingredients, list):
        recommended_ingredients = [recommended_ingredients]

    # Process each ingredient
    processed_ingredients = []
    for item in recommended_ingredients:
        # Split by numbers and periods, then take the last part
        parts = re.split(r'\d+\.?\s*', item[0])  # Note: item[0] to get the ingredient name
        ingredient = parts[-1].strip().lower() if parts else ''
        if ingredient:
            processed_ingredients.append(ingredient)

    products = get_products_by_ingredients(processed_ingredients)

    # Display product information
    display_product_info_ing(products)

    return None

def fetch_health_data(username):
    """Fetch health data from the database for a given user."""
    conn = sqlite3.connect(HEALTH_DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
    SELECT age, height, weight, diet_type, chronic_illnesses, dietary_restrictions, trigger_ingredients, health_goals
    FROM health_form
    WHERE username = ?
    ''', (username,))

    result = cursor.fetchone()

    if result:
        # Map the fetched data to a dictionary similar to the form data
        age, height, weight, diet_type, chronic_illnesses, dietary_restrictions, trigger_ingredients, health_goals,  = result
        health_data = {
            'What is your dietary type?': [diet_type],
            'What chronic illnesses do you have? (separate multiple answers with commas)': chronic_illnesses.split(','),
            'What specific dietary restrictions do you follow? (separate multiple answers with commas)': dietary_restrictions.split(','),
            'Are there specific ingredients that trigger your condition(s) or cause discomfort? (separate multiple answers with commas)': trigger_ingredients.split(','),
            'What health goal do you have? (separate multiple answers with commas)': health_goals.split(',')
        }
    else:
        print(f"No data found for user {username}.")
        health_data = {}

    conn.close()

    return health_data

def get_products_by_ingredients(ingredients):
    # Connect to the SQLite database
    conn = sqlite3.connect(PRODUCT_DB_PATH)
    cursor = conn.cursor()

    try:
        # Ensure ingredients is a list and remove any blank spaces
        if isinstance(ingredients, tuple):
            ingredients = list(ingredients)
        elif not isinstance(ingredients, list):
            ingredients = [ingredients]

        # Remove blank spaces and empty strings from ingredients
        ingredients = [i.strip().lower() for i in ingredients if i.strip()]

        # Create a query that will match any of the ingredients
        query = """
        SELECT id, barcode_num, product_name, ingredients, energy, proteins, carbohydrates, cholesterol, sugars, total_fat, saturated_fat, trans_fat, sodium, fruits_vegetables_nuts, dietary_fibre, allergens, nutrition_grade, calcium, iodine, zinc, phosphorous, magnesium, vitamin_A, vitamin_B, vitamin_C, vitamin_D, vitamin_E, vitamin_K, other
        FROM products
        WHERE {}
        """

        # Create conditions for each ingredient
        conditions = " OR ".join([f"LOWER(ingredients) LIKE ?" for _ in ingredients])
        query = query.format(conditions)

        # Execute the query with all ingredients
        cursor.execute(query, tuple(f'%{ingredient}%' for ingredient in ingredients))

        # Fetch all matching results
        results = cursor.fetchall()
        return results

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the database connection
        conn.close()

    return None

def display_product_info_ing(products):
    if not products:
        print("No products found containing any of the recommended ingredients.")
        return

    for product in products:
        print("\nProduct Information:")
        print(f"Product Name: {product[2]}")
        print(f"Barcode: {product[1]}")
        print(f"Ingredients: {product[3]}")
        print(f"Energy: {product[4]}")
        print(f"Proteins: {product[5]}")
        print(f"Carbohydrates: {product[6]}")
        print(f"Cholesterol: {product[7]}")
        print(f"Sugars: {product[8]}")
        print(f"Total Fat: {product[9]}")
        print(f"Saturated Fat: {product[10]}")
        print(f"Trans Fat: {product[11]}")
        print(f"Sodium: {product[12]}")
        print(f"Fruits/Vegetables/Nuts: {product[13]}")
        print(f"Dietary Fibre: {product[14]}")
        print(f"Allergens: {product[15]}")
        print(f"Nutrition Grade: {product[16]}")
        print(f"Calcium: {product[17]}")
        print(f"Iodine: {product[18]}")
        print(f"Zinc: {product[19]}")
        print(f"Phosphorous: {product[20]}")
        print(f"Magnesium: {product[21]}")
        print(f"Vitamin A: {product[22]}")
        print(f"Vitamin B: {product[23]}")
        print(f"Vitamin C: {product[24]}")
        print(f"Vitamin D: {product[25]}")
        print(f"Vitamin E: {product[26]}")
        print(f"Vitamin K: {product[27]}")
        print(f"Other: {product[28]}")
        print("-" * 50)

class Register:
    def __init__(self, *args):
        self.conn = sqlite3.connect(DB_PATH)
        self.data = {}
        self.get_user_input(args)

    def get_user_input(self, variables):
        for variable in variables:
            if variable.lower() == "password":
                self.data[variable] = getpass(f"Enter {variable}: ")
            elif variable.lower() == "email":
                while True:
                    email = input(f"Enter {variable}: ")
                    # Adjust email validation to accept all domains
                    if re.match(r"[^@]+@[^@]+\.[a-zA-Z]{2,}$", email):
                        self.data[variable] = email
                        break
                    else:
                        print("Invalid email format. Please enter a valid email.")
            elif variable.lower() == "username":
                while True:
                    username = input(f"Enter {variable} (alphanumeric): ")
                    if username.isalnum():
                        self.data[variable] = username
                        break
                    else:
                        print("Invalid username. Please enter alphanumeric characters only.")
            elif variable.lower() == "phone_number":
                while True:
                    phone = input(f"Enter {variable} (optional): ")
                    if phone.isdigit() and len(phone) == 10:
                        self.data[variable] = phone
                        break
                    elif phone == "":
                        # Allow empty phone number if it's optional
                        self.data[variable] = phone
                        break
                    else:
                        print("Invalid phone number. Please enter a 10-digit number.")
            else:
                self.data[variable] = input(f"Enter {variable}: ")

    def collect_health_data(self, username):
        """Collect and store health data from the user."""
        collect_form_data(username)

    def register_user(self):
        try:
            hashed_password = hashlib.sha256(self.data['password'].encode()).hexdigest()
            cursor = self.conn.cursor()
            username = self.data['username']
            email = self.data['email']
            phone_number = self.data.get('phone_number')
            registration_date = datetime.datetime.now()

            cursor.execute("""
                INSERT INTO Users (username, password, email, phone_number, registration_date)
                VALUES (?, ?, ?, ?, ?)
            """, (username, hashed_password, email, phone_number, registration_date))
            self.conn.commit()

            # Collect health data after user registration
            self.collect_health_data(username)

            print("Registration successful!")
        except sqlite3.Error as e:
            print("Registration failed:", e)
        finally:
            self.conn.close()

class Login:
    def __init__(self, username, password, conn=None):
        self.username = username
        self.password = password
        self.conn = sqlite3.connect(DB_PATH) if conn is None else conn

    def authenticate(self):
        try:
            hashed_password = hashlib.sha256(self.password.encode()).hexdigest()
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Users WHERE username = ? AND password = ?", 
                           (self.username, hashed_password))
            result = cursor.fetchone()
            if result:
                print("Login successful!")
                if self.username == "admin":
                    admin_interface()
                else:
                    # Pass the username to the post-login menu
                    post_login_menu(self.username)
                return True
            else:
                print("Login failed. Invalid username or password.")
                return False
        except sqlite3.Error as e:
            print("Login failed:", e)
            return False
        finally:
            self.conn.close()

def admin_interface():
    """Admin functionalities for managing users and products."""
    while True:
        print("\n--- Admin Interface ---")
        print("1: View Auth DB")
        print("2: Add User")
        print("3: Remove User")
        print("4: Change User Password")
        print("5: Add Products and Nutrient Info")
        print("6: Delete Product from Database")
        print("7: View All Products")
        print("8: Edit a Product")
        print("9: Log Out")

        try:
            choice = int(input("Select an option: "))
            if choice == 1:
                view_auth_db()
            elif choice == 2:
                add_user()
            elif choice == 3:
                remove_user()
            elif choice == 4:
                change_user_password()
            elif choice == 5:
                add_product()
            elif choice == 6:
                delete_product()
            elif choice == 7:
                view_all_products()
            elif choice == 8:
                edit_product()
            elif choice == 9:
                break  # Back to main menu
            else:
                print("Invalid option. Please select a valid option.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def calculate_nutri_score(data, moist):
    nutri_score = NutriScore()
    result = nutri_score.calculate_class(data, moist)
    print(f"The Nutri-Score for this product is: {result}")
    return result

def calculate_health_score(user_health_data, product_data):
    
    score = 50  # Start with a neutral score of 50
    max_score = 100
    
    # Normalize user health data
    chronic_illnesses = [illness.strip().lower() for illness in user_health_data.get('chronic_illnesses', '').split(',')]
    dietary_restrictions = [restriction.strip().lower() for restriction in user_health_data.get('dietary_restrictions', '').split(',')]
    trigger_ingredients = [trigger.strip().lower() for trigger in user_health_data.get('trigger_ingredients', '').split(',')]
    health_goals = [goal.strip().lower() for goal in user_health_data.get('health_goals', '').split(',')]

    # Assign penalties based on chronic illnesses and allergens
    if 'lactose intolerance' in chronic_illnesses and 'lactose' in product_data.get('allergens', '').lower():
        score -= 10
    if 'diabetes' in chronic_illnesses and product_data.get('sugars', 0) > 25:  # Increased sugar threshold
        score -= 20  # Reduced sugar penalty
    if 'high blood pressure' in chronic_illnesses and product_data.get('sodium', 0) > 200:
        score -= 15

    # Assign rewards for health goals and dietary preferences
    if 'low-sugar' in dietary_restrictions and product_data.get('sugars', 0) < 10:
        score += 10
    if 'protein-rich' in dietary_restrictions and product_data.get('proteins', 0) > 15:
        score += 25  # Slightly reduced reward to balance
    if 'bodybuilding' in health_goals and product_data.get('proteins', 0) > 15:
        score += 35  # Increased reward for protein-rich products
    if 'fiber-rich' in dietary_restrictions and product_data.get('dietary_fibre', 0) > 8:
        score += 10  # Reward for high fiber

    # Penalties for unhealthy content
    if product_data.get('sugars', 0) > 25:  # Increased sugar threshold for penalty
        score -= 10  # High sugar penalty
    if product_data.get('saturated_fat', 0) > 8:
        score -= 10  # Reduced saturated fat penalty
    if product_data.get('trans_fat', 0) > 0:
        score -= 10  # Trans fat penalty

    # Reward for natural ingredients and whole foods
    if 'oats' in product_data.get('ingredients', '').lower() or 'nuts' in product_data.get('ingredients', '').lower():
        score += 15  # Increase reward for whole grains and nuts

    # Penalty for artificial additives
    additives = ['preservatives', 'artificial', 'emulsifiers', 'stabilizers']
    for additive in additives:
        if additive in product_data.get('ingredients', '').lower():
            score -= 3  # Reduced penalty for each artificial ingredient

    # Reward for gluten-free products if the user has gluten restrictions
    if 'gluten-free' in dietary_restrictions and 'wheat' not in product_data.get('allergens', '').lower():
        score += 10

    # Ensure score is within the 0-100 range
    score = max(0, min(score, max_score))
    
    # Scale score to 1-5
    final_score = int(round((score / max_score) * 5))
    final_score = max(1, min(final_score, 5))  # Ensure the final score is between 1 and 5
    
    return final_score

def post_login_menu(username):
    while True:
        print("\n--- Post-Login Menu ---")
        print("1: View product information via Scanning Barcode")
        print("2: View product information via barcode number")
        print("3: User Profile Interface")
        print("4: Log Out")
        print("5: View shopping list")
        print("6: View favourite list")
        print("7: Delete from shopping list")
        print("8: Delete from favourite list")
        print("9: Search products based on filter")
        print("10: View all products")
        print("11: Recommend me")
        
        try:
            choice = int(input("Select an option: "))
            if choice == 1:
                use_custom_url = input("Do you want to use a custom IP address? (y/n): ").lower() == 'y'
                scan_barcode(username) 
            elif choice == 2:
                barcode = input("Enter the barcode number: ")
                display_product_info(username,barcode)
            elif choice == 3:
                view_profile(username)  # Ensure the username is passed
            elif choice == 4:
                log_out()
                break
            elif choice == 5:
                view_shopping_list(username)
            elif choice == 6:
                view_fav_list(username)   
            elif choice == 7 : 
                product_name_shop = input("Enter the name of the product to delete: ").strip()
                quantity_to_delete_shop = int(input("Enter the quantity to delete: "))
                delete_from_shopping_list(username, product_name_shop, quantity_to_delete_shop)  
            elif choice == 8:
                product_name_fav = input("Enter the name of the product to delete: ").strip()
                quantity_to_delete_fav = int(input("Enter the quantity to delete: "))
                delete_from_fav_list(username, product_name_fav, quantity_to_delete_fav)
            elif choice == 9:
                display_filters()
            elif choice == 10:
                view_all_products()
            elif choice == 11:
                recommend_ingredients(username)
        except ValueError:
            print("Invalid input. Please enter a number.")
            
def view_profile(username):
    """Display the profile menu and handle user input."""
    while True:
        print(f"\n--- View Profile for {username} ---")
        print("1: Change Password")
        print("2: Log Out")
        print("3: Change Account Info")
        print("4: View User Profile Questions & Answers")
        print("5: Edit Your Answers")
        print("6: Favourite Items")
        print("7: Edit Goals")
        print("8: Wishlist")
        print("9: My Past Orders")
        print("10: Cart")
        print("11: Change Payment Information")
        print("12: Health Chart")
        print("13: Savings Chart")

        try:
            choice = int(input("Select an option: "))
            if choice == 1:
                change_password(username)
            elif choice == 2:
                if log_out():
                    break
            elif choice == 3:
                change_account_info(username)
            elif choice == 4:
                view_user_questions(username)
            elif choice == 5:
                edit_user_questions(username)
            elif choice == 6:
                view_fav_list(username)
            elif 7 <= choice <= 9:
                print(f"Feature {choice}: Placeholder for the selected option.")
            elif choice == 10:
                view_shopping_list(username)
            elif 11 <= choice <= 13:
                print(f"Feature {choice}: Placeholder for the selected option.")
            else:
                print("Invalid option. Please select a valid option.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def view_user_questions(username):
    """Display the user's profile questions and answers."""
    conn = sqlite3.connect(HEALTH_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM health_form WHERE username = ?", (username,))
    result = cursor.fetchone()
    if result:
        print("\n--- User Profile Questions & Answers ---")
        print(f"Username: {result[1]}")
        print(f"Age: {result[2]}")
        print(f"Height: {result[3]} cm")
        print(f"Weight: {result[4]} kg")
        print(f"Dietary type: {result[5]}")
        print(f"Health conditions: {result[6]}")
        print(f"Diet restrictions: {result[7]}")
        print(f"Specific triggers: {result[8]}")
        print(f"Health goals: {result[9]}")
    else:
        print("User profile data not found.")
    conn.close()

def edit_user_questions(username):
    """Allow the user to edit their profile questions."""
    conn = sqlite3.connect(HEALTH_DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM health_form WHERE username = ?", (username,))
    result = cursor.fetchone()
    
    if result:
        # Prompt for new height and weight
        height = get_valid_float("Enter your height (in cm): ")
        weight = get_valid_float("Enter your weight (in kg): ")

        # Update other fields based on current values
        age = input(f"Age (current: {result[2]}): ")
        
        print("What is your dietary type? Current: ", result[4])
        print("1. Eggetarian 2. Vegetarian 3. Non-vegetarian 4. Jain")
        diet_choice = input("Enter new choice or press Enter to keep current: ")
        if diet_choice:
            diet_type = ['Eggetarian', 'Vegetarian', 'Non-vegetarian', 'Jain'][int(diet_choice) - 1] if diet_choice in ['1', '2', '3', '4'] else result[4]
        else:
            diet_type = result[4]

        print("What chronic illnesses do you have? Current: ", result[5])
        print("1. Diabetes 2. Obesity 3. High blood pressure 4. Heart diseases 5. Lactose intolerance/food allergies 6. None")
        chronic_illness_choices = input("Enter new choices (comma-separated) or press Enter to keep current: ").split(',')
        illness_map = ['Diabetes', 'Obesity', 'High blood pressure', 'Heart diseases', 'Lactose intolerance/food allergies', 'None']
        
        if chronic_illness_choices:
            try:
                chronic_illnesses = [illness_map[int(choice.strip()) - 1] for choice in chronic_illness_choices]
            except (IndexError, ValueError):
                print("Invalid choice(s). Defaulting to 'None'.")
                chronic_illnesses = ['None']
        else:
            chronic_illnesses = result[5].split(',')  # Keep current values

        print("What specific dietary restrictions do you follow? Current: ", result[6])
        print("1. Low-sugar 2. Low-fat 3. Low-salt 4. Protein-rich 5. Anti-inflammatory 6. Gluten-free")
        dietary_restriction_choices = input("Enter new choices (comma-separated) or press Enter to keep current: ").split(',')
        restriction_map = ['Low-sugar', 'Low-fat', 'Low-salt', 'Protein-rich', 'Anti-inflammatory', 'Gluten-free']
        
        if dietary_restriction_choices:
            try:
                dietary_restrictions = [restriction_map[int(choice.strip()) - 1] for choice in dietary_restriction_choices]
            except (IndexError, ValueError):
                print("Invalid choice(s). No dietary restrictions recorded.")
                dietary_restrictions = []
        else:
            dietary_restrictions = result[6].split(',')  # Keep current values

        print("Are there specific ingredients that trigger your condition(s)? Current: ", result[7])
        print("1. Sugar 2. Fats 3. Salt 4. Lactose 5. Wheat 6. None")
        trigger_choices = input("Enter new choices (comma-separated) or press Enter to keep current: ").split(',')
        
        # Define the mapping including 'None'
        trigger_map = ['Sugar', 'Fats', 'Salt', 'Lactose', 'Wheat', 'None']
        
        if trigger_choices:
            try:
                trigger_ingredients = [trigger_map[int(choice.strip()) - 1] for choice in trigger_choices]
                if 'None' in trigger_ingredients:
                    trigger_ingredients = ['None']
            except (IndexError, ValueError):
                print("Invalid choice(s). No trigger ingredients recorded.")
                trigger_ingredients = []
        else:
            trigger_ingredients = result[7].split(',')  # Keep current values

        print("What health goal do you have? Current: ", result[8])
        print("1. Blood sugar control 2. Weight maintenance 3. Manage cholesterol 4. Blood pressure control 5. Bodybuilding 6. Control symptoms of your chronic illness 7. None")
        health_goal_choices = input("Enter new choices (comma-separated) or press Enter to keep current: ").split(',')
        goal_map = ['Blood sugar control', 'Weight maintenance', 'Manage cholesterol', 'Blood pressure control', 'Bodybuilding', 'Control symptoms of your chronic illness', 'None']
        
        if health_goal_choices:
            try:
                health_goals = [goal_map[int(choice.strip()) - 1] for choice in health_goal_choices]
            except (IndexError, ValueError):
                print("Invalid choice(s). Defaulting to 'None'.")
                health_goals = ['None']
        else:
            health_goals = result[8].split(',')  # Keep current values

        # Update the database with new values (if any were provided)
        cursor.execute('''UPDATE health_form 
                          SET age = ?, height = ?, weight = ?, diet_type = ?, 
                              chronic_illnesses = ?, dietary_restrictions = ?, 
                              trigger_ingredients = ?, health_goals = ?
                          WHERE username = ?''',
                       (age or result[2],
                        height or result[3], 
                        weight or result[4], 
                        diet_type,
                        ','.join(chronic_illnesses), 
                        ','.join(dietary_restrictions), 
                        ','.join(trigger_ingredients), 
                        ','.join(health_goals), 
                        username))

        conn.commit()
        print("Profile updated successfully.")
    else:
        print("User profile data not found.")
    conn.close()

def change_password(username):
    """Change the user's password with old password verification."""
    db_path = os.path.join(os.path.dirname(__file__), 'user_auth.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print(f"Attempting to change password for username: {username}")

    old_password = getpass("Enter old password: ")
    new_password = getpass("Enter new password: ")
    confirm_password = getpass("Confirm new password: ")

    if new_password != confirm_password:
        print("Passwords do not match. Please try again.")
        conn.close()
        return

    hashed_old_password = hashlib.sha256(old_password.encode()).hexdigest()
    cursor.execute("SELECT password FROM Users WHERE username = ?", (username,))
    stored_password = cursor.fetchone()

    if stored_password and stored_password[0] == hashed_old_password:
        hashed_new_password = hashlib.sha256(new_password.encode()).hexdigest()
        cursor.execute("UPDATE Users SET password = ? WHERE username = ?", (hashed_new_password, username))
        conn.commit()
        print("Password updated successfully.")
    else:
        print("Old password is incorrect.")
    
    conn.close()

def log_out():
    """Handle the logout process with confirmation."""
    confirmation = input("Are you sure you want to log out? (yes/no): ").lower()
    if confirmation == "yes":
        print("Logging out...")
        return True  # Indicate successful logout
    else:
        print("Logout canceled.")
        return False  # Indicate logout was canceled

def change_account_info(username):
    """Change the user's account info (username or phone number)."""
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'user_auth.db'))
    cursor = conn.cursor()

    print("\n--- Change Account Info ---")
    print("1: Change Username")
    print("2: Change Phone Number")

    try:
        choice = int(input("Select an option: "))
        if choice == 1:
            email = input("Enter your email: ")
            password = getpass("Enter your password: ")
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            cursor.execute("SELECT * FROM Users WHERE username = ? AND email = ? AND password = ?", 
                           (username, email, hashed_password))
            result = cursor.fetchone()

            if result:
                new_username = input("Enter new username (alphanumeric): ")
                if new_username.isalnum():
                    cursor.execute("SELECT * FROM Users WHERE username = ?", (new_username,))
                    if cursor.fetchone():
                        print("Username already taken. Please try a different username.")
                    else:
                        cursor.execute("UPDATE Users SET username = ? WHERE email = ?", (new_username, email))
                        conn.commit()
                        print("Username updated successfully.")
                else:
                    print("Invalid username. Please enter alphanumeric characters only.")
            else:
                print("Authentication failed. Invalid email or password.")
        elif choice == 2:
            password = getpass("Enter your password: ")
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            cursor.execute("SELECT * FROM Users WHERE username = ? AND password = ?", 
                           (username, hashed_password))
            result = cursor.fetchone()

            if result:
                new_phone = input("Enter new phone number: ")
                cursor.execute("UPDATE Users SET phone_number = ? WHERE username = ?", (new_phone, username))
                conn.commit()
                print("Phone number updated successfully.")
            else:
                print("Authentication failed. Invalid username or password.")
        else:
            print("Invalid option. Please select a valid option.")
    except ValueError:
        print("Invalid input. Please enter a number.")
    conn.close()

def view_auth_db():
    """Display all users in the authentication database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email, phone_number, registration_date FROM Users")
    users = cursor.fetchall()
    
    print("\n--- Registered Users ---")
    for user in users:
        print(f"ID: {user[0]}, Username: {user[1]}, Email: {user[2]}, Phone: {user[3]}, Registration Date: {user[4]}")
    
    conn.close()

def add_user():
    """Add a new user to the database."""
    fields = ["username", "password", "email", "phone_number"]
    reg = Register(*fields)
    reg.register_user()

def list_tables(cursor):
    """List all tables in the database."""
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Debug: Tables in the database:")
    for table in tables:
        print(f" - {table[0]}")

def remove_user():
    """Remove a user from the database, but restrict removing the 'admin' account."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        username = input("Enter the username of the user to remove: ")

        if username == "admin":
            print("The 'admin' account cannot be removed.")
            return

        # Check if the user exists
        cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
        if cursor.fetchone():
            # Retrieve the user's health data before deletion
            with sqlite3.connect(HEALTH_DB_PATH) as conn_health:
                cursor_health = conn_health.cursor()
                cursor_health.execute("SELECT * FROM health_form WHERE username = ?", (username,))
                user_health_data = cursor_health.fetchone()

            # Display user's health data before deletion
            if user_health_data:
                print("User's health data:")
                print(f"Age: {user_health_data[1]}")
                print(f"Height: {user_health_data[2]} cm")
                print(f"Weight: {user_health_data[3]} kg")
                print(f"Diet Type: {user_health_data[4]}")
                print(f"Chronic Illnesses: {user_health_data[5]}")
                print(f"Dietary Restrictions: {user_health_data[6]}")
                print(f"Trigger Ingredients: {user_health_data[7]}")
                print(f"Health Goals: {user_health_data[8]}")

            # Confirm deletion
            confirm = input("Are you sure you want to remove this user and their health data? (yes/no): ")
            if confirm.lower() != 'yes':
                print("User removal cancelled.")
                return

            # Delete user's health data
            cursor_health.execute("DELETE FROM health_form WHERE username = ?", (username,))
            conn_health.commit()

            # Delete user from Users table
            cursor.execute("DELETE FROM Users WHERE username = ?", (username,))
            conn.commit()
            print("User and associated health data removed successfully.")
        else:
            print("User not found.")

def change_user_password():
    """Change the password of a specified user, but restrict changes for the 'admin' account."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    username = input("Enter the username of the user whose password you want to change: ")

    if username == "admin":
        print("The password for the 'admin' account cannot be changed.")
        return

    cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
    if cursor.fetchone():
        new_password = getpass("Enter new password: ")
        confirm_password = getpass("Confirm new password: ")

        if new_password == confirm_password:
            hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
            cursor.execute("UPDATE Users SET password = ? WHERE username = ?", (hashed_password, username))
            conn.commit()
            print("Password updated successfully.")
        else:
            print("Passwords do not match.")
    else:
        print("User not found.")
    
    conn.close()

def add_product():
    """Add a product and its nutrient info to the database."""
    conn = sqlite3.connect(PRODUCT_DB_PATH)
    cursor = conn.cursor()

    # Collect product details
    while True:
        barcode_num = input("Enter product barcode number: ")
        if len(barcode_num) == 13:
            break
        else:
            print("Invalid barcode number. Please enter a valid 13-digit barcode.")
    product_name = input("Enter product name: ")
    ingredients = input("Enter ingredients (comma separated): ")

    # Collect main nutrient information
    try:
        energy = float(input("Enter energy in kcal: ")) * 4.184  # Convert to kJ
        proteins = float(input("Enter proteins in g: "))
        carbohydrates = float(input("Enter carbohydrates in g: "))
        cholesterol = float(input("Enter total cholesterol in g: "))
        sugars = float(input("Enter sugars in g: "))
        total_fat = float(input("Enter total fat in g: "))
        saturated_fat = float(input("Enter saturated fat in g: "))
        trans_fat = float(input("Enter trans-fat in g: "))
        sodium = float(input("Enter sodium in mg: "))
        fruits_vegetables_nuts = float(input("Enter fruits, vegetables, nuts percentage: "))
        dietary_fibre = float(input("Enter fibre in g: "))
        allergens = input("Enter allergens (comma separated): ")
        moist = input("Enter product type (solid or beverage): ").strip().lower()


    except ValueError:
        print("Invalid input for numeric values. Please enter valid numbers.")
        conn.close()
        return
   
    # Calculate Nutri-Score

    data={
    'energy':  energy*4.184,
    'fibers': dietary_fibre,
    'fruit_percentage': fruits_vegetables_nuts,
    'proteins': proteins,
    'saturated_fats': saturated_fat,
    'sodium': sodium,
    'sugar': sugars
    }
    nutri_score =calculate_nutri_score(data, moist)

    # Initialize additional nutrients dictionary
    additional_minerals = {
        'calcium': 0,
        'iodine': 0,
        'zinc': 0,
        'phosphorous': 0,
        'magnesium': 0
        
    }
    additional_vitamins = {
        'vitamin_A': 0,
        'vitamin_B': 0,
        'vitamin_C': 0,
        'vitamin_D': 0,
        'vitamin_E': 0,
        'vitamin_K': 0
    }

    additional_others = {
        'other' : ""
    }
    # Ask if user wants to input more nutrients
    more_vit = input("Do you want to input more vitamins? (yes/no): ").lower()
    if more_vit == 'yes':
        try:
            for nutrient in additional_vitamins:
                unit = 'mg' if nutrient not in ['vitamin_A', 'vitamin_B', 'vitamin_D'] else 'mcg'
                unit = 'IU' if nutrient == 'vitamin_D' else unit
                additional_vitamins[nutrient] = float(input(f"Enter {nutrient} in {unit}: "))
        except ValueError:
            print("Invalid input for numeric values. Please enter valid numbers.")
            conn.close()
            return
        
    more_min = input("Do you want to input more minerals? (yes/no): ").lower()
    if more_min == 'yes':
        try:
            for nutrient in additional_minerals:
                unit_min = 'g'  
                additional_minerals[nutrient] = float(input(f"Enter {nutrient} in {unit_min}: "))
        except ValueError:
            print("Invalid input for numeric values. Please enter valid numbers.")
            conn.close()
            return

    more_others = input("Do you want to input more nutrients? (yes/no): ").lower()
    if more_others == 'yes':
        try:
            for nutrient in additional_others:
                additional_others[nutrient] = float(input(f"Enter {nutrient} : "))
        except ValueError:
            print("Invalid input for numeric values. Please enter valid numbers.")
            conn.close()
            return

    try:
        cursor.execute("""
        INSERT INTO Products (
            barcode_num, product_name, ingredients, energy, proteins, carbohydrates, cholesterol,
            sugars, total_fat, saturated_fat, trans_fat, sodium, fruits_vegetables_nuts,dietary_fibre,
            allergens, nutrition_grade, calcium, iodine, zinc, phosphorous, magnesium,
            vitamin_A, vitamin_B, vitamin_C, vitamin_D, vitamin_E, vitamin_K, other
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            barcode_num, product_name, ingredients, energy, proteins, carbohydrates, cholesterol,
            sugars, total_fat, saturated_fat, trans_fat, sodium, fruits_vegetables_nuts, dietary_fibre,
            allergens, nutri_score, additional_minerals['calcium'], additional_minerals['iodine'],
            additional_minerals['zinc'], additional_minerals['phosphorous'], additional_minerals['magnesium'],
            additional_vitamins['vitamin_A'], additional_vitamins['vitamin_B'], additional_vitamins['vitamin_C'],
            additional_vitamins['vitamin_D'], additional_vitamins['vitamin_E'], additional_vitamins['vitamin_K'],additional_others['other']
        ))
        conn.commit()
        print(f"Product '{product_name}' added successfully with Nutri-Score: {nutri_score}.")
    except sqlite3.IntegrityError:
        print("Error: Product with this barcode already exists.")
    except sqlite3.Error as e:
        print("Database error:", e)
    finally:
        conn.close()

def edit_product():
    """Edit a product and its nutrient info in the database."""
    try:
        conn = sqlite3.connect(PRODUCT_DB_PATH)
        cursor = conn.cursor()

        # Get product to edit
        barcode_num = input("Enter product barcode number: ")
        cursor.execute("SELECT * FROM Products WHERE barcode_num = ?", (barcode_num,))
        product = cursor.fetchone()
        
        if not product:
            print("Product not found.")
            return

        # Display current product information
        columns = [description[0] for description in cursor.description]
        print("\nCurrent product information:")
        for i, value in enumerate(product):
            print(f"{columns[i]}: {value}")

        # Collect updated product details
        print("\nUpdating product information:")
        new_values = list(product)
        nutri_score_relevant_fields = ['energy', 'dietary_fibre', 'fruits_vegetables_nuts', 'proteins', 'saturated_fat', 'sodium', 'sugars']
        nutri_score_fields_changed = False

        for i, column in enumerate(columns[1:], start=1):  # Start from index 1 to skip barcode
            edit_column = input(f"Do you want to edit {column}? (yes/no): ").lower()
            if edit_column == 'yes':
                new_value = input(f"Enter new {column} ({product[i]}): ").strip()
                if new_value:
                    if column in ['energy', 'proteins', 'carbohydrates', 'cholesterol', 'sugars', 'total_fat', 'saturated_fat', 'trans_fat', 'sodium', 'fruits_vegetables_nuts', 'dietary_fibre', 'calcium', 'iodine', 'zinc', 'phosphorous', 'magnesium', 'vitamin_A', 'vitamin_B', 'vitamin_C', 'vitamin_D', 'vitamin_E', 'vitamin_K']:
                        new_values[i] = float(new_value)
                    else:
                        new_values[i] = new_value
                    if column in nutri_score_relevant_fields:
                        nutri_score_fields_changed = True

        # Calculate new Nutri-Score only if relevant fields were changed
        if nutri_score_fields_changed:
            moist = input("Enter product type (solid or beverage): ").strip().lower()
            data = {
                'energy': new_values[columns.index('energy')] * 4.184,
                'fibers': new_values[columns.index('dietary_fibre')],
                'fruit_percentage': new_values[columns.index('fruits_vegetables_nuts')],
                'proteins': new_values[columns.index('proteins')],
                'saturated_fats': new_values[columns.index('saturated_fat')],
                'sodium': new_values[columns.index('sodium')],
                'sugar': new_values[columns.index('sugars')]
            }
            new_values[columns.index('nutrition_grade')] = calculate_nutri_score(data, moist)
            print(f"New Nutri-Score calculated: {new_values[columns.index('nutrition_grade')]}")
        else:
            print("Nutri-Score relevant fields were not changed. Keeping the original Nutri-Score.")

        # Update the product in the database
        update_query = f"UPDATE Products SET {', '.join(f'{col} = ?' for col in columns[1:])} WHERE barcode_num = ?"
        cursor.execute(update_query, new_values[1:] + [barcode_num])
        conn.commit()
        print(f"Product '{new_values[1]}' updated successfully.")

        # Verify the update
        cursor.execute("SELECT * FROM Products WHERE barcode_num = ?", (barcode_num,))
        updated_product = cursor.fetchone()
        print("\nUpdated product information:")
        for i, value in enumerate(updated_product):
            print(f"{columns[i]}: {value}")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()
            
def delete_product():
    """Delete a product from the database using product name or barcode number."""
    conn = sqlite3.connect(PRODUCT_DB_PATH)
    cursor = conn.cursor()

    # Ask user for deletion method
    delete_method = input("Delete by (1) Product Name or (2) Barcode Number? Enter 1 or 2: ")

    if delete_method == "1":
        product_name = input("Enter the product name to delete: ")
        cursor.execute("DELETE FROM Products WHERE product_name = ?", (product_name,))
    elif delete_method == "2":
        barcode_num = input("Enter the barcode number to delete: ")
        cursor.execute("DELETE FROM Products WHERE barcode_num = ?", (barcode_num,))
    else:
        print("Invalid option. Please enter 1 or 2.")
        conn.close()
        return

    if cursor.rowcount > 0:
        conn.commit()
        print(f"Product deleted successfully. {cursor.rowcount} row(s) affected.")
    else:
        print("No product found with the given information.")

    conn.close()

def display_filters():
    print("\nSelect one or more filter options (comma-separated):")
    print("1. Low Carbohydrates")
    print("2. High Proteins")
    print("3. Low Sugars")
    print("4. Low Sodium (Salt)")
    print("5. Low Fat")
    print("6. Low Saturated Fat")
    print("7. Dairy-Free")
    print("8. Wheat-Free")
    print("9. Nut-Free")
    print("10. Soy-Free")
    print("11. Sulphite-Free")
    
    # Allow multiple options to be selected
    options = input("\nChoose filters by entering their numbers (comma-separated): ").strip().split(',')

    sugar_threshold = 5  # Low sugar threshold
    sodium_threshold = 0.1  # Low sodium threshold
    fat_threshold = 3  # Low fat threshold
    sat_fat_threshold = 1.5  # Low saturated fat threshold

    # Fetch all products from the database
    products = get_all_products()

    filtered_products = []

    for product in products:
        allergens = product[15].lower()  # Allergens are in the 16th column, stored in uppercase, so convert to lowercase
        match = True

        for option in options:
            option = option.strip()  # Remove any extra spaces

            # Apply filters based on user selection
            if option == '1' and product[6] > 10:  # Low Carbohydrates
                match = False
            elif option == '2' and product[5] <= 10:  # High Proteins
                match = False
            elif option == '3' and product[8] > sugar_threshold:  # Low Sugars
                match = False
            elif option == '4' and product[12] > sodium_threshold:  # Low Sodium
                match = False
            elif option == '5' and product[9] > fat_threshold:  # Low Fat
                match = False
            elif option == '6' and product[10] > sat_fat_threshold:  # Low Saturated Fat
                match = False
            elif option == '7' and 'milk' in allergens:  # Dairy-Free
                match = False
            elif option == '8' and 'wheat' in allergens:  # Wheat-Free
                match = False
            elif option == '9' and ('nut' in allergens or 'peanut' in allergens):  # Nut-Free
                match = False
            elif option == '10' and 'soya' in allergens:  # Soy-Free
                match = False
            elif option == '11' and 'sulphite' in allergens:  # Sulphite-Free
                match = False

        if match:
            filtered_products.append(product)
    
    # Display filtered products and their warnings based on nutritional thresholds
    if filtered_products:
        for prod in filtered_products:
            print("\n--- Product ---")
            print(f"Product Name: {prod[2]}")
            print(f"Barcode: {prod[1]}")
            display_product_warnings(prod)
    else:
        print("No products match your filter.")

def get_all_products():
    """Fetch all products from the database."""
    conn = sqlite3.connect(PRODUCT_DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM Products")
        products = cursor.fetchall()
        return products
    except sqlite3.Error as e:
        print("Database error:", e)
        return []
    finally:
        conn.close()

def display_product_warnings(product):
    """Displays warnings based on nutritional values and includes nutrition grade."""
    sugars = product[8]
    sodium = product[12]
    proteins = product[5]
    energy_kcal = product[4]
    fats = product[9]
    saturated_fat = product[10]
    nutrition_grade = product[16]  # Nutrition Grade is in the 17th column

    print(f"\n📊 Nutrition Grade: {nutrition_grade}")

    if sugars > 22.5:
        print("\n⚠️ WARNING: This product is high in sugar!")
    elif sugars <= 5:
        print("\n🍎 NOTE: This product is low in sugar!")

    if sodium > 0.6:
        print("\n⚠️ WARNING: This product is high in sodium!")
    elif sodium <= 0.1:
        print("\n🥗 NOTE: This product is low in sodium!")

    if energy_kcal > 0:
        protein_energy_percentage = (proteins * 4 / energy_kcal) * 100
        if protein_energy_percentage >= 20:
            print("\n💪 NOTE: This product is high in protein!")

    if fats > 17.5:
        print("\n🍔 WARNING: This product is high in total fat!")
    elif fats < 0.5:
        print("\n🥬 NOTE: This product is fat-free!")
    elif fats < 3:
        print("\n🥗 NOTE: This product is low in fat!")

    if saturated_fat > 5:
        print("\n🥓 WARNING: This product is high in saturated fat!")
    elif saturated_fat < 0.1:
        print("\n🌱 NOTE: This product is free of saturated fat!")
    elif saturated_fat < 1.5:
        print("\n🥑 NOTE: This product is low in saturated fat!")

def view_all_products():
    """View all products and their details in the database."""
    conn = sqlite3.connect(PRODUCT_DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM Products")
        products = cursor.fetchall()
        
        if products:
            print("\n--- All Products in Database ---")
            for product in products:
                print(f"\nBarcode Number: {product[1]}")
                print(f"Product Name: {product[2]}")
                print(f"Ingredients: {product[3]}")
                print(f"Energy (kJ): {product[4]}")
                print(f"Proteins (g): {product[5]}")
                print(f"Carbohydrates (g): {product[6]}")
                print(f"Cholesterol (g): {product[7]}")
                print(f"Sugars (g): {product[8]}")
                print(f"Total Fat (g): {product[9]}")
                print(f"Saturated Fat (g): {product[10]}")
                print(f"Trans Fat (g): {product[11]}")
                print(f"Sodium (mg): {product[12]}")
                print(f"Fruits, Vegetables, Nuts Percentage: {product[13]}")
                print(f"Dietary Fibre (g): {product[14]}")
                print(f"Allergens: {product[15]}")
                print(f"Nutrition Grade: {product[16]}")  # Display nutrition grade
                print(f"Calcium (mg): {product[17]}")
                print(f"Iodine (mg): {product[18]}")
                print(f"Zinc (mg): {product[19]}")
                print(f"Phosphorous (mg): {product[20]}")
                print(f"Magnesium (mg): {product[21]}")
                print(f"Vitamin A (µg): {product[22]}")
                print(f"Vitamin B (µg): {product[23]}")
                print(f"Vitamin C (mg): {product[24]}")
                print(f"Vitamin D (µg): {product[25]}")
                print(f"Vitamin E (mg): {product[26]}")
                print(f"Vitamin K (µg): {product[27]}")
                print(f"Other Nutrients: {product[28]}")
                print("------------------------------")
        else:
            print("No products found in the database.")
    except sqlite3.Error as e:
        print("Database error:", e)
    finally:
        conn.close()

def log_out():
    """Handle the logout process with confirmation."""
    confirmation = input("Are you sure you want to log out? (yes/no): ").lower()
    if confirmation == "yes":
        print("Logging out...")
        menu()  # Return to the main menu after logging out
    else:
        print("Logout canceled.")

def menu():
    """Display the main menu and handle user input."""
    if not check_db_validity():
        print("Databases are not valid. Please fix the issues and try again.")
        return

    while True:
        print("\n--- Main Menu ---")
        print("0: Register")
        print("1: Log In")
        print("2: Quit Application")
        
        try:
            choice = int(input("Select an option: "))
            if choice == 0:
                fields = ["username", "password", "email", "phone_number"]
                reg = Register(*fields)
                reg.register_user()
            elif choice == 1:
                username = input("Enter username: ")
                password = getpass("Enter password: ")
                login = Login(username, password)
                login.authenticate()
            elif choice == 2:
                print("Quitting application.")
                break
            else:
                print("Invalid option. Please select a valid option.")
        except ValueError:
            print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    menu()  # Start the programs