# EcoCleanUp Hub - Community Cleanup Management System

## Project Overview

EcoCleanUp Hub is a web-based platform developed for GreenSteps Initiative. The system helps coordinate community cleanup events by connecting volunteers with event leaders and providing administrators with oversight capabilities. 

---

## Technology Stack

**Backend:** Python 3.13, Flask  
**Database:** PostgreSQL  
**Frontend:** Bootstrap 5, HTML, Jinja2 templates  
**Authentication:** Flask-Bcrypt for password hashing  
**Deployment:** PythonAnywhere  

---

## User Roles & Features

### Volunteer

- Browse and filter upcoming cleanup events (by date, location, type)
- Register for events with scheduling conflict detection
- View participation history
- Submit feedback (rating 1–5 + comments)
- Manage personal profile

### Event Leader

- Create new events (name, location, date, time, duration, supplies, safety instructions)
- Manage existing events (edit, cancel)
- View volunteers registered for events
- Track volunteer attendance
- Record event outcomes (attendees, rubbish bags collected, recyclables sorted)
- Review volunteer feedback
- Generate event reports

### Admin

- Manage users (view, search, filter by role/status)
- Activate/deactivate user accounts
- View platform-wide statistics
- Generate comprehensive reports
- Oversee all events and users

---

## Database Design

The database follows the ERD provided in the assignment specification, with the following main tables:

- **users** – Stores all user accounts with role-based access  
- **events** – Cleanup event details  
- **eventregistrations** – Tracks volunteer registrations  
- **feedback** – Stores volunteer feedback and ratings  
- **eventoutcomes** – Records event results (bags collected, recyclables sorted, etc.)

---

## Test Accounts

| Role | Username | Password |
|-----|-----|-----|
| Volunteer | oliver_smith | Olivermith639/ |
| Volunteer | ethan_lee | Ethanlee639/ |
| Event Leader | staff_liam | Liampatel639/ |
| Event Leader | staff_sophie | Sophiewilliams639/ |
| Admin | admin_julia | Adminjulia639/ |
| Admin | admin_michael | Adminmichael639/ |

**Note:** All test accounts have hashed passwords stored in the database for security.

---


## Security Features

- Passwords hashed using Flask_Bcrypt
- Session-based authentication
- Role-based access control
- Input validation on all forms
- SQL injection prevention via parameterized queries

---

## GenAI Usage Acknowledgement

In accordance with COMP639 assessment guidelines, I acknowledge the use of Generative AI tools in the development of this project.

### Tools Used

ChatGPT – Primary AI assistant used throughout development (February 18 - March 7, 2026).

### How AI Was Used

#### 1. Code Debugging & Troubleshooting (Feb 20 ~ Mar 7, 2026)

- Diagnosed database query errors
- Resolved Flask routing issues 
- Fixed template inheritance and variable scope issues
- Debugged datetime parsing errors in event creation forms

#### 2. Database Assistance (Feb 19-22, 2026)

- Helped create realistic user data 
- Generated sample event descriptions with appropriate supplies and safety instructions
- Created feedback data with varied ratings and realistic comments

#### 3. UI/UX Improvements (Feb 19 ~ Mar 4, 2026)

- Suggested Bootstrap classes for responsive layouts
- Helped design consistent card layouts across user roles
- Improved color scheme and visual hierarchy
- Optimized button placement and sizing for different screen sizes

#### 4. Report & Analytics Design (Feb 25 ~ Mar 5, 2026)

- Designed admin report pages with meaningful statistics
- Designed data presentation for event outcomes and volunteer participation
- Designed summary cards for platform metrics

#### 5. Code Optimization (Feb 23 ~ Mar 6, 2026)

- Refactored repetitive code into reusable functions
- Improved error handling and validation messages

### Example Prompts Used

- "Generate 20 realistic volunteer names and email addresses for test data"
- "Help me design a responsive event card layout with Bootstrap"
- "What's the best way to structure admin analytics dashboard?"
- "Debug this SQL query with subquery returning multiple columns"
- "Why is my database table 'eventregistrations' not found even though I created it?"
- "How to fix 'Could not build url for endpoint 'volunteer.volunteer_events'' error in Flask?"
- "How do I make Bootstrap buttons the same width in a button group?"
- "Why is my Jinja template showing 'now is undefined' error?"
- "Why does my foreign key constraint fail when inserting data?"
- "How to display user profile images in Flask with default fallback?"
- "How to fix 'ValueError: invalid salt' when checking password hash?"
- "How to structure admin dashboard with multiple statistics cards in Bootstrap?"
- "Why is my subquery returning multiple columns error in PostgreSQL?"
- "How to implement event registration with time conflict check?"
- "How to filter events by date, location and type in SQL query?"
- "How to make Flask session remember user login across pages?"
- "How to create a responsive table that scrolls on mobile devices?"

---

## Deployment on PythonAnywhere

The application is hosted on PythonAnywhere.

To deploy your own instance:

1. Create a PythonAnywhere account
2. Set up a web app with manual configuration
3. Clone your GitHub repository
4. Create and configure the virtual environment
5. Configure database
6. Create database tables and insert data
7. Configure WSGI file
8. Click the green Reload button on Web tab 

---

## Author

Michael Yin  
Student ID: **1171117**

GitHub: Michael-Yin-1171117  
Project Repository: **EcoCleanUp**

---

## Acknowledgements

- Course coordinator and teaching staff for the project specifications
- Flask and Bootstrap communities for excellent documentation
- ChatGPT for assistance with debugging and design suggestions

---

© 2026 EcoCleanUp - Community Cleanup Management System