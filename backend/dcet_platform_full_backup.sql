-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: dcet_platform
-- ------------------------------------------------------
-- Server version	8.0.43

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `dcet_platform`
--

/*!40000 DROP DATABASE IF EXISTS `dcet_platform`*/;

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `dcet_platform` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `dcet_platform`;

--
-- Table structure for table `app_settings`
--

DROP TABLE IF EXISTS `app_settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `app_settings` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `setting_key` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `setting_value` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `setting_key` (`setting_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_settings`
--

LOCK TABLES `app_settings` WRITE;
/*!40000 ALTER TABLE `app_settings` DISABLE KEYS */;
/*!40000 ALTER TABLE `app_settings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `attempt_answers`
--

DROP TABLE IF EXISTS `attempt_answers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `attempt_answers` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `selected_option` varchar(1) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_correct` tinyint(1) NOT NULL,
  `attempt_id` bigint NOT NULL,
  `question_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `attempt_answers_attempt_id_question_id_efc96dc0_uniq` (`attempt_id`,`question_id`),
  KEY `attempt_answers_question_id_e34489ec_fk_questions_id` (`question_id`),
  KEY `attempt_ans_attempt_91b708_idx` (`attempt_id`,`question_id`),
  CONSTRAINT `attempt_answers_attempt_id_6ed91d37_fk_attempts_id` FOREIGN KEY (`attempt_id`) REFERENCES `attempts` (`id`),
  CONSTRAINT `attempt_answers_question_id_e34489ec_fk_questions_id` FOREIGN KEY (`question_id`) REFERENCES `questions` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attempt_answers`
--

LOCK TABLES `attempt_answers` WRITE;
/*!40000 ALTER TABLE `attempt_answers` DISABLE KEYS */;
INSERT INTO `attempt_answers` (`id`, `selected_option`, `is_correct`, `attempt_id`, `question_id`) VALUES (14,'B',1,16,91),(15,'C',0,16,133),(16,'B',0,15,131),(17,'C',0,19,87),(18,'A',1,19,83),(19,'C',0,19,103),(20,'B',0,19,95),(21,'B',1,19,91),(22,'C',0,22,158),(23,'B',0,24,71),(24,'B',0,24,78),(25,'B',0,24,89),(26,'A',1,25,71),(27,'B',0,28,71),(28,'B',0,28,88),(29,'B',1,28,97),(30,'A',0,28,91),(31,'A',0,28,92),(32,'A',1,29,71),(33,'C',0,32,163),(34,'A',1,32,71),(35,'B',0,32,93),(36,'C',1,32,154),(37,'C',0,32,142),(38,'C',0,32,143),(39,'B',0,32,107),(40,'A',0,31,81),(41,'B',1,31,82),(42,'B',1,31,92),(43,'B',1,31,86);
/*!40000 ALTER TABLE `attempt_answers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `attempts`
--

DROP TABLE IF EXISTS `attempts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `attempts` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `started_at` datetime(6) NOT NULL,
  `finished_at` datetime(6) DEFAULT NULL,
  `score` int NOT NULL,
  `status` varchar(15) COLLATE utf8mb4_unicode_ci NOT NULL,
  `randomized_order` json NOT NULL,
  `exam_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `attempts_user_id_4c9686_idx` (`user_id`,`exam_id`),
  KEY `attempts_status_ea0f26_idx` (`status`),
  KEY `attempts_exam_id_918df9b7_fk_exams_id` (`exam_id`),
  KEY `attempts_status_945b1d7f` (`status`),
  CONSTRAINT `attempts_exam_id_918df9b7_fk_exams_id` FOREIGN KEY (`exam_id`) REFERENCES `exams` (`id`),
  CONSTRAINT `attempts_user_id_e8ed0ca1_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attempts`
--

LOCK TABLES `attempts` WRITE;
/*!40000 ALTER TABLE `attempts` DISABLE KEYS */;
INSERT INTO `attempts` (`id`, `started_at`, `finished_at`, `score`, `status`, `randomized_order`, `exam_id`, `user_id`) VALUES (15,'2025-12-05 13:15:17.027462','2025-12-05 13:44:26.327890',0,'submitted','[]',6,4),(16,'2025-12-05 13:15:17.029525','2025-12-05 13:38:38.860772',1,'submitted','[]',6,4),(17,'2025-12-05 13:36:32.584520',NULL,0,'in_progress','[]',6,3),(18,'2025-12-05 13:36:32.586511','2025-12-05 13:36:44.137652',0,'submitted','[]',6,3),(19,'2025-12-05 13:44:29.683062','2025-12-05 14:15:43.118779',2,'submitted','[]',6,4),(20,'2025-12-05 13:44:29.684574','2025-12-05 13:44:55.060548',0,'submitted','[]',6,4),(21,'2025-12-05 15:00:40.195457',NULL,0,'timeout','[]',6,4),(22,'2025-12-05 15:00:40.207454','2025-12-05 15:01:01.324277',0,'submitted','[]',6,4),(23,'2025-12-05 19:22:57.111218','2025-12-05 19:34:38.981306',0,'submitted','[]',6,4),(24,'2025-12-05 19:22:57.112232','2025-12-05 19:23:14.142153',0,'submitted','[]',6,4),(25,'2025-12-05 20:57:25.459513','2025-12-05 21:06:53.245035',1,'submitted','[]',6,4),(26,'2025-12-05 20:57:25.498058','2025-12-05 21:02:26.479767',0,'submitted','[]',6,4),(27,'2025-12-05 21:07:02.707914','2025-12-05 21:17:22.168893',0,'submitted','[]',6,4),(28,'2025-12-05 21:07:02.709907','2025-12-05 21:16:59.602143',1,'submitted','[]',6,4),(29,'2025-12-05 21:17:29.819180','2025-12-05 21:19:46.944794',1,'submitted','[]',6,4),(30,'2025-12-05 21:17:29.820179','2025-12-05 21:19:11.633684',0,'submitted','[]',6,4),(31,'2025-12-09 20:07:23.373813',NULL,0,'in_progress','[]',6,4),(32,'2025-12-09 20:07:23.389039','2025-12-09 20:18:53.560686',2,'submitted','[]',6,4);
/*!40000 ALTER TABLE `attempts` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add user',6,'add_user'),(22,'Can change user',6,'change_user'),(23,'Can delete user',6,'delete_user'),(24,'Can view user',6,'view_user'),(25,'Can add user activity',7,'add_useractivity'),(26,'Can change user activity',7,'change_useractivity'),(27,'Can delete user activity',7,'delete_useractivity'),(28,'Can view user activity',7,'view_useractivity'),(29,'Can add profile',8,'add_profile'),(30,'Can change profile',8,'change_profile'),(31,'Can delete profile',8,'delete_profile'),(32,'Can view profile',8,'view_profile'),(33,'Can add password reset request',9,'add_passwordresetrequest'),(34,'Can change password reset request',9,'change_passwordresetrequest'),(35,'Can delete password reset request',9,'delete_passwordresetrequest'),(36,'Can view password reset request',9,'view_passwordresetrequest'),(37,'Can add notification',10,'add_notification'),(38,'Can change notification',10,'change_notification'),(39,'Can delete notification',10,'delete_notification'),(40,'Can view notification',10,'view_notification'),(41,'Can add exam',11,'add_exam'),(42,'Can change exam',11,'change_exam'),(43,'Can delete exam',11,'delete_exam'),(44,'Can view exam',11,'view_exam'),(45,'Can add section',12,'add_section'),(46,'Can change section',12,'change_section'),(47,'Can delete section',12,'delete_section'),(48,'Can view section',12,'view_section'),(49,'Can add question',13,'add_question'),(50,'Can change question',13,'change_question'),(51,'Can delete question',13,'delete_question'),(52,'Can view question',13,'view_question'),(53,'Can add attempt',14,'add_attempt'),(54,'Can change attempt',14,'change_attempt'),(55,'Can delete attempt',14,'delete_attempt'),(56,'Can view attempt',14,'view_attempt'),(57,'Can add attempt answer',15,'add_attemptanswer'),(58,'Can change attempt answer',15,'change_attemptanswer'),(59,'Can delete attempt answer',15,'delete_attemptanswer'),(60,'Can view attempt answer',15,'view_attemptanswer'),(61,'Can add payment',16,'add_payment'),(62,'Can change payment',16,'change_payment'),(63,'Can delete payment',16,'delete_payment'),(64,'Can view payment',16,'view_payment'),(65,'Can add plan',17,'add_plan'),(66,'Can change plan',17,'change_plan'),(67,'Can delete plan',17,'delete_plan'),(68,'Can view plan',17,'view_plan'),(69,'Can add App Setting',18,'add_appsettings'),(70,'Can change App Setting',18,'change_appsettings'),(71,'Can delete App Setting',18,'delete_appsettings'),(72,'Can view App Setting',18,'view_appsettings'),(73,'Can add question issue',19,'add_questionissue'),(74,'Can change question issue',19,'change_questionissue'),(75,'Can delete question issue',19,'delete_questionissue'),(76,'Can view question issue',19,'view_questionissue'),(77,'Can add email otp',20,'add_emailotp'),(78,'Can change email otp',20,'change_emailotp'),(79,'Can delete email otp',20,'delete_emailotp'),(80,'Can view email otp',20,'view_emailotp');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
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
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_users_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
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
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES (1,'admin','logentry'),(18,'adminpanel','appsettings'),(3,'auth','group'),(2,'auth','permission'),(4,'contenttypes','contenttype'),(11,'exams','exam'),(13,'exams','question'),(12,'exams','section'),(16,'payments','payment'),(17,'payments','plan'),(14,'results','attempt'),(15,'results','attemptanswer'),(19,'results','questionissue'),(5,'sessions','session'),(20,'users','emailotp'),(10,'users','notification'),(9,'users','passwordresetrequest'),(8,'users','profile'),(6,'users','user'),(7,'users','useractivity');
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
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES (1,'payments','0001_initial','2025-12-04 17:00:38.981983'),(2,'users','0001_initial','2025-12-04 17:00:40.400728'),(3,'contenttypes','0001_initial','2025-12-04 17:00:40.510312'),(4,'admin','0001_initial','2025-12-04 17:00:40.912827'),(5,'admin','0002_logentry_remove_auto_add','2025-12-04 17:00:40.935642'),(6,'admin','0003_logentry_add_action_flag_choices','2025-12-04 17:00:40.952825'),(7,'adminpanel','0001_initial','2025-12-04 17:00:41.035620'),(8,'contenttypes','0002_remove_content_type_name','2025-12-04 17:00:41.333279'),(9,'auth','0001_initial','2025-12-04 17:00:42.127049'),(10,'auth','0002_alter_permission_name_max_length','2025-12-04 17:00:42.289185'),(11,'auth','0003_alter_user_email_max_length','2025-12-04 17:00:42.308004'),(12,'auth','0004_alter_user_username_opts','2025-12-04 17:00:42.326622'),(13,'auth','0005_alter_user_last_login_null','2025-12-04 17:00:42.344980'),(14,'auth','0006_require_contenttypes_0002','2025-12-04 17:00:42.354302'),(15,'auth','0007_alter_validators_add_error_messages','2025-12-04 17:00:42.373930'),(16,'auth','0008_alter_user_username_max_length','2025-12-04 17:00:42.390364'),(17,'auth','0009_alter_user_last_name_max_length','2025-12-04 17:00:42.415525'),(18,'auth','0010_alter_group_name_max_length','2025-12-04 17:00:42.467164'),(19,'auth','0011_update_proxy_permissions','2025-12-04 17:00:42.496161'),(20,'auth','0012_alter_user_first_name_max_length','2025-12-04 17:00:42.511242'),(21,'exams','0001_initial','2025-12-04 17:00:43.265388'),(22,'payments','0002_initial','2025-12-04 17:00:43.565697'),(23,'results','0001_initial','2025-12-04 17:00:44.617825'),(24,'sessions','0001_initial','2025-12-04 17:00:44.716332'),(25,'results','0002_questionissue','2025-12-05 13:26:34.022190'),(26,'users','0002_emailotp','2025-12-09 15:46:18.387965');
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
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `email_otps`
--

DROP TABLE IF EXISTS `email_otps`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `email_otps` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `otp` varchar(6) COLLATE utf8mb4_unicode_ci NOT NULL,
  `purpose` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_verified` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `email_otps_email_bf9e3214` (`email`),
  KEY `email_otps_created_at_1fbf7a8b` (`created_at`),
  KEY `email_otps_email_f309a0_idx` (`email`,`created_at`),
  KEY `email_otps_email_c12e2a_idx` (`email`,`purpose`,`is_verified`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `email_otps`
--

LOCK TABLES `email_otps` WRITE;
/*!40000 ALTER TABLE `email_otps` DISABLE KEYS */;
/*!40000 ALTER TABLE `email_otps` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exams`
--

DROP TABLE IF EXISTS `exams`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `exams` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `year` int NOT NULL,
  `total_marks` int NOT NULL,
  `duration_minutes` int NOT NULL,
  `is_published` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `exams_is_publ_8bb3b8_idx` (`is_published`),
  KEY `exams_year_61f053_idx` (`year`),
  KEY `exams_is_published_fc941262` (`is_published`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exams`
--

LOCK TABLES `exams` WRITE;
/*!40000 ALTER TABLE `exams` DISABLE KEYS */;
INSERT INTO `exams` (`id`, `name`, `year`, `total_marks`, `duration_minutes`, `is_published`, `created_at`, `updated_at`) VALUES (6,'DCET',2023,100,180,1,'2025-12-05 13:09:56.912535','2025-12-05 13:10:32.788813');
/*!40000 ALTER TABLE `exams` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notifications`
--

DROP TABLE IF EXISTS `notifications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notifications` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `notifications_user_id_468e288d_fk_users_id` (`user_id`),
  CONSTRAINT `notifications_user_id_468e288d_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notifications`
--

LOCK TABLES `notifications` WRITE;
/*!40000 ALTER TABLE `notifications` DISABLE KEYS */;
/*!40000 ALTER TABLE `notifications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `password_reset_requests`
--

DROP TABLE IF EXISTS `password_reset_requests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `password_reset_requests` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `reset_token` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `expires_at` datetime(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `password_reset_requests_user_id_6ed32be7_fk_users_id` (`user_id`),
  CONSTRAINT `password_reset_requests_user_id_6ed32be7_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `password_reset_requests`
--

LOCK TABLES `password_reset_requests` WRITE;
/*!40000 ALTER TABLE `password_reset_requests` DISABLE KEYS */;
/*!40000 ALTER TABLE `password_reset_requests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payments`
--

DROP TABLE IF EXISTS `payments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payments` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `provider` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `provider_payment_id` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `order_id` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `amount` int NOT NULL,
  `currency` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `metadata` json NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `provider_payment_id` (`provider_payment_id`),
  KEY `payments_status_760e149d` (`status`),
  KEY `payments_user_id_1b771c_idx` (`user_id`,`status`),
  KEY `payments_provide_340c17_idx` (`provider_payment_id`),
  CONSTRAINT `payments_user_id_189b9948_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payments`
--

LOCK TABLES `payments` WRITE;
/*!40000 ALTER TABLE `payments` DISABLE KEYS */;
/*!40000 ALTER TABLE `payments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `plans`
--

DROP TABLE IF EXISTS `plans`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `plans` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `key` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `price_in_paisa` int NOT NULL,
  `duration_days` int NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `key` (`key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plans`
--

LOCK TABLES `plans` WRITE;
/*!40000 ALTER TABLE `plans` DISABLE KEYS */;
/*!40000 ALTER TABLE `plans` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `profiles`
--

DROP TABLE IF EXISTS `profiles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `profiles` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `is_paid` tinyint(1) NOT NULL,
  `subscription_start` datetime(6) DEFAULT NULL,
  `subscription_end` datetime(6) DEFAULT NULL,
  `plan_id` bigint DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `profiles_plan_id_69c646bd_fk_plans_id` (`plan_id`),
  KEY `profiles_is_paid_2211e5f3` (`is_paid`),
  CONSTRAINT `profiles_plan_id_69c646bd_fk_plans_id` FOREIGN KEY (`plan_id`) REFERENCES `plans` (`id`),
  CONSTRAINT `profiles_user_id_36580373_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `profiles`
--

LOCK TABLES `profiles` WRITE;
/*!40000 ALTER TABLE `profiles` DISABLE KEYS */;
INSERT INTO `profiles` (`id`, `is_paid`, `subscription_start`, `subscription_end`, `plan_id`, `user_id`) VALUES (1,0,NULL,NULL,NULL,1),(2,0,NULL,NULL,NULL,2),(3,0,NULL,NULL,NULL,3),(4,0,NULL,NULL,NULL,4);
/*!40000 ALTER TABLE `profiles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `question_issues`
--

DROP TABLE IF EXISTS `question_issues`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `question_issues` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `issue_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(15) COLLATE utf8mb4_unicode_ci NOT NULL,
  `admin_notes` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `attempt_id` bigint DEFAULT NULL,
  `question_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `question_issues_attempt_id_52f68a33_fk_attempts_id` (`attempt_id`),
  KEY `question_issues_status_6951615d` (`status`),
  KEY `question_is_questio_53e3ec_idx` (`question_id`,`status`),
  KEY `question_is_user_id_ee4759_idx` (`user_id`,`created_at`),
  CONSTRAINT `question_issues_attempt_id_52f68a33_fk_attempts_id` FOREIGN KEY (`attempt_id`) REFERENCES `attempts` (`id`),
  CONSTRAINT `question_issues_question_id_c9c6d780_fk_questions_id` FOREIGN KEY (`question_id`) REFERENCES `questions` (`id`),
  CONSTRAINT `question_issues_user_id_759ee22b_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `question_issues`
--

LOCK TABLES `question_issues` WRITE;
/*!40000 ALTER TABLE `question_issues` DISABLE KEYS */;
/*!40000 ALTER TABLE `question_issues` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `questions`
--

DROP TABLE IF EXISTS `questions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `questions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `question_number` int NOT NULL,
  `question_text` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `plain_text` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `option_a` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  `option_b` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  `option_c` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  `option_d` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  `correct_option` varchar(1) COLLATE utf8mb4_unicode_ci NOT NULL,
  `marks` int NOT NULL,
  `diagram_url` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `section_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `questions_section_id_question_number_9443a0fd_uniq` (`section_id`,`question_number`),
  KEY `questions_section_775a09_idx` (`section_id`,`question_number`),
  CONSTRAINT `questions_section_id_2a64df75_fk_sections_id` FOREIGN KEY (`section_id`) REFERENCES `sections` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=171 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `questions`
--

LOCK TABLES `questions` WRITE;
/*!40000 ALTER TABLE `questions` DISABLE KEYS */;
INSERT INTO `questions` (`id`, `question_number`, `question_text`, `plain_text`, `option_a`, `option_b`, `option_c`, `option_d`, `correct_option`, `marks`, `diagram_url`, `created_at`, `section_id`) VALUES (71,1,'Which of the following is \\textbf{not} a cyber crime?','Which of the following is not a cyber crime?','Cryptography','Denial of Service','Man-in-the-middle attack','Phishing','A',1,NULL,'2025-12-05 13:09:56.937266',10),(72,2,'DoS is abbreviated as \\_\\_\\_\\_\\_\\_\\_\\_.','DoS is abbreviated as _________','Denial of Service','Distribution of Server','Distribution of Service','Denial of Server','A',1,NULL,'2025-12-05 13:09:56.947926',10),(73,3,'\\_\\_\\_\\_ protects interconnected systems including hardware, software and programs and data from cyber attacks.','____ protects interconnected systems including hardware, software and programs and data from cyber attacks.','Cyber Security','Computer Security','Resource Security','Hardware Security','A',1,NULL,'2025-12-05 13:09:56.957939',10),(74,4,'Basic functionality of the network device firewall is:','Basic functionality of the network device firewall is:','scans mobile applications','monitoring database','privatizes the computers','monitoring incoming and outgoing networks','D',1,NULL,'2025-12-05 13:09:56.969044',10),(75,5,'An algorithm represented in the form of programming language is called:','An algorithm represented in the form of programming language is called:','Flowchart','Pseudocode','Program','Instruction','C',1,NULL,'2025-12-05 13:09:56.977767',10),(76,6,'The \\_\\_\\_\\_\\_ symbol is used when the flowchart is starting or ending.','The ____ symbol is used when the flowchart is starting or ending.','Connector/Arrow','Terminal box/Rounded rectangle','Input/Output','Process','B',1,NULL,'2025-12-05 13:09:56.988950',10),(77,7,'MIT App Inventor allows user to','MIT App Inventor allows user to','Create web application','Build Android application','Create System Software','Develop Operating System','B',1,NULL,'2025-12-05 13:09:56.997500',10),(78,8,'What is the function of the ``when green flag clicked\'\' command block?','What is the function of the when green flag clicked command block?','Points Sprite in the specified direction','If condition is true, runs the blocks inside','Runs the script','Stops the execution of script','C',1,NULL,'2025-12-05 13:09:57.007816',10),(79,9,'The correct sequence of HTML tags for starting a webpage is:','The correct sequence of HTML tags for starting a webpage is:','Head, Title, Html, Body','Html, Head, Title, Body','Html, Body, Title, Head','Html, Title, Head, Body','B',1,NULL,'2025-12-05 13:09:57.019733',10),(80,10,'Web server:','Web server:','is a computer system that delivers web pages','is delivery news','provides options for those seeking real-time discussions','prints documents','A',1,NULL,'2025-12-05 13:09:57.030913',10),(81,11,'Which of the following is used to style the appearance of web pages?','Which of the following is used to style the appearance of web pages?','Html','JavaScript','PHP','CSS','D',1,NULL,'2025-12-05 13:09:57.042331',10),(82,12,'Which of the following is an example of web browser?','Which of the following is an example of web browser?','Google','Firefox','Apache','MySQL','B',1,NULL,'2025-12-05 13:09:57.053458',10),(83,13,'Which of the following is an open source and free workflow management software?','Which of the following is an open source and free workflow management software?','Trello','MS Excel','Windows','Linux','A',1,NULL,'2025-12-05 13:09:57.062479',10),(84,14,'ERP package will handle \\_\\_\\_\\_\\_\\_ business functionality/functionalities.','ERP package will handle ______ business functionality/functionalities.','One','Two','Three','Multiple/all','D',1,NULL,'2025-12-05 13:09:57.072678',10),(85,15,'\\_\\_\\_\\_ is a visual diagram of a company that describes what employees do, whom they report to and how decisions are made.','____ is a visual diagram of a company that describes what employees do, whom they report to and how decisions are made.','Physical Structure','Organizational Structure','Logical Structure','Hybrid Structure','B',1,NULL,'2025-12-05 13:09:57.083798',10),(86,16,'\\_\\_\\_\\_ is a methodology used in system analysis to identify, clarify, and organize system requirements.','____ is a methodology used in system analysis to identify, clarify, and organize system requirements.','Workflow','Use case','Algorithm','Software','B',1,NULL,'2025-12-05 13:09:57.094476',10),(87,17,'Which of the following is \\textbf{not} an application of IoT?','Which of the following is not an application of IoT?','Web browser','Smart home','Smart city','Self-driven cars','A',1,NULL,'2025-12-05 13:09:57.104222',10),(88,18,'Which of the following is \\textbf{not} a cloud service option?','Which of the following is not a cloud service option?','VaaS','IaaS','PaaS','SaaS','A',1,NULL,'2025-12-05 13:09:57.112223',10),(89,19,'How many types of services are offered by cloud computing to the users?','How many types of services are offered by cloud computing to the users?','2','4','3','5','C',1,NULL,'2025-12-05 13:09:57.124294',10),(90,20,'Combination of Public and Private deployment is called','Combination of Public and Private deployment is called','Hybrid','Hyper','Public','Private','A',1,NULL,'2025-12-05 13:09:57.136098',10),(91,21,'Unit of electrical power is','Unit of electrical power is','Volt','Watt','Watt-hour','Ampere-hour','B',1,NULL,'2025-12-05 13:09:57.154232',11),(92,22,'In pipe earthing, the diameter of GI pipe embedded in the pit is','In pipe earthing, the diameter of GI pipe embedded in the pit is','32 mm','38 mm','48 mm','56 mm','B',1,NULL,'2025-12-05 13:09:57.164056',11),(93,23,'If a resistor of \\(100\\,\\Omega\\) is connected in series with a parallel combination of two \\(200\\,\\Omega\\) resistors, the effective resistance is','If a resistor of \\(100\\,\\Omega\\) is connected in series with a parallel combination of two \\(200\\,\\Omega\\) resistors, the effective resistance is','200 ohms','250 ohms','350 ohms','150 ohms','A',1,NULL,'2025-12-05 13:09:57.174597',11),(94,24,'If a resistor of \\(20\\,\\Omega\\) is connected across a source of \\(5\\text{ V}\\), the current in the circuit is','If a resistor of \\(20\\,\\Omega\\) is connected across a source of \\(5\\text{ V}\\), the current in the circuit is','1 Ampere','4 Amperes','0.5 Amperes','0.25 Amperes','A',1,NULL,'2025-12-05 13:09:57.185458',11),(95,25,'Power factor is','Power factor is','ratio of resistance to inductance','ratio of apparent power to true power','ratio of resistance to impedance','ratio of inductance to capacitance','C',1,NULL,'2025-12-05 13:09:57.195601',11),(96,26,'The phaseΓÇôneutral voltage in a 3-phase star system is \\(230\\text{ V}\\). The line voltage is','The phaseΓÇôneutral voltage in a 3-phase star system is \\(230\\text{ V}\\). The line voltage is','230 V','398.37 V','400 V','440 V','C',1,NULL,'2025-12-05 13:09:57.206294',11),(97,27,'The time period of an AC wave at \\(50\\text{ Hz}\\) is','The time period of an AC wave at \\(50\\text{ Hz}\\) is','2 ms','10 ms','20 ms','50 ms','B',1,NULL,'2025-12-05 13:09:57.216409',11),(98,28,'The type of fuse used for domestic purpose is','The type of fuse used for domestic purpose is','HRC fuse','Kit-kat fuse','Ceramic cartridge fuse','Glass cartridge fuse','C',1,NULL,'2025-12-05 13:09:57.226100',11),(99,29,'MCCB stands for','MCCB stands for','Moulded Case Circuit Breaker','Miniature Case Circuit Breaker','Maximum Current Circuit Breaker','Minimum Current Circuit Breaker','A',1,NULL,'2025-12-05 13:09:57.236214',11),(100,30,'ELCB is used for detecting current leakage','ELCB is used for detecting current leakage','above 8 kVA','below 5 kVA','above 5 kVA','below 8 kVA','C',1,NULL,'2025-12-05 13:09:57.244751',11),(101,31,'A static machine that transfers electrical power from one circuit to another without changing frequency is called','A static machine that transfers electrical power from one circuit to another without changing frequency is called','DC machine','Alternator','Induction motor','Transformer','D',1,NULL,'2025-12-05 13:09:57.255046',11),(102,32,'The initial type of connection of motor windings in a star-delta starter is','The initial type of connection of motor windings in a star-delta starter is','Star connection','Delta connection','Series','Parallel','A',1,NULL,'2025-12-05 13:09:57.263564',11),(103,33,'The cause for a 3-phase motor producing mechanical noise is','The cause for a 3-phase motor producing mechanical noise is','Interchanged supply terminals','High load on motor','High voltage on motor winding','Incorrect coupling','D',1,NULL,'2025-12-05 13:09:57.273905',11),(104,34,'Cell is an ______ device.','Cell is an ______ device.','electro-mechanical','electro-chemical','electro-magnetic','electro-dynamic','B',1,NULL,'2025-12-05 13:09:57.282527',11),(105,35,'The most commonly used battery in electric vehicles is','The most commonly used battery in electric vehicles is','Lithium-ion battery','Lead-acid battery','Nickel-Cadmium battery','Alkaline rechargeable battery','A',1,NULL,'2025-12-05 13:09:57.291587',11),(106,36,'Digital signals are characterized by','Digital signals are characterized by','Continuous voltage levels','Infinite resolution','Discrete voltage levels','Variable voltage levels','C',1,NULL,'2025-12-05 13:09:57.299477',11),(107,37,'According to Boolean Algebra, \\(A + A =\\)','According to Boolean Algebra, \\(A + A =\\)','2A','A','1','A^{2}','A',1,NULL,'2025-12-05 13:09:57.308471',11),(108,38,'Photo diode is used in which application?','Photo diode is used in which application?','Voltage regulation','Temperature measurement','Light detection','RF amplification','B',1,NULL,'2025-12-05 13:09:57.316807',11),(109,39,'If resistor band = Brown (1), Black (0), Red (\\(\\times 100\\)), resistance is','If resistor band = Brown (1), Black (0), Red (\\(\\times 100\\)), resistance is','1 k\\Omega','10 k\\Omega','100 \\Omega','100 k\\Omega','A',1,NULL,'2025-12-05 13:09:57.325274',11),(110,40,'Binary equivalent of decimal 9 is','Binary equivalent of decimal 9 is','1001','1000','1100','1010','A',1,NULL,'2025-12-05 13:09:57.335807',11),(111,41,'Project Management is a combination of','Project Management is a combination of','human and non-human resources','only human resources','only non-human resources','no resources at all','A',1,NULL,'2025-12-05 13:09:57.358281',12),(112,42,'The consultant appointed to carry out the project work is','The consultant appointed to carry out the project work is','Compound house consultant','In-house consultant','Out-house consultant','Bridge consultant','B',1,NULL,'2025-12-05 13:09:57.368789',12),(113,43,'The type of project which requires minimum amount of capital is','The type of project which requires minimum amount of capital is','Crash project','Normal project','Disaster project','Consultant project','A',1,NULL,'2025-12-05 13:09:57.378632',12),(114,44,'Projects like building a hospital, park, playground and highway construction are examples of','Projects like building a hospital, park, playground and highway construction are examples of','Social needs','Customer needs','Market needs','Ecological needs','A',1,NULL,'2025-12-05 13:09:57.386529',12),(115,45,'In Project Management, WBS stands for','In Project Management, WBS stands for','Work Breakdown Structure','Waste Breakdown Structure','Window Breakdown Structure','Wireless Breakdown Structure','A',1,NULL,'2025-12-05 13:09:57.394719',12),(116,46,'The first step in Project Execution Plan is','The first step in Project Execution Plan is','Work packaging plan','Contracting plan','Organization plan','Procedure plan','A',1,NULL,'2025-12-05 13:09:57.402498',12),(117,47,'The team which gives the idea to start a project is','The team which gives the idea to start a project is','Core project team','Full project team','Advising project team','Initial project team','A',1,NULL,'2025-12-05 13:09:57.410099',12),(118,48,'In PEP, the letter \'E\' stands for','In PEP, the letter \'E\' stands for','Execution','Estimation','Evaluation','Enthusiasm','A',1,NULL,'2025-12-05 13:09:57.418622',12),(119,49,'In Project Life Cycle, more time is required for','In Project Life Cycle, more time is required for','Project closure','Project initiation','Project execution','Project planning','C',1,NULL,'2025-12-05 13:09:57.426353',12),(120,50,'Innovation is the hallmark of every project. Innovation means','Innovation is the hallmark of every project. Innovation means','New ideas','Project success','Professional approach','Project Management','A',1,NULL,'2025-12-05 13:09:57.434780',12),(121,51,'The Project Life Cycle Curve indicates','The Project Life Cycle Curve indicates','Work packaging','Number of workers in the project','Growth, maturity and decline','Project manual','C',1,NULL,'2025-12-05 13:09:57.442897',12),(122,52,'Taking actions to measure the quality accurately is the function of','Taking actions to measure the quality accurately is the function of','Quality management','Cost management','Review management','Risk management','A',1,NULL,'2025-12-05 13:09:57.451436',12),(123,53,'Project planning methodologies involve','Project planning methodologies involve','Planning by non-incentive and direction','Planning by incentive and direction','Unplanned initiation','Changing the project policies','B',1,NULL,'2025-12-05 13:09:57.460434',12),(124,54,'Identify the incorrect statement','Identify the incorrect statement','Project objective should be specific','Project objective should be realistic','Project objective should not be framed timely','Project objective should be measurable','C',1,NULL,'2025-12-05 13:09:57.471169',12),(125,55,'WBS, PEP and PPM are the tools used to design','WBS, PEP and PPM are the tools used to design','Project plan','Project work system','Project diary','Project direction','A',1,NULL,'2025-12-05 13:09:57.479537',12),(126,56,'The earliest method used for planning of project was','The earliest method used for planning of project was','CPM','PERT','Bar Chart','Milestone Chart','A',1,NULL,'2025-12-05 13:09:57.488593',12),(127,57,'The expansion of PERT is','The expansion of PERT is','Programme Evaluation and Review Technique','Project Estimation and Recording Tool','Project Estimation and Resource Technology','Performance Estimation and Resource Tool','A',1,NULL,'2025-12-05 13:09:57.496098',12),(128,58,'For non-repetitive projects, ______ tool is used in production planning and scheduling','For non-repetitive projects, ______ tool is used in production planning and scheduling','CPM','PERT','Both CPM and PERT','Bar Chart','B',1,NULL,'2025-12-05 13:09:57.505766',12),(129,59,'The purpose of conducting a project review is','The purpose of conducting a project review is','To close the project','To initiate the project','To develop the project scope','To assess project performance','D',1,NULL,'2025-12-05 13:09:57.514943',12),(130,60,'A project review does not contain','A project review does not contain','Performance evaluation','Evaluating the capital budget','Data collection','Initial review','D',1,NULL,'2025-12-05 13:09:57.522957',12),(131,61,'In a square matrix, if the elements above the principal diagonal are zero, then it is called','In a square matrix, if the elements above the principal diagonal are zero, then it is called','Identity matrix','Lower triangular matrix','Upper triangular matrix','Diagonal matrix','C',1,NULL,'2025-12-05 13:09:57.537868',13),(132,62,'The value of x if \\( \\begin{vmatrix} x-1 & 2 \\\\ 2 & 4 \\end{vmatrix} \\) is singular','The value of x if determinant is singular','3','8','-2','2','C',1,NULL,'2025-12-05 13:09:57.546184',13),(133,63,'The inverse of the matrix \\( A=\\begin{bmatrix}-1&0\\\\5&7\\end{bmatrix} \\) is','The inverse of matrix A','\\( -\\frac{1}{7}\\begin{bmatrix}7&0\\\\-5&-1\\end{bmatrix} \\)','\\( \\frac{1}{7}\\begin{bmatrix}7&0\\\\-5&-1\\end{bmatrix} \\)','\\( -\\frac{1}{7}\\begin{bmatrix}-7&0\\\\-5&-1\\end{bmatrix} \\)','\\( \\frac{1}{7}\\begin{bmatrix}7&0\\\\5&1\\end{bmatrix} \\)','A',1,NULL,'2025-12-05 13:09:57.554714',13),(134,64,'The eigenvalues of matrix \\( A=\\begin{bmatrix}3&0\\\\1&3\\end{bmatrix} \\) are','Eigenvalues of matrix A','2,2','-3,-3','3,3','-3,3','C',1,NULL,'2025-12-05 13:09:57.562717',13),(135,65,'The two lines \\( ax+by=c \\) and \\( a\'x+b\'y=c\' \\) are perpendicular if','Condition of perpendicular lines','\\( ab\'=ba\' \\)','\\( aa\'+bb\'=0 \\)','\\( a\'b+a b\'=0 \\)','\\( ab\'+ba\'=0 \\)','B',1,NULL,'2025-12-05 13:09:57.574748',13),(136,66,'The y-intercept of any line passing through origin is','The y-intercept of a line through origin','0','1','-1','2','A',1,NULL,'2025-12-05 13:09:57.584631',13),(137,67,'Slope form of straight line is','Slope form','\\( y+mx-c=0 \\)','\\( x=my+c \\)','\\( y=x+m \\)','\\( y=mx+c \\)','D',1,NULL,'2025-12-05 13:09:57.594014',13),(138,68,'The tangent of the angle between two lines having slopes \\( m_1,m_2 \\) is','Tangent of angle between two lines','\\( \\frac{m_1+m_2}{1-m_1m_2} \\)','\\( \\frac{m_1+m_2}{1+m_1m_2} \\)','\\( \\frac{m_1-m_2}{1-m_1m_2} \\)','\\( \\frac{m_1-m_2}{1+m_1m_2} \\)','A',1,NULL,'2025-12-05 13:09:57.603026',13),(139,69,'If the ladder is inclined making \\(135^\\circ\\) with wall, the inclination in radians is','Convert angle to radians','\\( \\frac{4\\pi}{3} \\)','\\( \\frac{3\\pi}{4} \\)','\\( \\frac{2\\pi}{4} \\)','\\( \\frac{4\\pi}{5} \\)','B',1,NULL,'2025-12-05 13:09:57.613535',13),(140,70,'The value of \\( \\sin 60^\\circ \\cos 30^\\circ - \\cos 60^\\circ \\sin 30^\\circ \\) is','Trigonometric identity','\\( \\frac{1}{2} \\)','\\( -\\frac{1}{2} \\)','\\( \\frac{\\sqrt{3}}{2} \\)','0','D',1,NULL,'2025-12-05 13:09:57.623022',13),(141,71,'The simplified value of \\( \\frac{\\sin 3A + \\sin A}{\\sin 3A - \\sin A} \\) is','Simplify expression','\\( \\cot A \\tan 5A \\)','\\( \\tan A \\cot 2A \\)','\\( \\tan 2A \\cot A \\)','\\( \\tan 3A \\cot 2A \\)','B',1,NULL,'2025-12-05 13:09:57.634277',13),(142,72,'If \\( y=\\log x + \\sec 2x \\), then \\( \\frac{dy}{dx} \\) is','Differentiate y','\\( -\\frac{1}{x}+\\sec 2x \\tan x \\)','\\( \\frac{1}{x}+2\\sec 2x \\tan 2x \\)','\\( \\frac{1}{\\sqrt{x}}+\\sec x \\tan x \\)','\\( -\\frac{1}{\\sqrt{x}}+\\sec 3x \\tan 2x \\)','B',1,NULL,'2025-12-05 13:09:57.650097',13),(143,73,'The derivative of \\( \\frac{1+x}{1-x} \\) is','Differentiate function','\\( -\\frac{2}{(1-x)^2} \\)','\\( \\frac{2x}{(1-x)^2} \\)','\\( -\\frac{2x}{(1-x)^2} \\)','\\( \\frac{2}{(1-x)^2} \\)','A',1,NULL,'2025-12-05 13:09:57.660093',13),(144,74,'Find the second order derivative of \\( y=e^{2x}-e^{-x} \\)','Second derivative','\\( 4e^{2x}-e^{-x} \\)','\\( 4e^{2x}+e^{-x} \\)','\\( -4e^{2x}-e^{-x} \\)','\\( 4e^{2x}+e^x \\)','A',1,NULL,'2025-12-05 13:09:57.670272',13),(145,75,'Equation of tangent to \\( y=2x^2+x \\) at (1,2) is','Tangent equation','\\( 5x-y-3=0 \\)','\\( 5x+y+3=0 \\)','\\( 5x+y-6=0 \\)','\\( 5x+y+6=0 \\)','A',1,NULL,'2025-12-05 13:09:57.679859',13),(146,76,'The value of \\( \\int (\\sec x \\tan x + \\sec^2 x )dx \\) is','Evaluate integral','\\( \\sec 2x+\\tan x+c \\)','\\( \\sec x+\\cosec x+c \\)','\\( \\sec x+\\tan x+c \\)','\\( \\sec x- \\cosec^2 x+c \\)','C',1,NULL,'2025-12-05 13:09:57.689154',13),(147,77,'The value of \\( \\int (2x^3+3x^2+2x)^{10} (3x^2+3x+1)\\,dx \\) is','Evaluate integral','\\( \\frac{1}{22}(6x+3x^2+2x)^{11}+c \\)','\\( \\frac{1}{22}(2x^3+3x^2+2x)^{11}+c \\)','\\( \\frac{1}{22}(2x^3+3x^2-2x)^{12}+c \\)','\\( \\frac{1}{12}(2x^3+3x^2-2x)^{12}+c \\)','B',1,NULL,'2025-12-05 13:09:57.698711',13),(148,78,'The value of \\( \\int_0^{\\pi/4}\\tan^2 x\\,dx \\) is','Evaluate definite integral','\\( 1+\\frac{\\pi}{4} \\)','\\( 1+\\frac{4\\pi}{2} \\)','\\( 1-\\frac{\\pi}{4} \\)','\\( 1-\\frac{4\\pi}{2} \\)','A',1,NULL,'2025-12-05 13:09:57.711795',13),(149,79,'Area bounded by \\( y=\\sin x \\) and x-axis from \\( x=0 \\) to \\( x=\\pi \\) is','Area under curve','2','-2','3','1','A',1,NULL,'2025-12-05 13:09:57.724901',13),(150,80,'The value of \\( \\tan 45^\\circ \\cot 225^\\circ + \\tan^2 60^\\circ \\) is','Simplify expression','-4','4','2','3','C',1,NULL,'2025-12-05 13:09:57.734688',13),(151,81,'_____ is an example of quantitative data.','_____ is an example of quantitative data.','Volume','Words','Symbols','Colour','A',1,NULL,'2025-12-05 13:09:57.756045',14),(152,82,'Data cleaning is the process of','Data cleaning is the process of','removing viruses','correctly formatting data','removing duplicate data','properly formatting data','B',1,NULL,'2025-12-05 13:09:57.766570',14),(153,83,'_____ is not a data collection tool.','_____ is not a data collection tool.','Word','Focus Group Discussion','Survey','Questionnaire','B',1,NULL,'2025-12-05 13:09:57.776092',14),(154,84,'The graph of cumulative frequency is called','The graph of cumulative frequency is called','Frequency polygon','Histogram','Cumulative frequency polygon','Frequency histogram','C',1,NULL,'2025-12-05 13:09:57.787823',14),(155,85,'To calculate percentage frequency, we use _____ formula.','To calculate percentage frequency, we use _____ formula.','P.f. = (f ├ù n) ├╖ 100','P.f. = (f ├╖ n) ├ù 100','P.f. = (100) ├╖ (f ├ù n)','P.f. = (100) ├ù (f ├╖ n)','B',1,NULL,'2025-12-05 13:09:57.799142',14),(156,86,'If XΓéü, XΓéé, XΓéâ ... XΓéÖ are the observations of a given data, then the mean will be:','If XΓéü, XΓéé, XΓéâ ... XΓéÖ are the observations of a given data, then the mean will be:','$$\\\\frac{\\\\text{Total number of observations}}{\\\\text{Sum of observations}}$$','Sum of observations + Total number of observations','$$\\\\frac{\\\\text{Sum of observations}}{\\\\text{Total number of observations}}$$','Total number of observations ΓêÆ Sum of observations','C',1,NULL,'2025-12-05 13:09:57.812029',14),(157,87,'The end points of a class interval are the _____ and _____ values a variable can take.','The end points of a class interval are the _____ and _____ values a variable can take.','Lowest and Highest','Minimum and Maximum','Numeral and Average','Mean and Mode','B',1,NULL,'2025-12-05 13:09:57.823801',14),(158,88,'In which years did the girls participate more than the boys?','In which years did the girls participate more than the boys?','2020, 2023','2021, 2022','2022, 2023','2020, 2021','B',1,NULL,'2025-12-05 13:09:57.833577',14),(159,89,'In which two years did an equal number of boys participate?','In which two years did an equal number of boys participate?','2020, 2021','2020, 2022','2020, 2023','2021, 2022','D',1,NULL,'2025-12-05 13:09:57.843110',14),(160,90,'To find third quartile in Excel, we use _____ formula.','To find third quartile in Excel, we use _____ formula.','= QUARTER (3, Range)','= QUARTILE (3, Range)','= QUARTER (Range, 3)','= QUARTILE (Range, 3)','D',1,NULL,'2025-12-05 13:09:57.852668',14),(161,91,'The percentile divides a series into _____ equal parts.','The percentile divides a series into _____ equal parts.','fifty','twenty','ten','hundred','D',1,NULL,'2025-12-05 13:09:57.862510',14),(162,92,'If the first quartile is 23 and interquartile range is 20, the third quartile is','If the first quartile is 23 and interquartile range is 20, the third quartile is','23','33','43','53','C',1,NULL,'2025-12-05 13:09:57.871395',14),(163,93,'The algebraic sum of the deviations of a frequency distribution from its mean is always','The algebraic sum of the deviations of a frequency distribution from its mean is always','a non-zero number','zero','less than zero','greater than zero','B',1,NULL,'2025-12-05 13:09:57.880484',14),(164,94,'The Excel formula for ΓÇÿMeanΓÇÖ is','The Excel formula for ΓÇÿMeanΓÇÖ is','= MEDIAN (array of numbers)','= AVERAGE (array of numbers)','= MEAN (array of numbers)','= MODE (array of numbers)','B',1,NULL,'2025-12-05 13:09:57.890220',14),(165,95,'What is output syntax in Python?','What is output syntax in Python?','Print()','PRINT()','print()','Printf()','C',1,NULL,'2025-12-05 13:09:57.900004',14),(166,96,'\'str\' is a','\'str\' is a','Text Type','Numeric Type','Binary Type','Sequence Type','B',1,NULL,'2025-12-05 13:09:57.908999',14),(167,97,'In Python, _____ standard data types are commonly used.','In Python, _____ standard data types are commonly used.','three','five','ten','four','B',1,NULL,'2025-12-05 13:09:57.917535',14),(168,98,'The result of Python program gets displayed in _____','The result of Python program gets displayed in _____','IDLE Shell 3.9.1 window','IDLE Shell 3.1.9 window','ILDE Shell 3.9.1 window','IELD Shell 3.9.1 window','A',1,NULL,'2025-12-05 13:09:57.925911',14),(169,99,'Which Python quotation does not accept quotes to denote strings?','Which Python quotation does not accept quotes to denote strings?','(\' \')','(\\ \\\")\"','( )','(\\\\\" \\\"\\\")\"','C',1,NULL,'2025-12-05 13:09:57.937251',14),(170,100,'In Python, _____ is used to end the physical line or ignore the comment.','In Python, _____ is used to end the physical line or ignore the comment.','**','#','&','\\\\\\\\','B',1,NULL,'2025-12-05 13:09:57.945790',14);
/*!40000 ALTER TABLE `questions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sections`
--

DROP TABLE IF EXISTS `sections`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sections` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `order` int NOT NULL,
  `max_marks` int NOT NULL,
  `exam_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sections_exam_id_order_a6ebc477_uniq` (`exam_id`,`order`),
  KEY `sections_exam_id_2ab103_idx` (`exam_id`,`order`),
  CONSTRAINT `sections_exam_id_8eac4054_fk_exams_id` FOREIGN KEY (`exam_id`) REFERENCES `exams` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sections`
--

LOCK TABLES `sections` WRITE;
/*!40000 ALTER TABLE `sections` DISABLE KEYS */;
INSERT INTO `sections` (`id`, `name`, `order`, `max_marks`, `exam_id`) VALUES (10,'IT Skills',1,20,6),(11,'FUNDAMENTALS OF ELECTRICAL & ELECTRONICS ENGINEERING',2,20,6),(12,'PROJECT MANAGEMENT SKILLS',3,20,6),(13,'ENGINEERING MATHEMATICS',4,20,6),(14,'STATISTICS & ANALYTICS',5,20,6);
/*!40000 ALTER TABLE `sections` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_activity`
--

DROP TABLE IF EXISTS `user_activity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_activity` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `activity` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ip_address` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_agent` longtext COLLATE utf8mb4_unicode_ci,
  `created_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_activity_user_id_9d5b7120_fk_users_id` (`user_id`),
  CONSTRAINT `user_activity_user_id_9d5b7120_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_activity`
--

LOCK TABLES `user_activity` WRITE;
/*!40000 ALTER TABLE `user_activity` DISABLE KEYS */;
INSERT INTO `user_activity` (`id`, `activity`, `ip_address`, `user_agent`, `created_at`, `user_id`) VALUES (1,'User logged in','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36','2025-12-04 17:45:40.469934',3),(2,'User logged in','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36','2025-12-04 18:10:49.804891',3),(3,'User logged in','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36','2025-12-04 19:12:14.177329',4),(4,'User logged in','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36','2025-12-05 13:13:28.460638',4),(5,'User logged in','127.0.0.1','Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36','2025-12-05 13:36:24.103446',3),(6,'User logged in','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36','2025-12-05 13:38:03.431993',4),(7,'User logged in','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36','2025-12-05 13:43:48.167758',4),(8,'User logged in','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36','2025-12-05 15:00:25.834659',4),(9,'User logged in','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36','2025-12-05 19:22:52.745017',4),(10,'User logged in','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36','2025-12-05 19:32:43.811072',4),(11,'User logged in','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36','2025-12-05 19:33:09.804412',4),(12,'User logged in','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36','2025-12-05 20:55:31.376029',4),(13,'User logged in','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36','2025-12-05 21:19:29.796940',4),(14,'User logged in','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36','2025-12-09 20:07:10.241639',4);
/*!40000 ALTER TABLE `user_activity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `username` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `password_hash` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email_verified` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`),
  KEY `users_usernam_baeb4b_idx` (`username`),
  KEY `users_email_4b85f2_idx` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` (`id`, `username`, `email`, `phone`, `password_hash`, `email_verified`, `created_at`, `updated_at`) VALUES (1,'demo2','demo2@gmail.com','','pbkdf2_sha256$600000$TbbyMVOtYhAWLSIrZfZ9vH$a2DElmFGeyyRkp0El1AMAfkwV47O4LQuS22B52Ha24c=',0,'2025-12-04 17:22:28.462596','2025-12-04 17:22:29.232971'),(2,'demo3','demo3@gmail.com','','pbkdf2_sha256$600000$5UhV0KhyJwPPF3dbGmBQPN$xIPCsckVfE9yfuR3JRNSwJL5hd3X3RmzTWaDDugQ1rY=',0,'2025-12-04 17:26:41.945424','2025-12-04 17:26:42.831574'),(3,'demo4','demo4@gmail.com','','pbkdf2_sha256$600000$mnRjlOkUOYPpKPrTwpNM9r$IJO6hnAkRAmneOx2W4tCGzaED8Ci7OKzWlqNHfdGBpE=',0,'2025-12-04 17:28:38.359421','2025-12-04 17:28:39.179260'),(4,'demo5','demo5@gmail.com','','pbkdf2_sha256$600000$wTDJ7XQWRxkVDHcgtmIycI$uvbxt1tBo5SL29Jhqn16lqiCvPwvuZ8b6NZpXaPQRsQ=',0,'2025-12-04 17:31:06.269829','2025-12-04 17:31:07.201681'),(5,'testuser','test@example.com',NULL,'pbkdf2_sha256$1000000$OvWqcPz4izPmW4UoxjzXis$7DtTiH2GXEyDBhBUYSm5JMFALtLoPip4o+7eAnFvhag=',0,'2025-12-09 19:43:25.607693','2025-12-09 19:43:25.607693');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'dcet_platform'
--

--
-- Dumping routines for database 'dcet_platform'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-12 11:23:10
