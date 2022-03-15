create table visitor(
    user_id int(10) unsigned not null auto_increment,
    username varchar(255) not null,
    pass varchar(255) default null,
    first_name VARCHAR(255) default null,
    last_name VARCHAR(255) default null,
    age int(3) default null,
    gender VARCHAR(255) null,
    PRIMARY KEY(user_id),
    UNIQUE KEY `username` (`username`)
) auto_increment = 100;

create table place(
    user_id int(10) unsigned not null auto_increment,
    username varchar(255) not null,
    pass varchar(255) default null,
    place_name VARCHAR(255) default null,
    place_owner_full_name VARCHAR(255),
    place_address VARCHAR(255) default null, 
    place_postal_code int(10) default null,
    PRIMARY KEY(user_id),
    UNIQUE KEY `username` (`username`)
) auto_increment = 100;

create table agent(
    user_id int(10) unsigned not null auto_increment,
    username varchar(255) not null,
    pass varchar(255) default null,
    agent_full_name VARCHAR(255) default null,
    agent_age int(3) default null,
    agent_gender VARCHAR(255) default null,
    PRIMARY KEY(user_id),
    UNIQUE KEY `username` (`username`)
) auto_increment = 100;

create table hospital(
    user_id int(10) unsigned not null auto_increment,
    username varchar(255) not null,
    pass varchar(255) default null,
    hospital_name varchar(255) default null,
    hospital_id varchar(255) not null,
    PRIMARY KEY(user_id),
    UNIQUE KEY `username` (`username`),
    UNIQUE KEY `hospital_id` (`hospital_id`)
) auto_increment = 100;