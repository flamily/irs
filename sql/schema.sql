create table sentiments (
	    id SERIAL primary key,
	    feeling varchar(250)
);

insert into no_sentiments (feeling) values ('hungry'), ('bored');
