import requests
import uuid  # For generating virtual user IDs

# Your OSINT API Key
OSINT_API_KEY = 'enter your key'
BASE_URL = 'https://api.osint.industries/v1/search'

# Create a session object to store cookies
session = requests.Session()

# Function to create a virtual user ID and device ID
def generate_user_data():
    user_uuid = str(uuid.uuid4())  # Generate a new UUID for the user (Virtual ID)
    device_id = str(uuid.uuid4())  # Generate a new UUID for the device (Device ID)
    return {
        'virtual_id': user_uuid,
        'device_id': device_id
    }

# Function to make API requests with cookies, user agent, and device ID
def osint_search(query_type, query_value, device_id):
    headers = {
        'Authorization': f'Bearer {OSINT_API_KEY}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'X-Device-ID': device_id  # Custom header to send device ID
    }
    params = {
        'type': query_type,
        'term': query_value
    }
    try:
        response = session.get(BASE_URL, headers=headers, params=params)  # Use session for cookies
        response.raise_for_status()  # Ensure we catch HTTP errors
        return response.json()  # Return the JSON response
    except requests.exceptions.HTTPError as err:
        if response.status_code == 451:
            return {'error': 'Unavailable For Legal Reasons'}
        else:
            return {'error': str(err)}
    except Exception as e:
        return {'error': f'Unknown error: {str(e)}'}

# Main function to handle user input
def main():
    print("Welcome to the OSINT Search CLI!")
    user_data = generate_user_data()
    print(f"Your Virtual ID: {user_data['virtual_id']}")
    print(f"Your Device ID: {user_data['device_id']}\n")
    
    print("Please select a search option:")
    print("1. Search by username")
    print("2. Search by email")
    print("3. Search by phone number")

    option = input("Enter the option number (1, 2, or 3): ")

    if option == '1':
        query_type = 'username'
        query_value = input("Enter the username to search: ")
    elif option == '2':
        query_type = 'email'
        query_value = input("Enter the email to search: ")
    elif option == '3':
        query_type = 'phone'
        query_value = input("Enter the phone number to search: ")
    else:
        print("Invalid option. Exiting.")
        return

    # Make the API request
    result = osint_search(query_type, query_value, user_data['device_id'])

    # Check and display the results
    if 'error' in result:
        print(f"Error: {result['error']}")
    elif result.get('data'):
        print(f"Search Results for {query_value}:")
        print(result['data'])
        if 'image_url' in result['data']:
            print(f"Image URL: {result['data']['image_url']}")
        else:
            print("No image available for this result.")
    else:
        print(f"No details found for {query_value}.")

if __name__ == "__main__":
    main()
