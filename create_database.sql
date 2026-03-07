CREATE DATABASE ecocleanup;

-- Create enum type first
-- CREATE TYPE user_role AS ENUM ('customer', 'staff', 'admin');

-- CREATE TABLE users (
--   user_id SERIAL PRIMARY KEY,
--   username VARCHAR(20) NOT NULL UNIQUE,
--   password_hash TEXT NOT NULL,
--   email VARCHAR(320) NOT NULL,
--   person_role user_role NOT NULL
-- );
CREATE TYPE role_enum AS ENUM ('volunteer', 'event_leader', 'admin');
CREATE TYPE status_enum AS ENUM ('active','inactive');
CREATE TYPE attendance AS ENUM ('registered', 'attended', 'no_show');


CREATE TABLE users(
user_id SERIAL PRIMARY KEY,
username VARCHAR(50) UNIQUE NOT NULL,
password_hash TEXT NOT NULL,
full_name VARCHAR(100),
email VARCHAR(100),
contact_number VARCHAR(20),
home_address VARCHAR(255),
profile_image VARCHAR(255),
environmental_interests VARCHAR(255),
role role_enum  NOT NULL,
status status_enum NOT NULL DEFAULT 'active',
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE events(
event_id SERIAL PRIMARY KEY,
event_name VARCHAR(100),
event_leader_id INTEGER REFERENCES users(user_id),
location VARCHAR(255),
event_type VARCHAR(50),
event_date DATE,
start_time TIME,
end_time TIME,
duration INTEGER,
description TEXT,
supplies TEXT,
safety_instructions TEXT,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE eventregistrations(
registration_id SERIAL PRIMARY KEY,
event_id INTEGER REFERENCES events(event_id),
volunteer_id INTEGER REFERENCES users(user_id),
attendance VARCHAR(20) DEFAULT 'registered',
registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE feedback (
feedback_id SERIAL PRIMARY KEY,
event_id INTEGER REFERENCES events(event_id) ON DELETE CASCADE,
volunteer_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
rating INTEGER CHECK (rating >= 1 AND rating <= 5),
comments TEXT,
submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
UNIQUE(event_id, volunteer_id)
);


CREATE TABLE eventoutcomes(
outcome_id SERIAL PRIMARY KEY,
event_id INTEGER REFERENCES events(event_id),
num_attendees INTEGER,
bags_collected INTEGER,
recyclables_sorted INTEGER,
other_achievements TEXT,
recorded_by INTEGER REFERENCES users(user_id),
recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);