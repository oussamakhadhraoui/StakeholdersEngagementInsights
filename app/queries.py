BAR_CHART_1 = """
WITH TimeGrouped AS (
    SELECT
        CASE 
            WHEN :time_interval = 'daily' THEN DATE(time.Date)
            WHEN :time_interval = 'weekly' THEN STR_TO_DATE(CONCAT(YEAR(time.Date), WEEK(time.Date), ' Sunday'), '%X%V %W')
            WHEN :time_interval = 'monthly' THEN STR_TO_DATE(CONCAT(YEAR(time.Date), '-', MONTH(time.Date), '-01'), '%Y-%m-%d')
        END AS GroupedDate,
        meetingtype.Type, 
        affiliation.AffiliationName, 
        COUNT(DISTINCT person.PersonID) AS participants 
    FROM 
        time 
    LEFT JOIN 
        meeting ON time.Date = meeting.StartDate 
    LEFT JOIN 
        attendance ON meeting.MeetingID = attendance.MeetingID 
    LEFT JOIN 
        person ON attendance.PersonID = person.PersonID 
    LEFT JOIN 
        affiliation ON person.AffiliationID = affiliation.AffiliationID 
    LEFT JOIN 
        meetingtype ON meeting.MeetingTypeID = meetingtype.MeetingTypeID
    WHERE
        meetingtype.MeetingTypeID = :meeting_type_id  
    GROUP BY 
        GroupedDate, meetingtype.Type, affiliation.AffiliationName 
    HAVING 
        COUNT(DISTINCT person.PersonID) > 0
)
SELECT
    GroupedDate AS Date,
    Type,
    AffiliationName,
    SUM(participants) AS participants
FROM
    TimeGrouped
GROUP BY
    GroupedDate, Type, AffiliationName
ORDER BY 
    GroupedDate;
"""

MAP_CHART_1 = '''
WITH 
InvitedAffiliations AS (
    SELECT 
        c.Alpha3Code, 
        COUNT(DISTINCT a.AffiliationID) AS InvitedAffiliationCount
    FROM 
        Meeting m
    JOIN 
        Invitation i ON m.MeetingID = i.MeetingID AND i.Status = 'Required'
    JOIN 
        Person p ON i.PersonID = p.PersonID
    LEFT JOIN 
        Affiliation a ON p.AffiliationID = a.AffiliationID
    JOIN 
        Country c ON p.CountryID = c.CountryID
    WHERE 
        m.MeetingTypeID = :meeting_type_id
    GROUP BY 
        c.Alpha3Code
),
AttendedAffiliations AS (
    SELECT 
        c.Alpha3Code, 
        COUNT(DISTINCT a.AffiliationID) AS AttendedAffiliationCount
    FROM 
        Meeting m
    JOIN 
        Attendance at ON m.MeetingID = at.MeetingID
    JOIN 
        Invitation i ON m.MeetingID = i.MeetingID AND i.PersonID = at.PersonID AND i.Status = 'Required'
    JOIN 
        Person p ON at.PersonID = p.PersonID
    LEFT JOIN 
        Affiliation a ON p.AffiliationID = a.AffiliationID
    JOIN 
        Country c ON p.CountryID = c.CountryID
    WHERE 
        m.MeetingTypeID = :meeting_type_id
    GROUP BY 
        c.Alpha3Code
)
SELECT 
    ia.Alpha3Code, 
    ia.InvitedAffiliationCount, 
    COALESCE(CAST(AttendedAffiliationCount AS FLOAT) / NULLIF(InvitedAffiliationCount, 0), 0) * 100 AS AttendanceRate
FROM 
    InvitedAffiliations ia
LEFT JOIN 
    AttendedAffiliations aa ON ia.Alpha3Code = aa.Alpha3Code
ORDER BY 
    AttendanceRate DESC;

'''

BAR_CHART_2 = '''
WITH InvitedPersons AS (
    SELECT
        p.PersonID,
        COALESCE(a.AffiliationName, 'Unknown Affiliation') AS Affiliation
    FROM
        Invitation i
    JOIN
        Person p ON i.PersonID = p.PersonID
    LEFT JOIN
        Affiliation a ON p.AffiliationID = a.AffiliationID
    WHERE
        i.MeetingID = :meeting_id AND i.Status = 'Required'
),
AttendedPersons AS (
    SELECT DISTINCT
        at.PersonID
    FROM
        Attendance at
    WHERE
        at.MeetingID = :meeting_id
),
AttendanceStatus AS (
    SELECT
        ip.PersonID,
        ip.Affiliation,
        CASE 
            WHEN ap.PersonID IS NOT NULL THEN 'Attended'
            ELSE 'Absent'
        END AS Status
    FROM
        InvitedPersons ip
    LEFT JOIN
        AttendedPersons ap ON ip.PersonID = ap.PersonID
)
SELECT
    Affiliation,
    SUM(CASE WHEN Status = 'Attended' THEN 1 ELSE 0 END) AS Attended,
    SUM(CASE WHEN Status = 'Absent' THEN 1 ELSE 0 END) AS Absent
FROM
    AttendanceStatus
GROUP BY
    Affiliation;

'''

BAR_CHART_2 = '''
WITH InvitedPersons AS (
    SELECT
        p.PersonID,
        COALESCE(a.AffiliationName, 'Unknown Affiliation') AS Affiliation
    FROM
        Invitation i
    JOIN
        Person p ON i.PersonID = p.PersonID
    LEFT JOIN
        Affiliation a ON p.AffiliationID = a.AffiliationID
    WHERE
        i.MeetingID = :meeting_id AND i.Status = 'Required'
),
AttendedPersons AS (
    SELECT DISTINCT
        at.PersonID
    FROM
        Attendance at
    WHERE
        at.MeetingID = :meeting_id
),
AttendanceStatus AS (
    SELECT
        ip.PersonID,
        ip.Affiliation,
        CASE 
            WHEN ap.PersonID IS NOT NULL THEN 'Attended'
            ELSE 'Absent'
        END AS Status
    FROM
        InvitedPersons ip
    LEFT JOIN
        AttendedPersons ap ON ip.PersonID = ap.PersonID
)
SELECT
    Affiliation,
    SUM(CASE WHEN Status = 'Attended' THEN 1 ELSE 0 END) AS Attended,
    SUM(CASE WHEN Status = 'Absent' THEN 1 ELSE 0 END) AS Absent
FROM
    AttendanceStatus
GROUP BY
    Affiliation;

'''

CARD_CHART = '''
WITH InvitedPersons AS (
    SELECT
        p.PersonID,
        COALESCE(a.AffiliationName, 'Unknown Affiliation') AS Affiliation
    FROM
        Invitation i
    JOIN
        Person p ON i.PersonID = p.PersonID
    LEFT JOIN
        Affiliation a ON p.AffiliationID = a.AffiliationID
    WHERE
        i.MeetingID = :meeting_id AND i.Status = 'Required'
),
AttendedPersons AS (
    SELECT DISTINCT
        at.PersonID
    FROM
        Attendance at
    WHERE
        at.MeetingID = :meeting_id
),
AttendanceStatus AS (
    SELECT
        ip.PersonID,
        ip.Affiliation,
        CASE 
            WHEN ap.PersonID IS NOT NULL THEN 'Attended'
            ELSE 'Absent'
        END AS Status
    FROM
        InvitedPersons ip
    LEFT JOIN
        AttendedPersons ap ON ip.PersonID = ap.PersonID
)
SELECT
    (SELECT COUNT(*) FROM InvitedPersons) - (SELECT COUNT(*) FROM AttendedPersons) AS TotalAbsent,
    (SELECT COUNT(*) FROM AttendedPersons) AS TotalAttended,
    (SELECT COUNT(DISTINCT Affiliation) FROM AttendanceStatus WHERE Status = 'Attended' AND Affiliation != 'Unknown Affiliation') AS UniqueAffiliations,
    (SELECT COUNT(*) FROM AttendedPersons) * 100.0 / (SELECT COUNT(*) FROM InvitedPersons) AS PresencePercentage
'''

