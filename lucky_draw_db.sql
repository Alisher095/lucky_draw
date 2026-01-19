-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: lucky_draw_db
-- ------------------------------------------------------
-- Server version	8.0.44

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
-- Table structure for table `accounts_draw`
--

DROP TABLE IF EXISTS `accounts_draw`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_draw` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_by_id` int DEFAULT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT (_utf8mb4'No description provided'),
  `draw_type` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `end_date` date DEFAULT NULL,
  `prize_name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `prize_value` decimal(10,2) NOT NULL,
  `result_date` date DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `winners_count` int unsigned NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `winners_selected` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `accounts_draw_created_by_id_2617ac14_fk_auth_user_id` (`created_by_id`),
  CONSTRAINT `accounts_draw_created_by_id_2617ac14_fk_auth_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `accounts_draw_chk_1` CHECK ((`winners_count` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_draw`
--

LOCK TABLES `accounts_draw` WRITE;
/*!40000 ALTER TABLE `accounts_draw` DISABLE KEYS */;
INSERT INTO `accounts_draw` VALUES (1,4,'this is lucky wheel','single','2026-01-19','luckky wheel',1000.00,'2026-01-20','2026-01-18','lucky wheel',2,'2026-01-18 09:01:17.567035','2026-01-18 09:01:17.567035',0),(2,2,'this is prize bond','single','2026-01-19','Prize bond',1000.00,'2026-01-18','2026-01-18','prize bond',1,'2026-01-18 09:25:34.379228','2026-01-18 10:06:34.092751',1),(3,2,'No description provideRS 1 BIKEd','multi',NULL,'RS 1 BIKE',1.00,NULL,NULL,'RS 1 BIKE',2,'2026-01-18 11:46:27.172595','2026-01-18 11:46:27.172595',0),(4,2,'No description provided\r\ndraw 3draw 3','multi',NULL,'3000 PKR',3000.00,'2026-01-18',NULL,'draw 3',2,'2026-01-18 12:58:44.551516','2026-01-18 14:30:08.680417',1);
/*!40000 ALTER TABLE `accounts_draw` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_entry`
--

DROP TABLE IF EXISTS `accounts_entry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_entry` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `entry_time` datetime(6) NOT NULL,
  `draw_id` bigint NOT NULL,
  `user_id` int NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_verified` tinyint(1) NOT NULL,
  `note` longtext COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_entry_user_id_draw_id_af97eaf6_uniq` (`user_id`,`draw_id`),
  KEY `accounts_entry_draw_id_b294e8bc_fk_accounts_draw_id` (`draw_id`),
  CONSTRAINT `accounts_entry_draw_id_b294e8bc_fk_accounts_draw_id` FOREIGN KEY (`draw_id`) REFERENCES `accounts_draw` (`id`),
  CONSTRAINT `accounts_entry_user_id_e390c5ad_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_entry`
--

LOCK TABLES `accounts_entry` WRITE;
/*!40000 ALTER TABLE `accounts_entry` DISABLE KEYS */;
INSERT INTO `accounts_entry` VALUES (1,'2026-01-18 09:16:23.200762',1,5,1,0,NULL),(2,'2026-01-18 09:46:22.401495',2,5,1,0,NULL),(3,'2026-01-18 09:48:14.656660',2,6,1,0,NULL),(4,'2026-01-18 09:48:18.909022',1,6,1,0,NULL),(5,'2026-01-18 11:47:34.544419',3,6,1,0,NULL),(6,'2026-01-18 14:26:45.609661',4,6,1,0,NULL);
/*!40000 ALTER TABLE `accounts_entry` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_entryadminaction`
--

DROP TABLE IF EXISTS `accounts_entryadminaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_entryadminaction` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `action` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `reason` longtext COLLATE utf8mb4_unicode_ci,
  `created_at` datetime(6) NOT NULL,
  `admin_id` int DEFAULT NULL,
  `entry_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `accounts_entryadminaction_admin_id_fff95fc2_fk_auth_user_id` (`admin_id`),
  KEY `accounts_entryadminaction_entry_id_4420376b_fk_accounts_entry_id` (`entry_id`),
  CONSTRAINT `accounts_entryadminaction_admin_id_fff95fc2_fk_auth_user_id` FOREIGN KEY (`admin_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `accounts_entryadminaction_entry_id_4420376b_fk_accounts_entry_id` FOREIGN KEY (`entry_id`) REFERENCES `accounts_entry` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_entryadminaction`
--

LOCK TABLES `accounts_entryadminaction` WRITE;
/*!40000 ALTER TABLE `accounts_entryadminaction` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_entryadminaction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_profile`
--

DROP TABLE IF EXISTS `accounts_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_profile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `role` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `accounts_profile_user_id_49a85d32_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_profile`
--

LOCK TABLES `accounts_profile` WRITE;
/*!40000 ALTER TABLE `accounts_profile` DISABLE KEYS */;
INSERT INTO `accounts_profile` VALUES (1,'admin',2),(2,'admin',3),(3,'admin',4),(4,'user',5),(5,'user',6);
/*!40000 ALTER TABLE `accounts_profile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_winner`
--

DROP TABLE IF EXISTS `accounts_winner`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_winner` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `position` smallint unsigned NOT NULL,
  `draw_id` bigint NOT NULL,
  `user_id` int NOT NULL,
  `audit_note` longtext COLLATE utf8mb4_unicode_ci,
  `entry_id` bigint DEFAULT NULL,
  `method` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `seed` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `selected_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_winner_draw_id_position_798d8eba_uniq` (`draw_id`,`position`),
  KEY `accounts_winner_user_id_9fa72d6b_fk_auth_user_id` (`user_id`),
  KEY `accounts_winner_draw_id_aab3580a` (`draw_id`),
  KEY `accounts_winner_entry_id_1fabf32d_fk_accounts_entry_id` (`entry_id`),
  CONSTRAINT `accounts_winner_draw_id_aab3580a_fk_accounts_draw_id` FOREIGN KEY (`draw_id`) REFERENCES `accounts_draw` (`id`),
  CONSTRAINT `accounts_winner_entry_id_1fabf32d_fk_accounts_entry_id` FOREIGN KEY (`entry_id`) REFERENCES `accounts_entry` (`id`),
  CONSTRAINT `accounts_winner_user_id_9fa72d6b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `accounts_winner_position_1359fd0d_check` CHECK ((`position` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_winner`
--

LOCK TABLES `accounts_winner` WRITE;
/*!40000 ALTER TABLE `accounts_winner` DISABLE KEYS */;
INSERT INTO `accounts_winner` VALUES (1,1,2,6,NULL,NULL,'random_sample',NULL,'2026-01-18 10:06:34.083088'),(2,1,4,6,NULL,NULL,'random_sample',NULL,'2026-01-18 14:30:08.668878'),(3,2,4,6,NULL,NULL,'random_sample',NULL,'2026-01-18 14:30:08.668878');
/*!40000 ALTER TABLE `accounts_winner` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add profile',7,'add_profile'),(26,'Can change profile',7,'change_profile'),(27,'Can delete profile',7,'delete_profile'),(28,'Can view profile',7,'view_profile'),(29,'Can add draw',8,'add_draw'),(30,'Can change draw',8,'change_draw'),(31,'Can delete draw',8,'delete_draw'),(32,'Can view draw',8,'view_draw'),(33,'Can add winner',9,'add_winner'),(34,'Can change winner',9,'change_winner'),(35,'Can delete winner',9,'delete_winner'),(36,'Can view winner',9,'view_winner'),(37,'Can add entry',10,'add_entry'),(38,'Can change entry',10,'change_entry'),(39,'Can delete entry',10,'delete_entry'),(40,'Can view entry',10,'view_entry'),(41,'Can add entry admin action',11,'add_entryadminaction'),(42,'Can change entry admin action',11,'change_entryadminaction'),(43,'Can delete entry admin action',11,'delete_entryadminaction'),(44,'Can view entry admin action',11,'view_entryadminaction');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'',NULL,0,'user3','user','3','user3@gmail.com',0,1,'2026-01-18 07:05:06.820222'),(2,'pbkdf2_sha256$1200000$1sEq7yQJpXckGYoL8mCGO8$bZbmIfwTPWz1OmLvwO8H/Gq18IiO1MoaoySz0VMleUI=','2026-01-18 20:27:11.700711',0,'admin3','admin','3','admin3@gmail.com',0,1,'2026-01-18 07:32:50.269317'),(3,'pbkdf2_sha256$1000000$Dci472fX8DfJD7AmRHru7B$0gahVMhcXbmFuXCsRp0Yg8MRcm/Q1H9MD17I2VPYpYA=',NULL,0,'admin4','admin','4','admin4@gmail.com',0,1,'2026-01-18 07:32:51.148379'),(4,'pbkdf2_sha256$1200000$DVIHdc1VhMI8D6romwGGwO$MVNi889jFMU0fCDCla9kUGryblO4uxMGCeKqCASNkvI=','2026-01-18 08:52:52.310756',0,'admin@gmail.com','admin','123','admin@gmail.com',0,1,'2026-01-18 07:50:08.874913'),(5,'pbkdf2_sha256$1200000$7NQlwOfLhPkp0SwXGjgCIt$yw3jodtkRP/HZh337HuxooxDWMsldwS+3ji218EnXK4=','2026-01-18 09:46:18.367143',0,'u1@gmail.com','u','1','u1@gmail.com',0,1,'2026-01-18 07:56:18.585071'),(6,'pbkdf2_sha256$1000000$pBWpbsFpRF2Va3iZS0z47g$gWsfsn5UPcp3TmU1jH5aTX08IW/gVRfuH5ImFDcOBNs=','2026-01-19 07:26:21.858698',0,'u2@gmail.com','u','2','u2@gmail.com',0,1,'2026-01-18 09:47:54.298113');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (8,'accounts','draw'),(10,'accounts','entry'),(11,'accounts','entryadminaction'),(7,'accounts','profile'),(9,'accounts','winner'),(1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2026-01-18 06:26:19.591556'),(2,'auth','0001_initial','2026-01-18 06:26:20.451907'),(3,'accounts','0001_initial','2026-01-18 06:26:20.581809'),(4,'accounts','0002_draw_winner_entry','2026-01-18 06:26:21.022793'),(5,'accounts','0003_alter_entry_draw_alter_entry_user','2026-01-18 06:26:21.036715'),(6,'accounts','0004_alter_winner_options_remove_draw_eligibility_and_more','2026-01-18 06:26:21.488624'),(7,'accounts','0005_remove_draw_draw_date_and_more','2026-01-18 06:26:22.555779'),(8,'accounts','0006_alter_entry_options_alter_winner_unique_together_and_more','2026-01-18 06:26:23.818045'),(9,'accounts','0007_alter_winner_unique_together_draw_winners_selected_and_more','2026-01-18 06:26:23.983169'),(10,'admin','0001_initial','2026-01-18 06:26:24.165604'),(11,'admin','0002_logentry_remove_auto_add','2026-01-18 06:26:24.175168'),(12,'admin','0003_logentry_add_action_flag_choices','2026-01-18 06:26:24.188140'),(13,'contenttypes','0002_remove_content_type_name','2026-01-18 06:26:24.341037'),(14,'auth','0002_alter_permission_name_max_length','2026-01-18 06:26:24.437504'),(15,'auth','0003_alter_user_email_max_length','2026-01-18 06:26:24.475279'),(16,'auth','0004_alter_user_username_opts','2026-01-18 06:26:24.488311'),(17,'auth','0005_alter_user_last_login_null','2026-01-18 06:26:24.583701'),(18,'auth','0006_require_contenttypes_0002','2026-01-18 06:26:24.586671'),(19,'auth','0007_alter_validators_add_error_messages','2026-01-18 06:26:24.596670'),(20,'auth','0008_alter_user_username_max_length','2026-01-18 06:26:24.693523'),(21,'auth','0009_alter_user_last_name_max_length','2026-01-18 06:26:24.797571'),(22,'auth','0010_alter_group_name_max_length','2026-01-18 06:26:24.825474'),(23,'auth','0011_update_proxy_permissions','2026-01-18 06:26:24.845471'),(24,'auth','0012_alter_user_first_name_max_length','2026-01-18 06:26:24.964513'),(25,'sessions','0001_initial','2026-01-18 06:26:25.010384');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('5eekn54cd8oh91zbwficbl8hs3278lhy','.eJxVjLEOwyAQQ_-FuUKQBg517N5vQHdwhLQVSCGZqv57iZShmWz52f4Ij9ua_dZ48XMUNzGIy39GGF5cdhCfWKYqQy3rMpPcK_KgTT5q5Pf96J4OMrbc184ax6QhQWRLjkYelEYGCqg0RwCbxmuyFMAAGGV0UOi4e-xiUxLfH_V1OHU:1vhSqz:kpA3VBMCaksJahUnlYsi44nAzIqcAgo_ac8e8yQ6vbQ','2026-02-01 13:30:05.854206'),('c6a6e8shs6heez0nk1i8ebxtlh4rth80','.eJxVjDEOwjAMRe-SGUUkkV3CyM4ZIjuOSQGlUtNOiLtDpQ6w_vfef5lE61LT2sucRjFng-bwuzHlR2kbkDu122Tz1JZ5ZLspdqfdXicpz8vu_h1U6vVbcybmkyo5CQpIohpCGBiEI4sL5Lw7xowAqOg5eHC5IAIJRD9ANu8PH5w4ig:1vhjeX:6whbKgB_A26tR7PTL60gT5_Tn75YNrR932Bw_Wibt3A','2026-02-02 07:26:21.862698');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-01-19 13:58:40
