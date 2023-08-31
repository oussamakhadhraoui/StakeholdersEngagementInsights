import csv
import pandas as pd
import chardet
import re
import os
from datetime import datetime
import io
from app.models import Meeting, MeetingType, Invitation, Person
from app import db

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

def detect_delimiter(file_path, encoding):
    with open(file_path, 'r', encoding=encoding) as f:
        line = f.readline()
        comma_count = line.count(',')
        semicolon_count = line.count(';')
        return ',' if comma_count > semicolon_count else ';'

def read_custom_csv(csv_path, encoding):
    with open(csv_path, 'r', encoding=encoding) as f:
        content = f.read()

    # Replace two consecutive double quotes with a single double quote
    content = content.replace('""', '"')

    # Split the content by lines
    lines = content.split("\n")

    adjusted_lines = []
    temp_line = ""
    inside_quotes = False

    for line in lines:
        if not inside_quotes and line.startswith('"'):
            inside_quotes = True
            temp_line = line
        elif inside_quotes and line.endswith('"'):
            inside_quotes = False
            temp_line += " " + line
            adjusted_lines.append(temp_line)
            temp_line = ""
        elif inside_quotes:
            temp_line += " " + line
        else:
            adjusted_lines.append(line)

    # If we're still inside quotes at the end, there's a problem with the CSV
    if inside_quotes:
        print(f"Warning: Unmatched quotation mark in line: {temp_line}")

    adjusted_content = "\n".join(adjusted_lines)

    return adjusted_content




def transform_meeting(csv_path):
    encoding = detect_encoding(csv_path)
    delimiter = detect_delimiter(csv_path, encoding)

    script_dir = os.path.dirname(os.path.realpath(__file__))
    project_root = os.path.join(script_dir, '..')
    output_csv_path = os.path.join(project_root, 'csv', 'meetings.csv')

    transformed_data = []

    adjusted_csv_content = read_custom_csv(csv_path, encoding)
    df = pd.read_csv(io.StringIO(adjusted_csv_content), delimiter=delimiter, quotechar='"', doublequote=True)

    for _, row in df.iterrows():
        # Skip rows where the first column isn't a string
        if not isinstance(row[0], str):
            continue
        if row[0].startswith("Annulé:") or row[0].startswith("Cancelled:"):
            continue

        full_string = row[0].strip()

        # Check for brackets
        bracket_pattern = re.compile(r'\[(.*?)\]')
        bracket_matches = bracket_pattern.findall(full_string)

        if bracket_matches:
            meeting_type = ', '.join(bracket_matches)
            title = bracket_pattern.sub('', full_string).strip()
        else:
            meeting_type = "Unknown"
            title = full_string
        # Check if date and time values are strings before parsing
        if isinstance(row[1], str) and isinstance(row[2], str) and isinstance(row[3], str) and isinstance(row[4], str):
            try:
                start_date = datetime.strptime(row[1], "%d/%m/%Y").date()
                start_time = datetime.strptime(row[2], "%H:%M:%S").time()
                end_date = datetime.strptime(row[3], "%d/%m/%Y").date()
                end_time = datetime.strptime(row[4], "%H:%M:%S").time()
            except ValueError:
                continue  # skip this row due to incorrect date/time format
        else:
            # Handle rows with missing or unexpected date/time values
            continue  # skip this row

        location = "Teams"
        organiser = row[9] if isinstance(row[9], str) else ""
        required = row[10] if isinstance(row[10], str) else ""
        optional = row[11] if isinstance(row[11], str) else ""

        transformed_data.append({
            'MeetingType': meeting_type,
            'Title': title,
            'StartDate': start_date,
            'StartTime': start_time,
            'EndDate': end_date,
            'EndTime': end_time,
            'Location': location,
            'Organiser': organiser,
            'Required': required,
            'Optional': optional
        })

    df_transformed = pd.DataFrame(transformed_data)
    columns = ['MeetingType', 'Title', 'StartDate', 'StartTime', 'EndDate', 'EndTime', 'Location', 'Organiser', 'Required', 'Optional']
    df_transformed = df_transformed[columns]
    df_transformed.to_csv(output_csv_path, index=False)






def extract_meeting_type(row):
    meeting_type_str = row['MeetingType']
    meeting_type_parts = meeting_type_str.split(", ")
    title = row['Title']
    meeting_type_parts = [part for part in meeting_type_parts if part != title]
    meeting_type_str = ', '.join(meeting_type_parts)
    return meeting_type_str, title

def parse_name(name_str):
    name_parts = name_str.split()

    # Start with the last part as the company
    company_parts = [name_parts[-1]]
    index = -2

    # Iterate from the end to the start
    while index >= -len(name_parts):
        part = name_parts[index]

        # Check if the part is the start of the first name
        if re.match(r'^[A-Z][a-z]', part):
            break

        company_parts.insert(0, part)
        index -= 1

    first_name_parts = name_parts[index:-len(company_parts)]
    last_name_parts = name_parts[:index]

    return {
        'last_name': ' '.join(last_name_parts),
        'first_name': ' '.join(first_name_parts),
        'company': ' '.join(company_parts)
    }



def get_person_by_name(first_name, last_name):
    return Person.get_by_name(first_name, last_name)

def create_or_get_invitation(meeting_id, person_id, role_id, status):
    invitation = Invitation.query.filter_by(meeting_id=meeting_id, person_id=person_id, role_id=role_id, status=status).first()
    if not invitation:
        invitation = Invitation(meeting_id=meeting_id, person_id=person_id, role_id=role_id, status=status)
        db.session.add(invitation)
        db.session.commit()
    return invitation

def meeting_to_db():
    # Read the CSV file
    script_dir = os.path.dirname(os.path.realpath(__file__))
    project_root = os.path.join(script_dir, '..')
    input_csv_path = os.path.join(project_root, 'csv', 'meetings.csv')
    df = pd.read_csv(input_csv_path)

    # Iterate through the rows in the DataFrame (back to front)
    for index, row in df.iloc[::-1].iterrows():
        # Extract MeetingType and Title
        meeting_type_name, title = extract_meeting_type(row)

        # Get or create the MeetingType
        meeting_type = MeetingType.query.filter_by(type=meeting_type_name).first()
        if meeting_type is None:
            meeting_type = MeetingType(type=meeting_type_name)
            db.session.add(meeting_type)
            db.session.commit()

        # Check if a meeting with the same attributes already exists
        existing_meeting = Meeting.query.filter_by(
            type_id=meeting_type.id,
            start_date=datetime.strptime(row['StartDate'], "%Y-%m-%d").date(),
            start_time=datetime.strptime(row['StartTime'], "%H:%M:%S").time(),
            end_date=datetime.strptime(row['EndDate'], "%Y-%m-%d").date(),
            end_time=datetime.strptime(row['EndTime'], "%H:%M:%S").time(),
            location=row['Location'],
            title=title
        ).first()

        if not existing_meeting:
            meeting = Meeting(
                type_id=meeting_type.id,
                start_date=datetime.strptime(row['StartDate'], "%Y-%m-%d").date(),
                start_time=datetime.strptime(row['StartTime'], "%H:%M:%S").time(),
                end_date=datetime.strptime(row['EndDate'], "%Y-%m-%d").date(),
                end_time=datetime.strptime(row['EndTime'], "%H:%M:%S").time(),
                location=row['Location'],
                title=title
            )
            db.session.add(meeting)
            db.session.commit()
        else:
            meeting = existing_meeting

        # Handle Organiser, Required, and Optional
        for role_id, (column_name, status) in zip([11, 13, 13], [('Organiser', 'Required'), ('Required', 'Required'), ('Optional', 'Optional')]):
            people_str = row[column_name]
            if pd.notna(people_str):
                for person_str in people_str.split(';'):
                    parsed_name = parse_name(person_str)
                    first_name = parsed_name['first_name']
                    last_name = parsed_name['last_name'] 
                    person = get_person_by_name(first_name, last_name)

                    if person:  # Only proceed if the person exists
                        create_or_get_invitation(meeting.id, person.person_id, role_id, status)

