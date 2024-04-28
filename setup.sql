CREATE DATABASE IF NOT EXISTS gencorp;

CREATE TABLE IF NOT EXISTS Employee (employee_id int PRIMARY KEY NOT NULL AUTO_INCREMENT,fname VARCHAR(50) NOT NULL, mname VARCHAR(50),lname VARCHAR(50) NOT NULL, password VARCHAR(50) NOT NULL, authorization varchar(50));
CREATE TABLE IF NOT EXISTS Swarm (swarm_id int PRIMARY KEY AUTO_INCREMENT, name varchar(45) NOT NULL,quantity int, latitude double(9, 5), longitude double (9,5));
CREATE TABLE IF NOT EXISTS Oversees (employee_id int, swarm_id int, FOREIGN KEY(employee_id) REFERENCES Employee(employee_id),  FOREIGN KEY(swarm_id) REFERENCES Swarm(swarm_id));
CREATE TABLE IF NOT EXISTS Gnome_Chompskis (chompskis_id int PRIMARY KEY AUTO_INCREMENT,name varchar(45) NOT NULL,  age smallint, height double(10,2), weight double (10,2), no_teeth int UNSIGNED, swarm_id int, FOREIGN KEY(swarm_id) REFERENCES Swarm(swarm_id));

INSERT INTO Employee(fname, mname, lname, password, authorization) VALUES ("Benjamin", "", "Adams", "BAdamsBigBoss1000", "Bossman")
