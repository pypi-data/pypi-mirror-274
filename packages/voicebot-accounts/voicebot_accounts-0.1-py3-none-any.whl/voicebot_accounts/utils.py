from datetime import timedelta
import datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def get_event(creds):
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """

  try:
    service = build("calendar", "v3", credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.now().isoformat() + 'Z'  # 'c' indicates UTC time
    five_days = datetime.datetime.now() + timedelta(days=5)
    #now = datetime.datetime.now
   
    print("Getting the upcoming 10 events")
    '''events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])'''

    calendar_user = service.calendarList().list().execute()
    timeZone = calendar_user['items'][1]['timeZone']
    print("TimeZzone : ", timeZone)
    calendar_id = calendar_user['items'][1]['id']

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    result = service.events().list(calendarId='primary', timeMin=now,
                                          # timeZone='GMT-04:00',
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()

    events = []
    for event in result['items']:
      dic = {}
      # print(event)
      if 'summary' in event.keys():
          dic['id'] = event['id']
          dic['summary'] = event['summary']
          dic['start'] = event['start']
          dic['end'] = event['end']
          events.append(dic)

    if not events:
      print("No upcoming events found.")
      return

    # Prints the start and name of the next 10 events
    for event in events:
      start = event["start"].get("dateTime", event["start"].get("date"))
      end  = event["end"].get("dateTime", event["end"].get("date"))
      print(start, end, event["summary"])
    
    return events

  except HttpError as error:
    print(f"An error occurred: {error}")

def schedule_event(event, creds):

  try:
    service = build("calendar", "v3", credentials=creds)
    created_event = service.events().insert(calendarId="primary", body=event).execute()
    print(f"Created event: {created_event['id']}")
    return "Event Created"
  except Exception as e:
    return ("Error Occured " + str(e))

def reschedule_event(meeting_id, new_start_time, new_end_time, creds):
  service = build("calendar", "v3", credentials=creds)
  event = service.events().get(calendarId='primary', eventId=meeting_id).execute()
  event['start']['dateTime'] = new_start_time
  event['end']['dateTime'] = new_end_time

  # Update the eventz
  updated_event = service.events().update(calendarId='primary', eventId=meeting_id, body=event).execute()

  print('Event updated:', updated_event)


def cancel_event(meeting_id, creds):
  service = build("calendar", "v3", credentials=creds)
  service.events().delete(calendarId="primary", eventId=meeting_id).execute()
  print(f"Deleted event: {meeting_id}")
