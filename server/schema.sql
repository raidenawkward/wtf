drop table if exists keys;
drop table if exists valuesofkey;
create table keys (
  id integer primary key autoincrement,
  key text not null
);
create table valuesofkey (
  id integer primary key autoincrement,
  key text not null,
  value text default null,
  tag text default null,
  createdby text default null
);
