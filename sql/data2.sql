-- MySQL dump 10.13  Distrib 8.0.28, for Linux (x86_64)
--
-- Host: localhost    Database: corona_archive
-- ------------------------------------------------------
-- Server version	8.0.28-0ubuntu0.20.04.3



--
-- Table structure for table `agent`
--



DROP TABLE IF EXISTS `agent`;

CREATE TABLE `agent` (
  `user_id` int unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `pass` varchar(255) DEFAULT NULL,
  `agent_full_name` varchar(255) DEFAULT NULL,
  `agent_age` int DEFAULT NULL,
  `agent_gender` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`)
)  AUTO_INCREMENT=101 ;

LOCK TABLES `agent` WRITE;
INSERT INTO `agent` VALUES (100,'q','q',NULL,NULL,NULL);
UNLOCK TABLES;
--
-- Table structure for table `hospital`
--

DROP TABLE IF EXISTS `hospital`;

CREATE TABLE `hospital` (
  `user_id` int unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `pass` varchar(255) DEFAULT NULL,
  `hospital_name` varchar(255) DEFAULT NULL,
  `hospital_medical_id` varchar(255) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `hospital_id` (`hospital_medical_id`)
) AUTO_INCREMENT=101;

LOCK TABLES `hospital` WRITE;
INSERT INTO `hospital` VALUES (100,'q','q',NULL,'1');
UNLOCK TABLES;


--
-- Table structure for table `place`
--

DROP TABLE IF EXISTS `place`;

CREATE TABLE `place` (
  `user_id` int unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `pass` varchar(255) DEFAULT NULL,
  `place_name` varchar(255) DEFAULT NULL,
  `place_owner_full_name` varchar(255) DEFAULT NULL,
  `place_address` varchar(255) DEFAULT NULL,
  `place_postal_code` int DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`)
) AUTO_INCREMENT=104 ;

LOCK TABLES `place` WRITE;
INSERT INTO `place` VALUES (100,'q','q','q','q','q',1),(101,'w','w','w','w','w',1),(102,'dsaf','q','q','q','q',12),(103,'sdfvasdfva','1','1','1','1',1);
UNLOCK TABLES;


--
-- Table structure for table `visitor`
--

DROP TABLE IF EXISTS `visitor`;
CREATE TABLE `visitor` (
  `user_id` int unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `pass` varchar(255) DEFAULT NULL,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `age` int DEFAULT NULL,
  `gender` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`)
) AUTO_INCREMENT=108 ;

LOCK TABLES `visitor` WRITE;
INSERT INTO `visitor` VALUES (102,'qq','qq','qq','qq',12,'qq'),(105,'asdf','aa','sdafs','asdfas',23,'dsaf'),(106,'adfas','12','dasfds','asdfas',12,'dgfasg'),(107,'1','1','1','1',1,'1');
UNLOCK TABLES;

--
-- Table structure for table `visitedPlace`
--

DROP TABLE IF EXISTS `visitedPlace`;
CREATE TABLE `visitedPlace` (
  `visit_id` int unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int unsigned NOT NULL,
  `place_id` int unsigned NOT NULL,
  `arrival_time` varchar(19) NOT NULL,
  `leave_time` varchar(19),
  PRIMARY KEY (`visit_id`)
) AUTO_INCREMENT=108 ;