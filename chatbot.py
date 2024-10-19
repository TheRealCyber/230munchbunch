import random
import spacy

print("ChatBot Prototype 2")
# Load the spaCy model
nlp = spacy.load('en_core_web_sm')

# Sample data structure
health_data = {
    "diet_type": {
        "eggetarian": "You follow an eggetarian diet.",
        "vegetarian": "You follow a vegetarian diet.",
        "non-vegetarian": "You follow a non-vegetarian diet.",
        "jain": "You follow a Jain diet."
    },
    "chronic_illnesses": {
        "diabetes": "Managing diabetes requires monitoring your carbohydrate intake.",
        "hypertension": "For hypertension, focus on low-sodium foods."
    },
    "dietary_restrictions": {
        "lactose_intolerance": "Avoid dairy products.",
        "gluten_free": "Avoid wheat and barley."
    },
    "health_goals": {
        "bp_control": "For blood pressure control, consider reducing salt intake.",
        "sugar_control": "Monitor your sugar intake."
    }
}

# Function to get response based on user input
def chatbot_response(user_input):
    tokens = nlp(user_input.lower())
    response = "I'm sorry, I didn't understand that."
    
    # Check for diet type
    if any(token.text in ['diet', 'vegetarian', 'non-vegetarian', 'eggetarian', 'jain'] for token in tokens):
        response = random.choice(list(health_data['diet_type'].values()))
    
    # Check for chronic illnesses
    elif any(token.text in ['diabetes', 'hypertension'] for token in tokens):
        response = random.choice(list(health_data['chronic_illnesses'].values()))
    
    # Check for dietary restrictions
    elif any(token.text in ['lactose', 'gluten'] for token in tokens):
        response = random.choice(list(health_data['dietary_restrictions'].values()))
    
    # Check for health goals
    elif any(token.text in ['blood pressure', 'sugar'] for token in tokens):
        response = random.choice(list(health_data['health_goals'].values()))

    return response

# Example interaction
while True:
    user_input = input("You: ")
    if user_input.lower() in ['exit', 'quit']:
        print("Chatbot: Goodbye!")
        break
    print("Chatbot:", chatbot_response(user_input))
