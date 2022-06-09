-- MySQL dump 10.13  Distrib 8.0.15, for Win64 (x86_64)
--
-- Host: localhost    Database: DB_TEST
-- ------------------------------------------------------
-- Server version	8.0.15

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `notas_fiscais`
--

DROP TABLE IF EXISTS `notas_fiscais`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `notas_fiscais` (
  `CPF` varchar(11) NOT NULL,
  `MATRICULA` varchar(5) NOT NULL,
  `DATA_VENDA` date DEFAULT NULL,
  `NUMERO` int(11) NOT NULL,
  `IMPOSTO` float NOT NULL,
  PRIMARY KEY (`NUMERO`),
  KEY `MATRICULA` (`MATRICULA`),
  KEY `CPF` (`CPF`),
  CONSTRAINT `notas_fiscais_ibfk_1` FOREIGN KEY (`MATRICULA`) REFERENCES `tabela_de_vendedores` (`MATRICULA`)
  ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `notas_fiscais_ibfk_2` FOREIGN KEY (`CPF`) REFERENCES `tabela_de_clientes` (`CPF`)
  ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;
