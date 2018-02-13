-- script used to generate the db used in the analysis
-- create user
CREATE USER  accenture with PASSWORD 'accenture';
--create schema
create schema dblp;
--create tables
create table dblp.paper(
id integer,
name character varying(10000)
);
create table dblp.author(
id integer,
name character varying(10000)
);
create table dblp.author_of(
id integer,
id_l integer,
id_r integer
);

create table dblp.cites(
id integer,
id_l integer,
id_r integer
);

create table dblp.proceedings(
id integer,
id_l integer,
id_r integer
);

create table dblp.journal(
id integer,
id_l integer,
id_r integer
);

create table dblp.book(
id integer,
id_l integer,
id_r integer
);

create table dblp.publisher(
id  integer,
name character varying(10000)
);

create table dblp.type(
id integer,
name character varying(50)
);
--add primary key constraints
alter table dblp.paper add primary key (id);
alter table dblp.author add primary key (id);
alter table dblp.author_of add primary key (id_l,id_r);
alter table dblp.cites add primary key (id_l,id_r);
alter table dblp.proceedings add primary key (id_l,id_r);
alter table dblp.journal add primary key (id_l,id_r);
alter table dblp.book add primary key (id_l,id_r);
alter table dblp.publisher add primary key (id,name);
alter table dblp.type add primary key (id,name);

-- add foreign key constraints to check the data
alter table dblp.author_of ADD CONSTRAINT my_fk_author_of_1 FOREIGN KEY (id_l) REFERENCES dblp.author ON DELETE CASCADE;
alter table dblp.author_of ADD CONSTRAINT my_fk_author_of_2 FOREIGN KEY (id_r) REFERENCES dblp.paper ON DELETE CASCADE;
alter table dblp.cites ADD CONSTRAINT my_fk_cites_1 FOREIGN KEY (id_l) REFERENCES dblp.paper ON DELETE CASCADE;
alter table dblp.cites ADD CONSTRAINT my_fk_cites_2 FOREIGN KEY (id_r) REFERENCES dblp.paper ON DELETE CASCADE;

--grant privileges to the user to access the db
alter table dblp.paper OWNER TO accenture;
alter table dblp.author OWNER TO accenture;
alter table dblp.author_of OWNER TO accenture;
alter table dblp.cites OWNER TO accenture;
GRANT ALL PRIVILEGES ON SCHEMA dblp TO accenture;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA dblp TO accenture;
GRANT ALL PRIVILEGES on database dblp to accenture;
