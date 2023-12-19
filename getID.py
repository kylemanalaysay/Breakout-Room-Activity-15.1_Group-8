import requests

# Replace 'YOUR_ACCESS_TOKEN' with your actual access token
access_token = 'MzdhMTQyY2ItZDhjYi00N2JmLTg0NzEtNjg2YjlkMWM1NjRjZjRiYWNkNTYtNWE4_P0A1_d0b19fc5-a717-4064-90e2-8d88b3acad9c'

headers = {
    'Authorization': f'Bearer {access_token}'
}

# Make a GET request to list spaces
response = requests.get('https://api.ciscospark.com/v1/rooms', headers=headers)

if response.status_code == 200:
    spaces = response.json()['items']
    for space in spaces:
        print(f"Space Name: {space['title']}, Space ID: {space['id']}")
else:
    print("Failed to fetch spaces")
