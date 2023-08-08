import sys
sys.path.append('C:\\Users\\o.khadhraoui\\StakeholdersEngagementInsights')

from app import create_app, db
from app.Attendance_csv import attendance_to_db

# Create the Flask app and set up the app context
app = create_app()
app.app_context().push()

# Call the function
attendance_to_db()
