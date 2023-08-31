import os   
import pandas as pd
from datetime import datetime, timedelta
from app.models import Person, Meeting, Attendance, Role, MeetingType
from app import db
import re 





def extract_names(full_name_from_row, email):
    name_parts = full_name_from_row.split(" ")
    first_name_index = next((i for i, part in enumerate(name_parts) if not part.isupper()), None)
    
    if first_name_index is not None:
        last_name = ' '.join(name_parts[:first_name_index])
        first_name = ' '.join(name_parts[first_name_index:first_name_index + 1])
    else:
        last_name = ''
        first_name = ''

    # If last_name or first_name is missing, try to extract from email
    if not last_name or not first_name:
        if isinstance(email, str) and '@' in email:
            full_name_from_email = re.sub(r'\d', '', email.split('@')[0])
            if '.' in full_name_from_email:
                first_name_from_email, last_name_from_email = full_name_from_email.split('.', 1)
                first_name = first_name_from_email.capitalize() if not first_name else first_name
                last_name = last_name_from_email.capitalize() if not last_name else last_name

    return last_name, first_name



def process_attendance_row(df, row_number, start_date, start_time, end_date, end_time, meeting_title):
    full_name_from_row = df.loc[row_number, 0].strip()  # Column A
    email = df.loc[row_number, 4]                      # Column E
    role = df.loc[row_number, 6]                       # Column G
    attendance_duration = df.loc[row_number, 3]        # Column D

    last_name, first_name = extract_names(full_name_from_row, email)

    return {
        'StartDate': start_date,
        'StartTime': start_time,
        'EndDate': end_date,
        'EndTime': end_time,
        'Title': meeting_title,
        'FirstName': first_name,
        'LastName': last_name,
        'Email': email,
        'AttendanceDuration': attendance_duration,
        'Role': role
    }




def transform_attendance(csv_path):
    # Read the file line by line and split fields by a tab or at least two spaces
    lines = []
    with open(csv_path, encoding='utf-16') as f:
        for line in f:
            fields = re.split(r'\t| {2,}', line.strip())
            lines.append(fields)

    # Convert the lines into a DataFrame
    df = pd.DataFrame(lines)

    meeting_title = df.loc[1, 1]
    start_date, start_time = df.loc[3, 1].split(", ")
    end_date, end_time = df.loc[4, 1].split(", ")

    transformed_data = []

    # Find the row number of the first blank row (with all cells empty or whitespace only) after row 10
    blank_row = df.loc[10:].index[df.loc[10:].apply(lambda x: all(isinstance(y, str) and y.strip() == '' or pd.isnull(y) for y in x), axis=1)].tolist()
    
    # If there's no blank row found, continue to the end
    last_row = blank_row[0] if blank_row else len(df)

    # Start iterating from row 11 (0-indexed) to the blank row (or the end)
    for row_number, row_data in df.loc[10:last_row-1].iterrows():
        transformed_data.append(process_attendance_row(df, row_number, start_date, start_time, end_date, end_time, meeting_title))

    # Save the transformed data to a CSV file
    output_csv_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'csv', 'attendance.csv')
    output_df = pd.DataFrame(transformed_data)
    columns = ['StartDate', 'StartTime', 'EndDate', 'EndTime', 'Title', 'FirstName', 'LastName', 'Email', 'AttendanceDuration', 'Role']
    output_df = output_df[columns]
    output_df.to_csv(output_csv_path, index=False)


def parse_duration(duration_str):
    hours = 0
    minutes = 0
    seconds = 0

    # Extract hours if present
    if 'h' in duration_str:
        hours = int(duration_str.split('h')[0].strip())

    # Extract minutes if present
    if 'm' in duration_str:
        minutes_part = duration_str.split('h')[1] if 'h' in duration_str else duration_str
        minutes = int(minutes_part.split('m')[0].strip())

    # Extract seconds if present
    if 's' in duration_str:
        seconds_part = duration_str.split('m')[1] if 'm' in duration_str else duration_str
        seconds = int(seconds_part.split('s')[0].strip())

    return timedelta(hours=hours, minutes=minutes, seconds=seconds)



def handle_invalid_person(row, invalid_people):
    invalid_people.append({
        'FirstName': row['FirstName'],
        'LastName': row['LastName'],
        'Email': row['Email']  
    })


def create_or_get_person(first_name, last_name, email, invalid_people):
    # Check if Person already exists
    person = Person.get_by_email(email)
    if person is None:
        # If Person does not exist, create a new Person
        # Check if there are missing fields
        if not all([first_name, last_name, email]):
            invalid_people.append({'first_name': first_name, 'last_name': last_name, 'email': email})
        person = Person(
            first_name=first_name, 
            last_name=last_name, 
            email=email,
            phone=None, 
            address=None, 
            affiliation_id=None, 
            country_id=None
        )
        db.session.add(person)
        db.session.commit()
    return person


def extract_meeting_type_from_title(title):
    type_matches = re.findall(r'\[(.*?)\]', title)
    return ' '.join(type_matches).strip()

def create_or_get_meeting_type(type_name):
    # Check if MeetingType already exists
    meeting_type = MeetingType.query.filter_by(type=type_name).first()
    if meeting_type is None:
        # If MeetingType does not exist, create a new MeetingType
        meeting_type = MeetingType(type=type_name)
        db.session.add(meeting_type)
        db.session.commit()
    return meeting_type

def create_or_get_meeting(row):
    # Extract meeting type from title
    type_name = extract_meeting_type_from_title(row['Title'])
    meeting_type = create_or_get_meeting_type(type_name)
    
    # Adjust the title to exclude the meeting type
    actual_title = re.sub(r'\[.*?\]', '', row['Title']).strip()

    # Create or get the Meeting
    meeting = Meeting.query.filter_by(title=actual_title).first()
    if meeting is None:
        meeting = Meeting(
            type_id=meeting_type.id,
            start_date=datetime.strptime(row['StartDate'].strip(','), "%m/%d/%y").date(),
            start_time=datetime.strptime(row['StartTime'], "%I:%M:%S %p").time(),
            end_date=datetime.strptime(row['EndDate'].strip(','), "%m/%d/%y").date(),
            end_time=datetime.strptime(row['EndTime'], "%I:%M:%S %p").time(),
            location='Teams',
            title=actual_title
        )
        db.session.add(meeting)
        db.session.commit()
    return meeting


def create_or_get_role(role_name):
    # Get or create the Role
    role = Role.query.filter_by(role_name=role_name).first()
    if role is None:
        role = Role(role_name=role_name)
        db.session.add(role)
        db.session.commit()
    return role

def attendance_to_db():
    input_csv_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'csv', 'attendance.csv')
    df = pd.read_csv(input_csv_path)

    invalid_people = []  # List to store people with invalid data

    for index, row in df.iterrows():
        email = row['Email'] if not pd.isna(row['Email']) else ""
        first_name = row['FirstName'] if not pd.isna(row['FirstName']) else ""
        last_name = row['LastName'] if not pd.isna(row['LastName']) else ""

        # If any of these details are missing or not a string type, add to invalid_people list and continue.
        if not all([isinstance(email, str), isinstance(first_name, str), isinstance(last_name, str), email.strip(), first_name.strip(), last_name.strip()]):
            handle_invalid_person(row, invalid_people)
            continue

        person = create_or_get_person(first_name, last_name, email, invalid_people)
        meeting = create_or_get_meeting(row)
        attendance_duration = parse_duration(row['AttendanceDuration'])

        # Check if an attendance record already exists for the given person and meeting
        existing_attendance = Attendance.query.filter_by(person_id=person.person_id, meeting_id=meeting.id).first()
        if not existing_attendance:
            attendance = Attendance(person_id=person.person_id, meeting_id=meeting.id, attendance_duration=attendance_duration)
            db.session.add(attendance)
            db.session.commit()
        else:
            # Optionally, update the existing attendance record if needed
            existing_attendance.attendance_duration = attendance_duration
            db.session.commit()

        role_name = row['Role']
        create_or_get_role(role_name)
        
    # Print the invalid people data for testing
    if invalid_people:
        print("Invalid People:")
        for person in invalid_people:
            print(f"First Name: {person['FirstName']}, Last Name: {person['LastName']}, Email: {person['Email']}")

    return invalid_people
