# agenticScheduler

This is ageneticScheduler project


## Contributing

To contribute:
1. Create a new branch for your feature or bug fix.
2. Commit your changes with clear and descriptive messages.
3. Open a Pull Request (PR) against the main branch, detailing the changes you've made.

## Development Environment Setup

The following tools are required for development:
*   Visual Studio Code
*   Google Code assist
*   Langchain
*   Langraph

![image](https://github.com/user-attachments/assets/55c11d13-14f6-42c8-abc8-3f4a19ec578b)



# Smart Email-Based Meeting Scheduler

*Requirements \& System Design*

## 1. Overview

Develop an intelligent agent, **@smart_scheduler**, that automates meeting scheduling from within ongoing email conversations. The agent leverages calendar integrations (e.g., Google Calendar) and email parsing to streamline coordination among participants, minimizing manual effort and optimizing for availability.

---

## 2. Key Features

- **Email Thread Detection and Participant Identification**
    - Detect invocation when a registered user includes `@smart_scheduler` in an email thread.
    - Extract all participants from the email’s recipient list (To, Cc, Bcc as appropriate).
    - Register new users as needed, or prompt for registration if unregistered participants are detected.
- **Calendar Integration**
    - Sync with Person A’s (initiator’s) Google Calendar to fetch available time slots.
    - Optionally, support calendar integration for other participants if they are registered.
- **Scheduling Initiation**
    - Upon invocation, send an initiation email to all thread participants, proposing available time slots.
    - Allow recipients to reply with their preferred times or integrate with their calendars for automated availability sharing.
- **Time Slot Selection and Confirmation**
    - Parse responses for suggested times.
    - Use an algorithm to select the optimal time slot based on initiator’s availability and participants’ preferences.
    - Send a meeting invitation to all participants, including `@smart_scheduler` as an attendee for tracking and auditing.
- **Meeting Invitation and Tracking**
    - Add `@smart_scheduler` to the meeting invite as an attendee or include a unique identifier in the invite body for tracking.
    - Monitor the event for changes or cancellations up to 24 hours before the meeting.
    - If changes or cancellations occur, automatically restart the scheduling process, with a configurable limit (X) on rescheduling attempts.
- **Change Monitoring and Rescheduling**
    - Poll or subscribe to calendar updates to detect changes or cancellations.
    - Notify participants of any changes and restart the scheduling process if needed, respecting the maximum reschedule limit.
- **User Experience Enhancements**
    - Provide clear email templates for initiation, confirmation, and rescheduling.
    - Support natural language parsing for flexible user replies (e.g., “I’m free after 2pm”).
    - Allow configuration of working hours, time zones, and meeting duration preferences.

---

## 3. System Architecture

- **Email Listener/Parser:** Monitors inboxes for `@smart_scheduler` mentions and parses email threads.
- **User Directory \& Registration:** Manages user profiles, registration status, and calendar integration tokens.
- **Calendar API Integration:** Interfaces with Google Calendar (and optionally others) to fetch and update events.
- **Scheduling Engine:** Core logic for proposing, negotiating, and finalizing meeting times.
- **Notification Service:** Handles all outgoing emails and calendar invites.
- **Monitoring \& Rescheduling Module:** Tracks meeting status and triggers rescheduling workflows as needed.
- **Configuration Management:** Allows customization of rescheduling limits, working hours, and notification preferences.

---


**End of Document**
