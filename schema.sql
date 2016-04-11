drop table if exists entries;
create table entries (
	id integer primary key autoincrement,
	title text not null,
	text text not null
);

drop table if exists tags;
create table tags (
	id integer primary key autoincrement,
	entry integer,
	name text
);

drop table if exists comments;
create table comments (
	id integer primary key autoincrement,
	entry integer,
	name text not null,
	comment text not null
);