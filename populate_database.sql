
--DELETE FROM feedback;        
--DELETE FROM eventregistrations;  
--DELETE FROM eventoutcomes;   
--DELETE FROM events;
--DELETE FROM users;

INSERT INTO users (username,password_hash,full_name,email,contact_number,home_address,environmental_interests,role)
VALUES
-- ADMINS
('admin_julia','$2b$12$C6UzMDM.H6dfI/f/IKcEeO8sVZySUdkGFUTkOcJCIZy9FHn5Vf3.e','Julia Thompson','julia.thompson@email.com','021-445-872','12 Queen Street, Auckland','policy, sustainability','admin'),
('admin_michael','$2b$12$C6UzMDM.H6dfI/f/IKcEeO8sVZySUdkGFUTkOcJCIZy9FHn5Vf3.e','Michael Chen','michael.chen@email.com','022-118-993','8 Albert Road, Auckland','climate action','admin'),

-- EVENT LEADERS
('staff_sophie','$2b$12$C6UzMDM.H6dfI/f/IKcEeO8sVZySUdkGFUTkOcJCIZy9FHn5Vf3.e','Sophie Williams','sophie.w@email.com','021-778-912','45 Lake Rd, Takapuna','marine conservation','event_leader'),
('staff_liam','$2b$12$C6UzMDM.H6dfI/f/IKcEeO8sVZySUdkGFUTkOcJCIZy9FHn5Vf3.e','Liam Patel','liam.p@email.com','027-661-204','18 King St, Hamilton','tree planting','event_leader'),
('staff_aria','$2b$12$C6UzMDM.H6dfI/f/IKcEeO8sVZySUdkGFUTkOcJCIZy9FHn5Vf3.e','Aria Ngatai','aria.n@email.com','021-901-772','9 Moana Ave, Tauranga','wildlife protection','event_leader'),
('staff_noah','$2b$12$C6UzMDM.H6dfI/f/IKcEeO8sVZySUdkGFUTkOcJCIZy9FHn5Vf3.e','Noah Robinson','noah.r@email.com','022-557-113','76 Hillcrest Rd, Rotorua','river cleanup','event_leader'),
('staff_emma','$2b$12$C6UzMDM.H6dfI/f/IKcEeO8sVZySUdkGFUTkOcJCIZy9FHn5Vf3.e','Emma Garcia','emma.g@email.com','020-887-665','33 Park Lane, Wellington','community gardens','event_leader'),

-- VOLUNTEERS (20)
('oliver_smith','$2b$12$C6UzMDM.H6dfI/f/IKcEeO8sVZySUdkGFUTkOcJCIZy9FHn5Vf3.e','Oliver Smith','oliver.s@email.com','021-882-001','14 Green Rd, Auckland','recycling','volunteer'),
('ava_jones','$2b$12$C6UzMDM.H6dfI/f/IKcEeO8sVZySUdkGFUTkOcJCIZy9FHn5Vf3.e','Ava Jones','ava.j@email.com','021-882-002','88 Coast Rd, Auckland','oceans','volunteer'),
('ethan_lee','$2b$12$C6UzMDM.H6dfI/f/IKcEeO8sVZySUdkGFUTkOcJCIZy9FHn5Vf3.e','Ethan Lee','ethan.l@email.com','021-882-003','9 River St, Hamilton','forests','volunteer'),
('mia_khan','$2b$12$C6UzMDM.H6dfI/f/IKcEeO8sVZySUdkGFUTkOcJCIZy9FHn5Vf3.e','Mia Khan','mia.k@email.com','021-882-004','17 Sunset Blvd, Auckland','wildlife','volunteer'),
('lucas_wilson','$2b$12$C6UzMDM.H6dfI/f/IKcEeO8sVZySUdkGFUTkOcJCIZy9FHn5Vf3.e','Lucas Wilson','lucas.w@email.com','021-882-005','21 Palm Dr, Tauranga','parks','volunteer'),
('isabella_clark','$2b$12$C6UzMDM.H6dfI/f/IKcEeO8sVZySUdkGFUTkOcJCIZy9FHn5Vf3.e','Isabella Clark','isabella.c@email.com','021-882-006','55 Ridge Rd, Napier','sustainability','volunteer'),
('jack_white','$2b$12$C6UzMDM.H6dfI/f/IKcEeO8sVZySUdkGFUTkOcJCIZy9FHn5Vf3.e','Jack White','jack.w@email.com','021-882-007','67 Valley Rd, Dunedin','eco education','volunteer'),
('amelia_hall','$2b$12$C6UzMDM.H6dfI/f/IKcEeO8sVZySUdkGFUTkOcJCIZy9FHn5Vf3.e','Amelia Hall','amelia.h@email.com','021-882-008','3 Ocean View, Nelson','coastal care','volunteer'),
('henry_adams','$2b$12$C6UzMDM.H6dfI/f/IKcEeO8sVZySUdkGFUTkOcJCIZy9FHn5Vf3.e','Henry Adams','henry.a@email.com','021-882-009','29 Beach Rd, Auckland','marine life','volunteer'),
('charlotte_brown','$2b$12$C6UzMDM.H6dfI/f/IKcEeO8sVZySUdkGFUTkOcJCIZy9FHn5Vf3.e','Charlotte Brown','charlotte.b@email.com','021-882-010','11 Hill Rd, Hamilton','trees','volunteer'),
('daniel_scott','$2b$12$C6UzMDM.H6dfI/f/IKcEeO8sVZySUdkGFUTkOcJCIZy9FHn5Vf3.e','Daniel Scott','daniel.s@email.com','021-882-011','42 Park Ave, Wellington','river cleanup','volunteer'),
('harper_turner','$2b$12$C6UzMDM.H6dfI/f/IKcEeO8sVZySUdkGFUTkOcJCIZy9FHn5Vf3.e','Harper Turner','harper.t@email.com','021-882-012','90 Forest Ln, Rotorua','forests','volunteer'),
('sebastian_evans','$2b$12$C6UzMDM.H6dfI/f/IKcEeO8sVZySUdkGFUTkOcJCIZy9FHn5Vf3.e','Sebastian Evans','sebastian.e@email.com','021-882-013','72 Lake Rd, Taupo','wildlife','volunteer'),
('ella_perez','$2b$12$C6UzMDM.H6dfI/f/IKcEeO8sVZySUdkGFUTkOcJCIZy9FHn5Vf3.e','Ella Perez','ella.p@email.com','021-882-014','5 Greenway, Christchurch','climate','volunteer'),
('logan_edwards','$2b$12$C6UzMDM.H6dfI/f/IKcEeO8sVZySUdkGFUTkOcJCIZy9FHn5Vf3.e','Logan Edwards','logan.e@email.com','021-882-015','8 Riverbank, Gisborne','waterways','volunteer'),
('grace_collins','$2b$12$C6UzMDM.H6dfI/f/IKcEeO8sVZySUdkGFUTkOcJCIZy9FHn5Vf3.e','Grace Collins','grace.c@email.com','021-882-016','101 Sunrise Rd, Auckland','urban gardens','volunteer'),
('leo_stewart','$2b$12$C6UzMDM.H6dfI/f/IKcEeO8sVZySUdkGFUTkOcJCIZy9FHn5Vf3.e','Leo Stewart','leo.s@email.com','021-882-017','44 Hilltop Dr, Hamilton','recycling','volunteer'),
('zoe_morris','$2b$12$C6UzMDM.H6dfI/f/IKcEeO8sVZySUdkGFUTkOcJCIZy9FHn5Vf3.e','Zoe Morris','zoe.m@email.com','021-882-018','13 Coastal Rd, Auckland','ocean plastics','volunteer'),
('owen_rogers','$2b$12$C6UzMDM.H6dfI/f/IKcEeO8sVZySUdkGFUTkOcJCIZy9FHn5Vf3.e','Owen Rogers','owen.r@email.com','021-882-019','25 Valley St, Wellington','ecosystems','volunteer'),
('lily_cooper','$2b$12$C6UzMDM.H6dfI/f/IKcEeO8sVZySUdkGFUTkOcJCIZy9FHn5Vf3.e','Lily Cooper','lily.c@email.com','021-882-020','6 Garden Way, Auckland','gardening','volunteer');


--ALTER SEQUENCE events_event_id_seq RESTART WITH 1;
--ALTER SEQUENCE eventregistrations_registration_id_seq RESTART WITH 1;
--ALTER SEQUENCE feedback_feedback_id_seq RESTART WITH 1;
--ALTER SEQUENCE eventoutcomes_outcome_id_seq RESTART WITH 1;

INSERT INTO events (event_name, event_leader_id, location, event_type, event_date, start_time, end_time, duration, description, supplies, safety_instructions)
VALUES
-- past events- event_id 1-20
('Mission Bay Beach Cleanup', 3, 'Mission Bay, Auckland', 'Cleanup', '2025-11-02', '09:00', '12:00', 3, 'Collect litter and plastics from the beach', 'Gloves, rubbish bags, litter pickers, hand sanitizer', 'Wear closed-toe shoes, bring sunscreen and water, stay with your group'),
('Waikato River Restoration', 4, 'Hamilton', 'Restoration', '2025-11-05', '10:00', '13:00', 3, 'Remove debris from riverbank and plant natives', 'Gloves, bags, native plants, tools', 'Watch for slippery banks, wear appropriate footwear, stay away from fast-flowing water'),
('Native Tree Planting', 5, 'Tauranga Reserve', 'Planting', '2025-11-07', '08:30', '11:30', 3, 'Plant native saplings in the reserve', 'Seedlings, spades, gloves, watering cans', 'Long pants recommended, watch for uneven ground, bring insect repellent'),
('Lake Rotorua Care Day', 6, 'Rotorua', 'Cleanup', '2025-11-10', '09:00', '12:00', 3, 'Lake shore cleanup and weed removal', 'Bags, gloves, litter pickers, weed tools', 'Stay with your group, wear sunscreen, be aware of bird nesting areas'),
('Urban Garden Build', 7, 'Wellington', 'Community', '2025-11-12', '11:00', '15:00', 4, 'Build raised beds for community garden', 'Tools, wood, screws, nails, gloves', 'Safety goggles required, closed shoes mandatory, lift with your legs not your back'),
('Coastal Watch Patrol', 3, 'Takapuna Beach', 'Monitoring', '2025-11-14', '07:00', '10:00', 3, 'Wildlife observation and data collection', 'Binoculars, monitoring sheets, pens, snacks', 'Early start, bring warm clothes, stay on designated paths'),
('Forest Trail Maintenance', 4, 'Hamilton Park', 'Maintenance', '2025-11-15', '09:00', '12:00', 3, 'Trail clearing and maintenance', 'Loppers, gloves, safety vests, first aid kit', 'Watch for branches, stay on marked trail, be aware of wildlife'),
('Plastic Audit Workshop', 7, 'Wellington Hall', 'Workshop', '2025-11-18', '13:00', '15:00', 2, 'Waste audit training and sorting', 'Gloves, masks, sorting tables, recording sheets', 'Wear gloves at all times, wash hands after, masks required during sorting'),
('Wetland Habitat Care', 5, 'Tauranga Wetlands', 'Restoration', '2025-11-20', '09:00', '12:00', 3, 'Restore wetland habitat', 'Native plants, gloves, mulch, tools', 'Beware of wet areas, wear gumboots recommended, watch for native wildlife'),
('School Eco Talk', 7, 'Wellington School', 'Education', '2025-11-21', '10:00', '11:30', 2, 'Student environmental awareness session', 'Presentation materials, handouts, activity sheets', 'Standard classroom safety, follow school guidelines'),
('Harbour Cleanup', 3, 'Auckland Harbour', 'Cleanup', '2025-11-22', '09:00', '12:00', 3, 'Remove trash from harbour area', 'Bags, gloves, pickers, boat transport', 'Life jackets provided, must know how to swim, follow boat safety instructions'),
('Park Tree Survey', 4, 'Hamilton Park', 'Survey', '2025-11-24', '10:00', '13:00', 3, 'Count and document native trees', 'Survey sheets, clipboard, pens, tree ID guide', 'Stay on paths, watch for poison ivy, bring water'),
('Wildlife Tracking', 5, 'Tauranga Hills', 'Research', '2025-11-26', '06:30', '10:30', 4, 'Track native wildlife species', 'Tracking equipment, camera, notebook, snacks', 'Early start, bring warm clothes, stay quiet, follow guide at all times'),
('Community Recycling Day', 7, 'Wellington Square', 'Community', '2025-11-28', '09:00', '14:00', 5, 'Sort recyclables and educate public', 'Gloves, sorting bins, information leaflets', 'Wear gloves, wash hands regularly, stay hydrated'),
('Riverbank Planting', 6, 'Rotorua River', 'Planting', '2025-11-29', '08:30', '12:30', 4, 'Plant natives to stabilize riverbanks', 'Native plants, spades, gloves, stakes', 'Stay away from river edge, wear sturdy boots, sun protection required'),
('Ocean Microplastic Study', 3, 'Auckland Coast', 'Research', '2025-12-02', '07:30', '11:30', 4, 'Collect water samples for microplastic analysis', 'Sample bottles, sieves, gloves, coolers', 'Water safety briefing required, wear waders, stay with research team'),
('Eco Film Night', 7, 'Wellington Center', 'Awareness', '2025-12-04', '18:00', '20:00', 2, 'Screening of environmental documentary', 'Seating, projector, snacks, discussion cards', 'Standard venue safety, follow fire exit signs'),
('Community Compost Training', 7, 'Wellington', 'Workshop', '2025-12-06', '10:00', '12:00', 2, 'Teach composting techniques', 'Compost bins, kitchen scraps, handouts', 'Wash hands before and after, wear closed shoes'),
('Nature Walk & Cleanup', 6, 'Rotorua Forest', 'Cleanup', '2025-12-09', '09:00', '12:00', 3, 'Guided nature walk with litter collection', 'Bags, gloves, walking sticks', 'Stay on trail, bring water, wear appropriate footwear'),
('Bird Habitat Build', 5, 'Tauranga Park', 'Conservation', '2025-12-12', '09:00', '13:00', 4, 'Install nesting boxes for native birds', 'Nesting boxes, ladder, tools, gloves', 'Working at heights, safety harness provided, follow instructions carefully'),

-- future events- event_id 21-30
('Summer Beach Cleanup', 3, 'Mission Bay, Auckland', 'Cleanup', '2026-01-15', '09:00', '12:00', 3, 'Summer beach maintenance and litter collection', 'Gloves, bags, pickers, sunscreen', 'Sun protection mandatory, bring water, stay hydrated'),
('River Health Monitoring', 4, 'Hamilton', 'Monitoring', '2026-01-20', '10:00', '13:00', 3, 'Check water quality and river health', 'Testing kits, waders, clipboards', 'Water safety briefing, wear appropriate footwear'),
('Tree Planting Day', 5, 'Tauranga Reserve', 'Planting', '2026-02-01', '08:30', '11:30', 3, 'Plant native species in the reserve', 'Seedlings, spades, gloves, mulch', 'Long pants recommended, bring water, sun protection'),
('Wetland Restoration', 6, 'Rotorua', 'Restoration', '2026-02-10', '09:00', '12:00', 3, 'Wetland care and native planting', 'Native plants, gloves, tools', 'Wear gumboots, be aware of wet areas'),
('Community Garden', 7, 'Wellington', 'Community', '2026-02-15', '11:00', '15:00', 4, 'Expand community garden with new beds', 'Tools, wood, soil, plants', 'Safety goggles, closed shoes, lift safely'),
('Coastal Cleanup', 3, 'Takapuna Beach', 'Cleanup', '2026-02-20', '07:00', '10:00', 3, 'Beach maintenance and litter collection', 'Bags, gloves, pickers', 'Sun protection, bring water, early start'),
('Trail Maintenance', 4, 'Hamilton Park', 'Maintenance', '2026-02-25', '09:00', '12:00', 3, 'Trail work and clearing', 'Tools, gloves, safety vests', 'Stay on trail, watch for hazards'),
('Recycling Workshop', 7, 'Wellington Hall', 'Workshop', '2026-03-01', '13:00', '15:00', 2, 'Recycling education and sorting practice', 'Gloves, sorting bins, samples', 'Wear gloves, wash hands after'),
('Habitat Restoration', 5, 'Tauranga Wetlands', 'Restoration', '2026-03-05', '09:00', '12:00', 3, 'Restore native habitat in wetlands', 'Plants, tools, gloves, mulch', 'Wear gumboots, watch for wet areas'),
('Eco Education Day', 7, 'Wellington School', 'Education', '2026-03-08', '10:00', '11:30', 2, 'School environmental education program', 'Materials, handouts, activities', 'Follow school guidelines');

-- （eventregistrations）
INSERT INTO eventregistrations (event_id, volunteer_id, attendance, registered_at)
VALUES
-- past events (event_id 1-20)
(1, 1, 'attended', '2025-10-15 09:30:00'),
(1, 2, 'attended', '2025-10-15 10:00:00'),
(1, 3, 'attended', '2025-10-16 14:00:00'),
(2, 4, 'attended', '2025-10-18 11:00:00'),
(2, 5, 'no-show', '2025-10-18 11:30:00'),
(3, 6, 'attended', '2025-10-20 08:15:00'),
(3, 7, 'attended', '2025-10-20 08:45:00'),
(4, 8, 'attended', '2025-10-22 13:00:00'),
(4, 9, 'attended', '2025-10-22 13:30:00'),
(5, 10, 'no-show', '2025-10-25 10:00:00'),
(5, 11, 'attended', '2025-10-25 10:30:00'),
(6, 12, 'attended', '2025-10-28 06:30:00'),
(6, 13, 'attended', '2025-10-28 07:00:00'),
(7, 14, 'attended', '2025-10-30 08:30:00'),
(7, 15, 'attended', '2025-10-30 09:00:00'),
(8, 16, 'attended', '2025-11-02 12:15:00'),
(8, 17, 'attended', '2025-11-02 12:45:00'),
(9, 18, 'attended', '2025-11-05 08:30:00'),
(9, 19, 'no-show', '2025-11-05 09:00:00'),
(10, 20, 'attended', '2025-11-08 09:15:00'),
(11, 1, 'attended', '2025-11-10 08:00:00'),
(11, 2, 'attended', '2025-11-10 08:30:00'),
(12, 3, 'attended', '2025-11-12 09:00:00'),
(12, 4, 'attended', '2025-11-12 09:30:00'),
(13, 5, 'attended', '2025-11-15 06:00:00'),
(13, 6, 'attended', '2025-11-15 06:30:00'),
(14, 7, 'attended', '2025-11-18 08:30:00'),
(14, 8, 'attended', '2025-11-18 09:00:00'),
(15, 9, 'attended', '2025-11-20 08:00:00'),
(15, 10, 'attended', '2025-11-20 08:30:00'),
(16, 11, 'attended', '2025-11-22 07:00:00'),
(16, 12, 'attended', '2025-11-22 07:30:00'),
(17, 13, 'attended', '2025-11-25 17:30:00'),
(17, 14, 'attended', '2025-11-25 18:00:00'),
(18, 15, 'attended', '2025-11-28 09:30:00'),
(18, 16, 'attended', '2025-11-28 10:00:00'),
(19, 17, 'attended', '2025-12-01 08:15:00'),
(19, 18, 'no-show', '2025-12-01 08:45:00'),
(20, 19, 'attended', '2025-12-05 08:30:00'),
(20, 20, 'attended', '2025-12-05 09:00:00'),

-- future events (event_id 21-30)
(21, 1, 'registered', CURRENT_TIMESTAMP),
(21, 2, 'registered', CURRENT_TIMESTAMP),
(22, 3, 'registered', CURRENT_TIMESTAMP),
(22, 4, 'registered', CURRENT_TIMESTAMP),
(23, 5, 'registered', CURRENT_TIMESTAMP),
(23, 6, 'registered', CURRENT_TIMESTAMP),
(24, 7, 'registered', CURRENT_TIMESTAMP),
(24, 8, 'registered', CURRENT_TIMESTAMP),
(25, 9, 'registered', CURRENT_TIMESTAMP),
(25, 10, 'registered', CURRENT_TIMESTAMP),
(26, 11, 'registered', CURRENT_TIMESTAMP),
(26, 12, 'registered', CURRENT_TIMESTAMP),
(27, 13, 'registered', CURRENT_TIMESTAMP),
(27, 14, 'registered', CURRENT_TIMESTAMP),
(28, 15, 'registered', CURRENT_TIMESTAMP),
(28, 16, 'registered', CURRENT_TIMESTAMP),
(29, 17, 'registered', CURRENT_TIMESTAMP),
(29, 18, 'registered', CURRENT_TIMESTAMP),
(30, 19, 'registered', CURRENT_TIMESTAMP),
(30, 20, 'registered', CURRENT_TIMESTAMP);

-- 5. feedback
INSERT INTO feedback (event_id, volunteer_id, rating, comments, submitted_at)
VALUES
(1, 1, 5, 'Amazing beach cleanup! We collected over 40 bags of rubbish.', '2025-11-03 15:30:00'),
(1, 2, 4, 'Great event, well organized.', '2025-11-03 16:00:00'),
(1, 3, 5, 'Loved it! Will definitely come again.', '2025-11-03 16:30:00'),
(2, 4, 5, 'The river looks so much better now.', '2025-11-06 14:20:00'),
(3, 6, 5, 'Planted so many trees! Very rewarding.', '2025-11-08 15:45:00'),
(3, 7, 4, 'Great team effort.', '2025-11-08 16:00:00'),
(4, 8, 5, 'Lake is cleaner, saw lots of birds.', '2025-11-11 17:30:00'),
(4, 9, 4, 'Good turnout, well led.', '2025-11-11 18:00:00'),
(5, 11, 5, 'Built 4 raised beds for the community!', '2025-11-13 19:15:00'),
(6, 12, 5, 'Beautiful morning, saw native birds.', '2025-11-15 13:30:00'),
(6, 13, 4, 'Early start but worth it.', '2025-11-15 14:00:00'),
(7, 14, 5, 'Cleared 3km of trail. Great workout!', '2025-11-16 17:45:00'),
(7, 15, 5, 'Trail looks amazing now.', '2025-11-16 18:15:00'),
(8, 16, 5, 'Learned so much about recycling!', '2025-11-19 20:30:00'),
(8, 17, 4, 'Very informative workshop.', '2025-11-19 21:00:00'),
(9, 18, 5, 'Removed weeds and planted natives.', '2025-11-21 16:45:00'),
(10, 20, 5, 'Kids loved it! Great presentation.', '2025-11-22 15:30:00'),
(11, 1, 5, 'Harbour is much cleaner now.', '2025-11-23 14:30:00'),
(11, 2, 4, 'Good organization, nice weather.', '2025-11-23 15:00:00'),
(12, 3, 5, 'Counted over 50 native trees!', '2025-11-25 16:30:00'),
(12, 4, 5, 'Educational and fun.', '2025-11-25 17:00:00'),
(13, 5, 5, 'Tracked 5 different species!', '2025-11-27 12:30:00'),
(13, 6, 4, 'Interesting research project.', '2025-11-27 13:00:00'),
(14, 7, 5, 'Sorted over 75kg of recycling!', '2025-11-29 17:30:00'),
(14, 8, 5, 'Great community turnout.', '2025-11-29 18:00:00'),
(15, 9, 5, 'Riverbank looks beautiful.', '2025-11-30 15:45:00'),
(15, 10, 4, 'Hard work but satisfying.', '2025-11-30 16:15:00'),
(16, 11, 5, 'Important research, collected samples.', '2025-12-03 13:30:00'),
(16, 12, 5, 'Fascinating microplastic study.', '2025-12-03 14:00:00'),
(17, 13, 5, 'Great film, very educational.', '2025-12-05 21:30:00'),
(17, 14, 4, 'Good choice of film.', '2025-12-05 22:00:00'),
(18, 15, 5, 'Learned proper composting techniques.', '2025-12-07 13:30:00'),
(18, 16, 5, 'Very practical workshop.', '2025-12-07 14:00:00'),
(19, 17, 5, 'Beautiful forest, great cleanup.', '2025-12-10 14:45:00'),
(20, 19, 5, 'Installed 5 nesting boxes!', '2025-12-13 15:30:00'),
(20, 20, 5, 'Birds will love these.', '2025-12-13 16:00:00');

-- 6. event outcomes
INSERT INTO eventoutcomes (event_id, num_attendees, bags_collected, recyclables_sorted, other_achievements, recorded_by)
VALUES
(1, 12, 45, 30, 'Beach fully cleared, 3 tyres removed', 3),
(2, 8, 32, 15, 'Riverbank restored, 2 shopping carts removed', 4),
(3, 15, 0, 0, '150 native trees planted', 5),
(4, 10, 28, 12, 'Lake shore cleaned, 4 bags of recycling', 6),
(5, 12, 0, 0, '4 raised garden beds built', 7),
(6, 8, 15, 5, 'Beach monitored, wildlife documented', 3),
(7, 10, 20, 8, '2km of trail cleared', 4),
(8, 12, 0, 0, '20 volunteers trained in waste audit', 7),
(9, 8, 18, 0, '1 acre of wetland restored', 5),
(10, 15, 0, 0, '50 students educated about environment', 7),
(11, 18, 42, 28, 'Harbour area cleaned, 5 tyres removed', 3),
(12, 10, 0, 0, 'Tree survey completed, 200+ trees counted', 4),
(13, 6, 0, 0, 'Wildlife tracking data collected', 5),
(14, 20, 0, 75, 'Community recycling day successful', 7),
(15, 12, 0, 0, 'Riverbank stabilized with native plants', 6),
(16, 8, 0, 0, 'Microplastic samples collected for study', 3),
(17, 25, 0, 0, 'Film night attended by 25 people', 7),
(18, 10, 0, 0, 'Composting workshop completed', 7),
(19, 12, 24, 10, 'Forest trail cleaned', 6),
(20, 8, 0, 0, '10 nesting boxes installed', 5);