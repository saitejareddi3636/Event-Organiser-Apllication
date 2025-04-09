Sprint Review Document
Summary of Accomplishments
Group Contributions
Sprint Goal
User Stories Completed:

Implemented the Favorite Events feature.
Developed the base for event creation and management.
Technical Work:
Set up database operations for the storage of events.

Users can add, view, and mark events as favorite
The core functionality of event management and favorites is up and running.
Work Done:
Core functionality of managing events and favorites is operational.
Got the base ready to extend more in upcoming sprints.
Challenges Faced:
Initial issues were ensuring that the favorite feature worked without performance or UI hiccups.

Limited time to expand beyond base event management system.

Database integration and error handling at the database and sharing functionality level to ensure seamless integration between those features.

Managed edge cases for invalid usernames or sharing of the same event multiple times.

Next Steps:
Event search and filtering are planned for the next sprint.

Improve the UI design of the event manager; make it more interactive.
Add the functionality to edit or delete an event, among others.
Enhance the functionality of the Share feature by allowing notifications when events are shared with any recipient.
Improve usability when event sharing with email or other forms of external mechanisms.
Share Feature:
Backend Integration:

Added a new table called shared_events in the database, which will store who shared an event with whom and what event was shared; this allows for easy data exchange between users.
UI Implementation:
Added "Share" button in event manager. Users can share an event by selecting it, writing the recipient's username, and pressing the share button.
View Shared Events:
Implemented a feature to view all events shared with a user without much effort or hassle to shared received event details.
Notification Feature:
Feature Overview:

Firebase Cloud Messaging - FCM added to implement real-time event notifications.
Users are reminded of upcoming events in due time right on their devices.
Work Done:
Notification System

Integrated FCM to enable event notifications.
Notify users in advance of an upcoming event.
General Improvements:
Enhanced UI/UX to make things flow better.
Ensured seamless integrations with the app's event management system.
