from flask import Blueprint, render_template, request, make_response
from app.models.meeting import Meeting
from app.models.meetingtype import MeetingType
from flask import jsonify
from app import db
import csv
import re
from datetime import datetime
import pandas as pd
import os

meeting_api_bp = Blueprint('meeting_api', __name__, url_prefix='/api/v1/meetings')

@meeting_api_bp.route('/', methods=['POST', 'OPTIONS'])
def create():
        data = request.get_json()
        new_meeting = Meeting(
            type_id=data['MeetingTypeID'],
            start_date=data['StartDate'],
            start_time=data['StartTime'],
            end_date=data['EndDate'],
            end_time=data['EndTime'],
            location=data['Location'],
            title=data['Title']  
        )   
        db.session.add(new_meeting)
        db.session.commit()
        return jsonify({'message': 'Meeting created'}), 201



@meeting_api_bp.route('/', methods=['GET'])
def index():
    meetings = Meeting.query.all()
    return jsonify({'items': [meeting.to_dict() for meeting in meetings]}), 200

@meeting_api_bp.route('/<int:id>', methods=['GET'])
def show(id):
    meeting = Meeting.get_by_id(id)
    if meeting:
        return jsonify(meeting.to_dict()), 200
    else:
        return jsonify({'message': 'Meeting not found'}), 404

@meeting_api_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
def update(id):
    data = request.get_json()
    meeting = Meeting.get_by_id(id)
    if meeting:
        meeting.update({
            'type_id': data.get('MeetingTypeID'),
            'start_date': data.get('StartDate'),
            'start_time': data.get('StartTime'),
            'end_date': data.get('EndDate'),
            'end_time': data.get('EndTime'),
            'location': data.get('Location'),
            'title': data.get('Title'),  
        })
        db.session.commit()
        return jsonify({'message': 'Meeting updated'}), 200
    else:
        return jsonify({'message': 'Meeting not found'}), 404

@meeting_api_bp.route('/<int:id>', methods=['DELETE'])
def delete(id):
    meeting = Meeting.get_by_id(id)
    if meeting:
        db.session.delete(meeting)
        db.session.commit()
        return jsonify({'message': 'Meeting deleted'}), 200
    else:
        return jsonify({'message': 'Meeting not found'}), 404
    

def transform_data(csv_path):

    script_dir = os.path.dirname(os.path.realpath(__file__))
    project_root = os.path.join(script_dir, '..', '..')
    output_csv_path = os.path.join(project_root, 'csv', 'meetings.csv')

    pattern = re.compile(r'\[(.+?)\] \[(.+?)\] (.+?),(.+?),(.+?),(.+?),(.+?),')
    transformed_data = []

    with open(csv_path, newline='', encoding='ansi') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            line = ','.join(row)
            match = pattern.match(line)
            if match:
                type_parts = [match.group(1), match.group(2)]
                meeting_type_str = ', '.join(type_parts)
                
                title = match.group(3)
                start_date = datetime.strptime(match.group(4), "%d/%m/%Y").date()
                start_time = datetime.strptime(match.group(5), "%H:%M:%S").time()
                end_date = datetime.strptime(match.group(6), "%d/%m/%Y").date()
                end_time = datetime.strptime(match.group(7), "%H:%M:%S").time()
                location = "Teams"

                transformed_data.append({
                    'MeetingType': meeting_type_str,
                    'Title': title,
                    'StartDate': start_date,
                    'StartTime': start_time,
                    'EndDate': end_date,
                    'EndTime': end_time,
                    'Location': location
                })

    df = pd.DataFrame(transformed_data)
    columns = ['MeetingType', 'Title', 'StartDate', 'StartTime', 'EndDate', 'EndTime', 'Location']
    df = df[columns]
    df.to_csv(output_csv_path, index=False)


def extract_meeting_type(row):
    meeting_type_str = row['MeetingType']
    meeting_type_parts = meeting_type_str.split(", ")
    title = row['Title']
    meeting_type_parts = [part for part in meeting_type_parts if part != title]
    meeting_type_str = ', '.join(meeting_type_parts)
    return meeting_type_str, title


def csv_to_db():
    # Read the CSV file
    script_dir = os.path.dirname(os.path.realpath(__file__))
    project_root = os.path.join(script_dir, '..', '..')
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

        # Create a Meeting with the appropriate MeetingType ID
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

