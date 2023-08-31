import pandas as pd
from app import db 
import csv
import os
import re
from datetime import timedelta
from app.models import Country, Person, Affiliation


def extract_affiliation(affiliation_str):
    if pd.isnull(affiliation_str) or not isinstance(affiliation_str, str):
        return []

    return [affiliation_str]



def extract_name_and_email(cell):
    if pd.isnull(cell):
        return '', '', ''
    
    email_pattern = r'\((.*?)\)'
    email_match = re.search(email_pattern, str(cell))
    
    if email_match:
        email = email_match.group(1)
    else:
        email = cell

    name_parts = cell.split(' ')[0:-1] if email_match else email.split('@')[0].split('.')
    first_name_index = next((i for i, part in enumerate(name_parts) if not part.isupper()), None)

    if first_name_index is not None:
        last_name = ' '.join(name_parts[:first_name_index])
        first_name = ' '.join(name_parts[first_name_index:first_name_index + 1])
    else:
        last_name = ''
        first_name = ''

    # Check if last_name is missing and the email contains a '.' before the '@'
    if not last_name and '.' in email.split('@')[0]:
        full_name_from_email = re.sub(r'\d', '', email.split('@')[0]) 
        first_name, last_name = full_name_from_email.split('.', 1)
        first_name = first_name.capitalize()
        last_name = last_name.capitalize()

    return first_name, last_name, email



def get_country_id_from_phone_prefix(phone_prefix):
    if len(phone_prefix) == 0:
        return None
    country = Country.query.filter_by(phone_prefix=phone_prefix).first()
    

    if country:
        return country.id
    return get_country_id_from_phone_prefix(phone_prefix[:-1])




def extract_country_id(phone):
    if pd.isnull(phone) or not isinstance(phone, str):
        return None

    # Keep only the digits from the phone number
    digits_only = ''.join(filter(str.isdigit, phone))
    
    # Consider the first 3 digits as the phone prefix
    phone_prefix = digits_only[:3]
    

    # Get the CountryID using the phone_prefix
    country_id = get_country_id_from_phone_prefix(phone_prefix)

    return country_id








def detect_delimiter(csv_path):
    with open(csv_path, 'r', encoding='cp1252') as f:
        line = f.readline()
        sniffer = csv.Sniffer()
        delimiter = sniffer.sniff(line).delimiter
        return delimiter

def transform_persons(csv_path):
    # Detect the delimiter used in the CSV file
    delimiter = detect_delimiter(csv_path)
    
    df = pd.read_csv(csv_path, sep=delimiter, encoding='cp1252')

    persons = []

    affiliation_column_index = 6  # Column index for affiliation 
    phone_column_index = 40       # Column index for phone number 
    full_name_email_column_index = 50 # Column index for full name and email 

    # Now check if we have the required number of columns.
    # If not, it's possible that the wrong delimiter was detected or that the CSV is not structured as expected.
    if df.shape[1] <= max(affiliation_column_index, phone_column_index, full_name_email_column_index):
        raise ValueError("CSV does not have the expected number of columns.")


    for index, row in df.iterrows():
     full_name_cell = row[full_name_email_column_index]
     affiliation_str = row[affiliation_column_index]
     phone = row[phone_column_index]
     first_name, last_name, email = extract_name_and_email(full_name_cell)
     affiliations = extract_affiliation(affiliation_str)

     # If affiliations list is empty, append an empty string to ensure the loop runs once
     if not affiliations:
         affiliations.append('')

     for affiliation_name in affiliations:
        person = {
            'AffiliationName': affiliation_name,
            'FirstName': first_name,
            'LastName': last_name,
            'Email': email,
            'Phone': phone,
        }
        persons.append(person)

    # Save the transformed data to a CSV file
    output_csv_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'csv', 'persons.csv')
    output_df = pd.DataFrame(persons)
    columns = ['AffiliationName', 'FirstName', 'LastName', 'Email', 'Phone']
    output_df = output_df[columns]
    output_df.to_csv(output_csv_path, index=False)


def create_or_get_person(first_name, last_name, email, phone, affiliation_id, country_id, manager_id=None):
    if pd.isna(phone): 
        phone = None

    if pd.isna(last_name): 
        last_name = None

    
    if not manager_id:
        manager_id = None
        
    person = Person.get_by_email(email)
    if person is None:
        person = Person(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address=None,  
            affiliation_id=affiliation_id,
            country_id=country_id,
            manager_id=manager_id
        )
        db.session.add(person)

    return person.person_id







def create_or_get_affiliation(affiliation_str, parent_affiliation_id=None, parent_affiliation_name=None):
    if not isinstance(affiliation_str, str) or pd.isna(affiliation_str):
        return None

    affiliations = affiliation_str.split('/')
    if not affiliations:
        return None

    # Take the first affiliation from the list
    affiliation_name = affiliations[0]

    # Creating a unique ID by concatenating the current affiliation name with the parent's name
    affiliation_id = f"{affiliation_name}{parent_affiliation_name}" if parent_affiliation_name else affiliation_name

    affiliation = Affiliation.query.filter_by(affiliation_id=affiliation_id).first()

    # Check if affiliation already exists, and if not, add it
    if affiliation is None:
        affiliation = Affiliation(
            affiliation_id=affiliation_id,
            affiliation_name=affiliation_name,
            parent_affiliation_id=parent_affiliation_id if parent_affiliation_id else None,
            parent_affiliation_name=parent_affiliation_name if parent_affiliation_name else None
        )
        db.session.add(affiliation)

    # If there are more affiliations in the list, call the function recursively
    if len(affiliations) > 1:
        return create_or_get_affiliation('/'.join(affiliations[1:]), affiliation_id, affiliation_name)
    else:
        return affiliation_id  # Return the ID of the latest affiliation






def person_to_db():
    input_csv_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'csv', 'persons.csv')

    df = pd.read_csv(input_csv_path)

    invalid_people = []  # List to store people with invalid data

    for index, row in df.iterrows():
        first_name = row['FirstName']
        last_name = row['LastName']
        email = row['Email']
        phone = row['Phone']
        affiliation_name = row['AffiliationName']

        # Ignore lines with only affiliation filled
        if pd.isnull(first_name) and pd.isnull(last_name) and pd.isnull(email) and pd.isnull(phone) and not pd.isnull(affiliation_name):
          continue

        # Ignore lines where the email does not contain '@'
        if email and "@" not in email:
          continue

        # Skip if any required data is missing
        if pd.isna(email) or not isinstance(email, str) or not first_name or not last_name:
            invalid_people.append({
                'FirstName': first_name,
                'LastName': last_name
            })
            continue

        # If there is an affiliation, create or get it
        latest_affiliation_id = create_or_get_affiliation(affiliation_name) if isinstance(affiliation_name, str) else None

        # Create or get the person
        country_id = extract_country_id(phone)
        person_id = create_or_get_person(first_name, last_name, email, phone, latest_affiliation_id, country_id, invalid_people)

    
    db.session.commit()

    # Print the invalid people data for testing
    if invalid_people:
     print("Invalid People:")
     for person_id in invalid_people:
        person = Person.query.get(person_id) # Get person by ID
        if person:
            print(f"First Name: {person.first_name}, Last Name: {person.last_name}, Email: {person.email}")



    # You can also return the invalid_people list if needed
    return invalid_people
