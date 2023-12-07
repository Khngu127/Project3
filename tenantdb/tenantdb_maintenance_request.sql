-- MySQL dump 10.13  Distrib 8.0.29, for Win64 (x86_64)
--
-- Host: localhost    Database: tenantdb
-- ------------------------------------------------------
-- Server version	8.0.29

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `maintenance_request`
--

DROP TABLE IF EXISTS `maintenance_request`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `maintenance_request` (
  `id` varchar(8) NOT NULL,
  `apartment_number` varchar(255) DEFAULT NULL,
  `area` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `photo` varchar(255) DEFAULT NULL,
  `date_time` varchar(255) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  `comment` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `maintenance_request`
--

LOCK TABLES `maintenance_request` WRITE;
/*!40000 ALTER TABLE `maintenance_request` DISABLE KEYS */;
INSERT INTO `maintenance_request` VALUES ('0228f4e5','1','1','1',NULL,'2023-12-06 19:22:16','completed',''),('09c8dd16','','a','a','','2023-12-06 19:54:39','pending',NULL),('2199a88e','2','don\'t know','haven\'t a scooby','','2023-12-06 18:33:36','completed',''),('21ee3c92','','1','1','','2023-12-06 19:08:03','pending',NULL),('266c6f67','1','somewhere','of course','fish.png','2023-12-06 18:33:26','completed','sure'),('291eb235','','1','1','','2023-12-06 19:09:42','pending',NULL),('484d92de','','a','a','','2023-12-06 19:53:49','pending',NULL),('55c55f7d','1','aa','aa','fish.png','2023-12-06 20:16:35','pending',NULL),('62132867','','fds','fsd','','2023-12-06 19:54:42','pending',NULL),('62ab3887','1','fds','fsd','fish.png','2023-12-06 20:04:21','pending',NULL),('66f91d1f','1','asdf','asdf','fish.png','2023-12-06 20:02:26','pending',NULL),('6d48cf60','1','a','a','','2023-12-06 19:56:18','pending',NULL),('767f0ade','1','fds','fds','','2023-12-06 19:56:28','completed',''),('8a465a62','1','f','f','','2023-12-06 19:56:20','completed','fdsafdsfs'),('903c65a2','101','a','a','','2023-12-06 19:10:45','completed','asdfasdf'),('9f76d771','','asdf','asdf','','2023-12-06 19:54:34','completed','trea'),('d2b11d8b','1','a','a','','2023-12-06 20:03:23','pending',NULL),('e2fce2f3','','asdf','asdf','','2023-12-06 19:53:51','completed','');
/*!40000 ALTER TABLE `maintenance_request` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-12-06 20:45:46
