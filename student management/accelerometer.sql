-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 11, 2021 at 01:03 PM
-- Server version: 10.4.11-MariaDB
-- PHP Version: 7.2.29

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `accelerometerDatas`
--

-- --------------------------------------------------------

--
-- Table structure for table `attendence`
--

CREATE TABLE `analytics` (
  `aid` int(11) NOT NULL,
  `XAxis` float NOT NULL,
  `YAxis` float NOT NULL,
  `ZAxis` float NOT NULL,
  `name` float NOT NULL,
  `value` int(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `data_source`
--

CREATE TABLE `data_source` (
  `cid` int(11) NOT NULL,
  `source_name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `data_source`
--

INSERT INTO `data_source` (`cid`, `source_name`) VALUES
(2, 'Manual Web'),
(3, 'Android'),
(4, 'iPhone'),
(5, 'Raspberry Pi '),
(7, 'Other IOT'),
(8, 'Others');

-- --------------------------------------------------------

--
-- Table structure for table `accelerometerData`
--

CREATE TABLE `accelerometerData` (
  `id` int(11) NOT NULL,
  `XAxis` float NOT NULL,
  `YAxis` float NOT NULL,
  `ZAxis` float NOT NULL,
  `latitude` float NOT NULL,
  `longitude` float NOT NULL,
  `source_name` varchar(100) NOT NULL,
  `datetime` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Triggers `accelerometerData`
--
DELIMITER $$
CREATE TRIGGER `DELETE` BEFORE DELETE ON `accelerometerData` FOR EACH ROW INSERT INTO trig VALUES(null,OLD.XAxis,'AccelerometerData DELETED',NOW())
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `Insert` AFTER INSERT ON `accelerometerData` FOR EACH ROW INSERT INTO trig VALUES(null,NEW.XAxis,'AccelerometerData INSERTED',NOW())
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `UPDATE` AFTER UPDATE ON `accelerometerData` FOR EACH ROW INSERT INTO trig VALUES(null,NEW.XAxis,'AccelerometerData UPDATED',NOW())
$$
DELIMITER ;


CREATE TABLE `trig` (
  `tid` int(11) NOT NULL,
  `XAxis` float NOT NULL,
  `action` varchar(50) NOT NULL,
  `timestamp` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `email`, `password`) VALUES
(4, 'devangnithin', 'devangnithin@gmail.com', 'pbkdf2:sha256:260000$ILaEVx41Q4jJw7EF$242a8f67c5a01c65b8675886eca540f1afa02356ae67dcd8bf92f8096196cf98');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `attendence`
--
ALTER TABLE `attendence`
  ADD PRIMARY KEY (`aid`);

--
-- Indexes for table `data_source`
--
ALTER TABLE `data_source`
  ADD PRIMARY KEY (`cid`);

--
-- Indexes for table `accelerometerData`
--
ALTER TABLE `accelerometerData`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `trig`
--
ALTER TABLE `trig`
  ADD PRIMARY KEY (`tid`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `attendence`
--
ALTER TABLE `attendence`
  MODIFY `aid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `data_source`
--
ALTER TABLE `data_source`
  MODIFY `cid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `accelerometerData`
--
ALTER TABLE `accelerometerData`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;


--
-- AUTO_INCREMENT for table `trig`
--
ALTER TABLE `trig`
  MODIFY `tid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
