import os   
import pandas as pd
from datetime import datetime, timedelta
from app.models import PersonTestCSV, MeetingTestCSV, AttendanceTestCSV, Role
from app import db



def transform_attendance(csv_path):
    transformed_data = []
    in_attendance_part = False

    with open(csv_path, newline='', encoding='utf16') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        for line_number, row in enumerate(reader):
            if line_number == 1:
                meeting_title = row[1]
            elif line_number == 3:
                start_date, start_time = row[1].split(", ")
            elif line_number == 4:
                end_date, end_time = row[1].split(", ")
            elif line_number == 8:
                in_attendance_part = True
            elif line_number >= 10:
                if row[0].strip() == "":
                    in_attendance_part = False
                if row[0].strip() == "3. Activités en réunion":
                    break
                if in_attendance_part:
                    email = row[4]
                    full_name_from_row = row[0].strip()
                    role = row[6]
                    name_parts = full_name_from_row.split(" ")
                    
                    first_name_index = next((i for i, part in enumerate(name_parts) if not part.isupper()), None)
                    if first_name_index is not None:
                        last_name = ' '.join(name_parts[:first_name_index])
                        first_name = ' '.join(name_parts[first_name_index:first_name_index + 1])
                    else:
                        last_name = ''
                        first_name = ''

                    if email.count('.') > 1 and '@' in email:
                        full_name_from_email = email.split('@')[0].rsplit('.', 1)[0]
                        if '.' in full_name_from_email:
                            first_name_from_email, last_name_from_email = full_name_from_email.split('.', 1)
                            if last_name_from_email.lower() in full_name_from_row.lower() and first_name_from_email.lower() in full_name_from_row.lower():
                                first_name = first_name_from_email.capitalize()
                                last_name = last_name_from_email.capitalize()

                    attendance_duration = row[3]
                    transformed_data.append({
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
                    })

    output_csv_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'csv', 'attendance.csv')
    df = pd.DataFrame(transformed_data)
    columns = ['StartDate', 'StartTime', 'EndDate', 'EndTime', 'Title', 'FirstName', 'LastName', 'Email', 'AttendanceDuration', 'Role']
    df = df[columns]
    df.to_csv(output_csv_path, index=False)

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



def attendance_to_db():
    input_csv_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'csv', 'attendance.csv')
    df = pd.read_csv(input_csv_path)
    
    invalid_people = []  # List to store people with invalid data

    # Iterate through the rows in the DataFrame
    for index, row in df.iterrows():
        first_name = row['FirstName']
        last_name = row['LastName']
        email = row['Email']

        # Handle the case where email is NaN or missing
        if pd.isna(email) or not isinstance(email, str):
            invalid_people.append(row)
            continue  # Skip this iteration

        # If first name or last name is missing, try to extract from email
        if (pd.isna(first_name) or pd.isna(last_name)) and '@' in email and '.' in email.split('@')[0]:
            email_local_part = email.split('@')[0]
            first_name, last_name = email_local_part.split('.', 1)

        # If still missing, add to invalid people list
        if pd.isna(first_name) or pd.isna(last_name) or pd.isna(email) or '@' not in email:
            invalid_people.append(row)
            continue  # Skip this iteration

        # Check if Person already exists
        person = PersonTestCSV.query.filter_by(email=email).first()
        if person is None:
          # If Person does not exist, create a new Person
          person = PersonTestCSV(first_name=first_name, last_name=last_name, email=email)
          db.session.add(person)
          db.session.commit()



        # Create or get the Meeting
        meeting = MeetingTestCSV.query.filter_by(title=row['Title']).first()
        if meeting is None:
            meeting = MeetingTestCSV(
                start_date=datetime.strptime(row['StartDate'].strip(','), "%m/%d/%y").date(),
                start_time=datetime.strptime(row['StartTime'], "%I:%M:%S %p").time(),
                end_date=datetime.strptime(row['EndDate'].strip(','), "%m/%d/%y").date(),
                end_time=datetime.strptime(row['EndTime'], "%I:%M:%S %p").time(),
                title=row['Title']
            )
            db.session.add(meeting)
            db.session.commit()

        # Parse the attendance duration
        attendance_duration = parse_duration(row['AttendanceDuration'])

        # Create the Attendance
        attendance = AttendanceTestCSV(person_id=person.id, meeting_id=meeting.id, attendance_duration=attendance_duration)
        db.session.add(attendance)
        db.session.commit()


        # Get or create the Role
        role_name = row['Role']  # Assuming you have 'Role' column in your CSV file
        role = Role.query.filter_by(role_name=role_name).first()
        if role is None:
          role = Role(role_name=role_name)
          db.session.add(role)
          db.session.commit()



    # Print the invalid people data for testing
    if invalid_people:
        print("Invalid People:")
        for person in invalid_people:
          print(f"First Name: {person['FirstName']}, Last Name: {person['LastName']}")

    # You can also return the invalid_people list if needed
    return invalid_people


