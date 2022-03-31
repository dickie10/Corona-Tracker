-- MySQL dump 10.13  Distrib 8.0.28, for Linux (x86_64)
--
-- Host: localhost    Database: corona_archive
-- ------------------------------------------------------
-- Server version	8.0.28-0ubuntu0.20.04.3







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
/*!40000 ALTER TABLE `agent` DISABLE KEYS ;*/
INSERT INTO `agent` VALUES (100,'q','q',NULL,NULL,NULL);
/*!40000 ALTER TABLE `agent` ENABLE KEYS ;*/
UNLOCK TABLES;
=======
INSERT INTO `agent` VALUES (100,'q','q',NULL,NULL,NULL);
>>>>>>> database change


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
/*!40101 SET character_set_client = @saved_cs_client ;*/

--
-- Dumping data for table `hospital`
--

LOCK TABLES `hospital` WRITE;
/*!40000 ALTER TABLE `hospital` DISABLE KEYS ;*/
INSERT INTO `hospital` VALUES (100,'q','q',NULL,'1');
/*!40000 ALTER TABLE `hospital` ENABLE KEYS ;*/
UNLOCK TABLES;



DROP TABLE IF EXISTS `place`;

CREATE TABLE `place` (
  `user_id` int unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `pass` varchar(255) DEFAULT NULL,
  `place_name` varchar(255) DEFAULT NULL,
  `place_owner_full_name` varchar(255) DEFAULT NULL,
  `place_address` varchar(255) DEFAULT NULL,
  `place_postal_code` int DEFAULT NULL, 
  `QRcode` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`)
) AUTO_INCREMENT=104 ;


INSERT INTO `place` VALUES (100,'q','q','q','q','q',1,'qqpp1');



DROP TABLE IF EXISTS `visitor`;
CREATE TABLE `visitor` (
  `user_id` int unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `pass` varchar(255) DEFAULT NULL,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `age` int DEFAULT NULL,
  `gender` varchar(255) DEFAULT NULL,  
  `infected` int, 
  `address` varchar(255) DEFAULT NULL,
  `email` varchar(255)  DEFAULT NULL, 
  `phonenumber` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`)
) AUTO_INCREMENT=108 ;
/*!40101 SET character_set_client = @saved_cs_client ;*/


LOCK TABLES `visitor` WRITE;
/*!40000 ALTER TABLE `visitor` DISABLE KEYS ;*/
INSERT INTO `visitor` VALUES (102,'qq','qq','qq','qq',12,'qq'),(105,'asdf','aa','sdafs','asdfas',23,'dsaf'),(106,'adfas','12','dasfds','asdfas',12,'dgfasg'),(107,'1','1','1','1',1,'1');
/*!40000 ALTER TABLE `visitor` ENABLE KEYS ;*/
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE ;*/

/*!40101 SET SQL_MODE=@OLD_SQL_MODE ;*/
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS ;*/
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS ;*/
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT ;*/
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS ;*/
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION ;*/
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES ;*/

-- Dump completed on 2022-03-18 21:58:25


--
-- Table structure for table `visitor`
--

DROP TABLE IF EXISTS `visitedPlace`;
CREATE TABLE `visitedPlace` (
  `visit_id` int unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int unsigned NOT NULL,
  `place_id` int unsigned NOT NULL,
  `arrival_time` varchar(19), NOT NULL,
  `leave_time` varchar(19),
  PRIMARY KEY (`visit_id`)
) AUTO_INCREMENT=108 ;
INSERT INTO `visitor` VALUES (102,'qq','qq','qq','qq',12,'qq',0,"Bremen","qq@pp.com","98756232");



