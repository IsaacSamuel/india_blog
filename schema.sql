drop table if exists comments;
create table comments (
	id integer primary key autoincrement,
	entry integer,
	name text not null,
	comment text not null
);