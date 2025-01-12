-- MySQL dump 10.13  Distrib 8.0.40, for Linux (x86_64)
--
-- Host: localhost    Database: Certifier_db
-- ------------------------------------------------------
-- Server version	8.0.40-0ubuntu0.22.04.1

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add user',6,'add_customuser'),(22,'Can change user',6,'change_customuser'),(23,'Can delete user',6,'delete_customuser'),(24,'Can view user',6,'view_customuser');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `certifier_app_customuser`
--

DROP TABLE IF EXISTS `certifier_app_customuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `certifier_app_customuser` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `email` varchar(50) NOT NULL,
  `is_deleted` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `certifier_app_customuser`
--

LOCK TABLES `certifier_app_customuser` WRITE;
/*!40000 ALTER TABLE `certifier_app_customuser` DISABLE KEYS */;
INSERT INTO `certifier_app_customuser` VALUES (2,'pbkdf2_sha256$720000$pBgxv8FlAccuaic8io7VGu$qthyWIYGjOXUiVV2b4+mNcQpdNOqBDywZQGrJlkIUuU=','2025-01-06 11:47:47.945429',0,'Shantanu','Gupta',0,1,'2024-12-23 22:27:10.122547','shantanugupta13524@gmail.com',NULL),(3,'pbkdf2_sha256$720000$Oj5jvYBIdKhBTvDHlDSRPe$lIlK6S+6YvEo3fx1kIG3XhTkUzeXpp2nswRoSsOzT04=',NULL,0,'Prince','Kushwaha',0,1,'2024-12-24 00:12:58.113700','prince@gmail.com',NULL);
/*!40000 ALTER TABLE `certifier_app_customuser` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `certifier_app_customuser_groups`
--

DROP TABLE IF EXISTS `certifier_app_customuser_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `certifier_app_customuser_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customuser_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `certifier_app_customuser_customuser_id_group_id_368b9860_uniq` (`customuser_id`,`group_id`),
  KEY `certifier_app_custom_group_id_e9e11f26_fk_auth_grou` (`group_id`),
  CONSTRAINT `certifier_app_custom_customuser_id_0f9b0609_fk_certifier` FOREIGN KEY (`customuser_id`) REFERENCES `certifier_app_customuser` (`id`),
  CONSTRAINT `certifier_app_custom_group_id_e9e11f26_fk_auth_grou` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `certifier_app_customuser_groups`
--

LOCK TABLES `certifier_app_customuser_groups` WRITE;
/*!40000 ALTER TABLE `certifier_app_customuser_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `certifier_app_customuser_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `certifier_app_customuser_user_permissions`
--

DROP TABLE IF EXISTS `certifier_app_customuser_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `certifier_app_customuser_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customuser_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `certifier_app_customuser_customuser_id_permission_bef2740b_uniq` (`customuser_id`,`permission_id`),
  KEY `certifier_app_custom_permission_id_d09f9727_fk_auth_perm` (`permission_id`),
  CONSTRAINT `certifier_app_custom_customuser_id_4f907b2b_fk_certifier` FOREIGN KEY (`customuser_id`) REFERENCES `certifier_app_customuser` (`id`),
  CONSTRAINT `certifier_app_custom_permission_id_d09f9727_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `certifier_app_customuser_user_permissions`
--

LOCK TABLES `certifier_app_customuser_user_permissions` WRITE;
/*!40000 ALTER TABLE `certifier_app_customuser_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `certifier_app_customuser_user_permissions` ENABLE KEYS */;
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
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_certifier_app_customuser_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_certifier_app_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `certifier_app_customuser` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(6,'certifier_app','customuser'),(4,'contenttypes','contenttype'),(5,'sessions','session');
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
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2024-12-23 20:03:15.563507'),(2,'contenttypes','0002_remove_content_type_name','2024-12-23 20:03:15.856900'),(3,'auth','0001_initial','2024-12-23 20:03:17.112220'),(4,'auth','0002_alter_permission_name_max_length','2024-12-23 20:03:17.409838'),(5,'auth','0003_alter_user_email_max_length','2024-12-23 20:03:17.428963'),(6,'auth','0004_alter_user_username_opts','2024-12-23 20:03:17.448518'),(7,'auth','0005_alter_user_last_login_null','2024-12-23 20:03:17.469028'),(8,'auth','0006_require_contenttypes_0002','2024-12-23 20:03:17.482735'),(9,'auth','0007_alter_validators_add_error_messages','2024-12-23 20:03:17.501867'),(10,'auth','0008_alter_user_username_max_length','2024-12-23 20:03:17.520202'),(11,'auth','0009_alter_user_last_name_max_length','2024-12-23 20:03:17.540751'),(12,'auth','0010_alter_group_name_max_length','2024-12-23 20:03:17.589417'),(13,'auth','0011_update_proxy_permissions','2024-12-23 20:03:17.609974'),(14,'auth','0012_alter_user_first_name_max_length','2024-12-23 20:03:17.624457'),(15,'certifier_app','0001_initial','2024-12-23 20:03:19.141023'),(16,'admin','0001_initial','2024-12-23 20:03:19.758161'),(17,'admin','0002_logentry_remove_auto_add','2024-12-23 20:03:19.780587'),(18,'admin','0003_logentry_add_action_flag_choices','2024-12-23 20:03:19.801487'),(19,'sessions','0001_initial','2024-12-23 20:03:19.971890'),(20,'certifier_app','0002_remove_customuser_username','2024-12-23 20:11:58.956795');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('13ucfpxfr11srnn59pduv5cjmlq9dc1w','.eJxVjDsOwjAQBe_iGlleJ_GHkp4zWLveNQ6gRIqTCnF3iJQC2jcz76USbmtNW5MljazOyqrT70aYHzLtgO843Wad52ldRtK7og_a9HVmeV4O9--gYqvfOoKEDtggFO-d9XnofYEQ-whoQl_MgIJMlGFgE6Ewu05KcM53ljKJen8A0SQ4Bw:1tUReR:JXLQ4YyxAQ5_bTxMQ8LPMR1u1mYZgm2J3mCLVaWjdoI','2025-01-19 20:00:47.555780'),('1qtgro7m24rbsjkhmmx128i3bq9n248u','.eJxVjDsOwjAQBe_iGlleJ_GHkp4zWLveNQ6gRIqTCnF3iJQC2jcz76USbmtNW5MljazOyqrT70aYHzLtgO843Wad52ldRtK7og_a9HVmeV4O9--gYqvfOoKEDtggFO-d9XnofYEQ-whoQl_MgIJMlGFgE6Ewu05KcM53ljKJen8A0SQ4Bw:1tRFDs:eVogBWJUzKDIFE-DeOWLkXNEnTcXu-Js2rstAExLYZQ','2025-01-11 00:08:08.990553'),('ai05ohkt7a8u1m6j6ojfb2owfgj2f7zu','.eJxVjDsOwjAQBe_iGlleJ_GHkp4zWLveNQ6gRIqTCnF3iJQC2jcz76USbmtNW5MljazOyqrT70aYHzLtgO843Wad52ldRtK7og_a9HVmeV4O9--gYqvfOoKEDtggFO-d9XnofYEQ-whoQl_MgIJMlGFgE6Ewu05KcM53ljKJen8A0SQ4Bw:1tQnhC:jgs7FCucr_58qSWpzHoOx8gDcjYe6gMmfNiXyE_lRxs','2025-01-09 18:44:34.179238'),('cln3aim2i949f8pzk2n0yme4b312pb4t','.eJxVjDsOwjAQBe_iGlleJ_GHkp4zWLveNQ6gRIqTCnF3iJQC2jcz76USbmtNW5MljazOyqrT70aYHzLtgO843Wad52ldRtK7og_a9HVmeV4O9--gYqvfOoKEDtggFO-d9XnofYEQ-whoQl_MgIJMlGFgE6Ewu05KcM53ljKJen8A0SQ4Bw:1tQnl5:vhRgnk2nUll8Xr053xUyecrniu7jCLwwt90plUMpsJM','2025-01-09 18:48:35.234066'),('i6r4jcuzdwarpql3uem5elgwyqi3882g','.eJxVjDsOwjAQBe_iGlleJ_GHkp4zWLveNQ6gRIqTCnF3iJQC2jcz76USbmtNW5MljazOyqrT70aYHzLtgO843Wad52ldRtK7og_a9HVmeV4O9--gYqvfOoKEDtggFO-d9XnofYEQ-whoQl_MgIJMlGFgE6Ewu05KcM53ljKJen8A0SQ4Bw:1tQnPI:Zshj5oObEMD3isfPyX63xlI56jz5mq928cVQXQgVBeE','2025-01-09 18:26:04.435284'),('lbqupi7deoaql0fw97wc5kx9ut2jo6to','.eJxVjDsOwjAQBe_iGlleJ_GHkp4zWLveNQ6gRIqTCnF3iJQC2jcz76USbmtNW5MljazOyqrT70aYHzLtgO843Wad52ldRtK7og_a9HVmeV4O9--gYqvfOoKEDtggFO-d9XnofYEQ-whoQl_MgIJMlGFgE6Ewu05KcM53ljKJen8A0SQ4Bw:1tR34L:sBVVuaaRq56LKrGMqZtXRcXyGLfSAJof1u4PQVgZzOI','2025-01-10 11:09:29.498399'),('mwee4iozlu8p7vnfdd91swecliurgjxm','.eJxVjDsOwjAQBe_iGlleJ_GHkp4zWLveNQ6gRIqTCnF3iJQC2jcz76USbmtNW5MljazOyqrT70aYHzLtgO843Wad52ldRtK7og_a9HVmeV4O9--gYqvfOoKEDtggFO-d9XnofYEQ-whoQl_MgIJMlGFgE6Ewu05KcM53ljKJen8A0SQ4Bw:1tQnXl:rZm46hgE6gA3fEanCJkz_j3jAvGR7WLIRWtnZCN5whc','2025-01-09 18:34:49.482104'),('r7bl09rk3imaz1mlp8h7bmdyj8zqjyj1','.eJxVjDsOwjAQBe_iGlleJ_GHkp4zWLveNQ6gRIqTCnF3iJQC2jcz76USbmtNW5MljazOyqrT70aYHzLtgO843Wad52ldRtK7og_a9HVmeV4O9--gYqvfOoKEDtggFO-d9XnofYEQ-whoQl_MgIJMlGFgE6Ewu05KcM53ljKJen8A0SQ4Bw:1tUgQu:MJGAbM6BjrRQIVeEBjzPH7Cq198NnrGVnjQ662fWuIA','2025-01-20 11:47:48.099534'),('u4tpop5c9iklfcd3hjgtga1bfgmbdy9z','.eJxVjDsOwjAQBe_iGlleJ_GHkp4zWLveNQ6gRIqTCnF3iJQC2jcz76USbmtNW5MljazOyqrT70aYHzLtgO843Wad52ldRtK7og_a9HVmeV4O9--gYqvfOoKEDtggFO-d9XnofYEQ-whoQl_MgIJMlGFgE6Ewu05KcM53ljKJen8A0SQ4Bw:1tUWJs:RBAjQ8cC8Rt9mN-QSv0GfU3jdokJ8UaSeMOqRmfxbf4','2025-01-20 00:59:52.877594'),('ukg7wxw89g3tor78lyy3v3m2pop7hx9e','.eJxVjDsOwjAQBe_iGlleJ_GHkp4zWLveNQ6gRIqTCnF3iJQC2jcz76USbmtNW5MljazOyqrT70aYHzLtgO843Wad52ldRtK7og_a9HVmeV4O9--gYqvfOoKEDtggFO-d9XnofYEQ-whoQl_MgIJMlGFgE6Ewu05KcM53ljKJen8A0SQ4Bw:1tQsOH:pQVTLl_-D5qNrSUj1D6DQdygGmYTDq9VnkN8SsWA43c','2025-01-09 23:45:21.998187'),('yin1k3wuo2zej61a24sm1art3le1g4py','.eJxVjDsOwjAQBe_iGlleJ_GHkp4zWLveNQ6gRIqTCnF3iJQC2jcz76USbmtNW5MljazOyqrT70aYHzLtgO843Wad52ldRtK7og_a9HVmeV4O9--gYqvfOoKEDtggFO-d9XnofYEQ-whoQl_MgIJMlGFgE6Ewu05KcM53ljKJen8A0SQ4Bw:1tQngO:n3bH-mYR_MKaqqj6pdGgXgKoTZ6HCCtjSpSKowjqGoY','2025-01-09 18:43:44.969896');
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

-- Dump completed on 2025-01-06 11:49:06
