import re
from datetime import datetime
import csv

def extract_user_data(sql_file):
    user_countries = {}  # user_id -> country_code
    user_details = {}    # user_id -> {email, name, join_date}
    
    print("Starting data extraction...")
    
    with open(sql_file, 'r') as f:
        for line in f:
            # Extract country codes
            if 'user_country_code' in line:
                matches = re.findall(r'\((\d+),(\d+),\'user_country_code\',\'([A-Z]{2})\'\)', line)
                for match in matches:
                    user_id = match[1]
                    country_code = match[2]
                    user_countries[user_id] = country_code
            
            # Extract user details (email, name, join date)
            if 'INSERT INTO `wp_users`' in line:
                details_matches = re.findall(r'\((\d+),\'[^\']*\',\'[^\']*\',\'[^\']*\',\'([^\']*)\',\'[^\']*\',\'([^\']*)\',', line)
                for match in details_matches:
                    user_id = match[0]
                    email = match[1]
                    join_date = match[2]
                    name = email.split('@')[0]  # Extract name from email
                    user_details[user_id] = {
                        'email': email,
                        'name': name,
                        'join_date': join_date
                    }

    print(f"Found {len(user_countries)} users with country codes")
    print(f"Found {len(user_details)} user details")

    # Combine the data
    combined_data = []
    for user_id in user_details:
        if user_id in user_countries:
            data = user_details[user_id]
            data['country_code'] = user_countries[user_id]
            combined_data.append(data)

    print(f"Successfully matched {len(combined_data)} users with their country codes")
    return combined_data

# Extract and export data
print("Starting extraction process...")
data = extract_user_data('sqlfile.sql')

# Export to CSV
output_file = 'complete_user_data.csv'
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['name', 'email', 'join_date', 'country_code'])
    writer.writeheader()
    writer.writerows(data)

print(f"\nExported {len(data)} entries to {output_file}")
print("\nSample of first 5 entries:")
for entry in data[:5]:
    print(f"Name: {entry['name']}, Email: {entry['email']}, Joined: {entry['join_date']}, Country: {entry['country_code']}")