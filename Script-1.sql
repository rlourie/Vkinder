create table if not exists vk_users (
	id serial primary key,
	vk_id integer,
	vk_age integer,
	vk_sex varchar(40),
	vk_city varchar(40),
	vk_relation varchar(40),
	vk_offset integer
);
create table if not exists vk_search (
	id serial primary key,
	vk_id_user integer,
	vk_id_search integer
)