/*
 * Purpose: Define persistent data model for the IRS relational database.
 *
 * Author: Andrew Pope
 * Date: 2018-09-14
 */
-- Schema Enums
CREATE TYPE event_e 			AS ENUM ('ready', 'seated', 'paid', 'maintaining');
CREATE TYPE permission_e 	AS ENUM ('robot', 'wait_staff', 'management');
CREATE TYPE shape_e 			AS ENUM ('rectangle', 'ellipse');

-- Schema Tables
CREATE TABLE staff (
	staff_id					serial				PRIMARY KEY,
	username					text 					NOT NULL UNIQUE,
	password					text					NOT NULL,	-- Should not be stored in plaintext. Stored as a hash.
	first_name 				text 					NOT NULL,
	last_name 				text 					NOT NULL,
	start_dt					timestamptz		NOT NULL DEFAULT now(),
	permission				permission_e 	NOT NULL
);

CREATE TABLE dining_table (
	dining_table_id		serial				PRIMARY KEY,
	capacity					numeric				NOT NULL CHECK(capacity > 0),
	x_pos							integer				NOT NULL,
	y_pos							integer				NOT NULL,
	width							integer				NOT NULL CHECK(width > 0),
	height						integer				NOT NULL CHECK(height > 0),
	shape							shape_e				NOT NULL
); -- TODO fancy checks with an event being created in same transaction

CREATE TABLE event (
	event_id					serial				PRIMARY KEY,
	description				event_e				NOT NULL,
	event_dt					timestamptz		NOT NULL DEFAULT now(),
	dining_table_id		integer				NOT NULL REFERENCES dining_table (dining_table_id)
);

CREATE TABLE reservation (
	reservation_id		serial				PRIMARY KEY,
	group_size				numeric				NOT NULL CHECK(group_size > 0),
	reservation_dt		timestamptz		NOT NULL DEFAULT now()
); -- TODO fancy checks with a customer_event being created in same transaction

CREATE TABLE customer_event (
	event_id					integer				NOT NULL,
	reservation_id		integer				NOT NULL,
	staff_id					integer				NOT NULL,
	-- Key definitions
	FOREIGN KEY	(event_id) 					REFERENCES event (event_id),
	FOREIGN KEY	(reservation_id) 		REFERENCES reservation (reservation_id),
	FOREIGN KEY (staff_id)					REFERENCES staff (staff_id),
	PRIMARY KEY (event_id, reservation_id)
);

CREATE TABLE satisfaction (
	event_id					integer				NOT NULL,
	reservation_id		integer				NOT NULL,
	score							numeric				NOT NULL CHECK (score >= 0 AND score <= 100),
	-- Key definitions
	FOREIGN KEY	(event_id, reservation_id) REFERENCES customer_event (event_id, reservation_id),
	PRIMARY KEY (event_id, reservation_id)
);
