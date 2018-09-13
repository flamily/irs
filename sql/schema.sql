-- Schema Enums
CREATE TYPE event_e AS ENUM ('ready', 'seated', 'paid', 'maintaining');

create table sentiments (
	    id SERIAL primary key,
	    feeling varchar(250)
);

insert into sentiments (feeling) values ('hungry'), ('bored');
