create table sentiments (
	    id SERIAL primary key,
	    feeling varchar(250)
);

insert into sentiments (feeling) values ('hungry'), ('bored');
