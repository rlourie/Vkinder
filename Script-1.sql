create table if not exists product (
	id serial primary key,
	vk_id integer,
	vk_age integer,
	vk_sex varchar(40),
	vk_city varchar(40),
	vk_relation varchar(40)
);