-- Schema Enums
CREATE TYPE event_e AS ENUM ('ready', 'seated', 'paid', 'maintaining');
CREATE TYPE permission_e AS ENUM ('robot', 'wait_staff', 'management');
CREATE TYPE shape_e AS ENUM ('rectangle', 'ellipse');

-- Schema Tables
CREATE TABLE staff (
	staff_id		serial			PRIMARY KEY,
	username		text 				NOT NULL UNIQUE,
	first_name 	text 				NOT NULL,
	last_name 	text 				NOT NULL,
	password		varchar()		NOT NULL,
	start_dt		timestamp		NOT NULL,
	permission	permission_e NOT NULL
); --WIP

create table sentiments (
	    id SERIAL primary key,
	    feeling varchar(250)
);

insert into sentiments (feeling) values ('hungry'), ('bored');
