def fetch_food_info(barcode):
    # Open Food Facts API URL
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    
    # Send a GET request to the API
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response as JSON
        product_data = response.json()
        
        # Check if the product was found
        if product_data['status'] == 1:
            # Extract relevant information
            product = product_data['product']
            product_name = product.get('product_name', 'No product name available')
            brand = product.get('brands', 'No brand available')
            categories = product.get('categories', 'No categories available')
            ingredients = product.get('ingredients_text', 'No ingredients available')
            nutrition_grades = product.get('nutriscore_grade', 'No nutrition grade available')
            allergens = product.get('allergens', 'No allergens listed')
            countries = product.get('countries_tags', [])
            countries_list = ', '.join(countries) if countries else 'No countries listed'

            # Display the product information
            print(f"Product Name: {product_name}")
            print(f"Brand: {brand}")
            print(f"Categories: {categories}")
            print(f"Ingredients: {ingredients}")
            print(f"Nutrition Grade: {nutrition_grades.upper()}")
            print(f"Allergens: {allergens}")
            print(f"Available in Countries: {countries_list}")
        else:
            print("Product not found in the database.")
    else:
        print(f"Failed to fetch data (Status code: {response.status_code})")

# Ask the user for the barcode
barcode = input("Enter the barcode: ")

# Fetch and display the food information
fetch_food_info(barcode)

#examples
#3017620429484
#7622210449283
#030000001070
#737628064502