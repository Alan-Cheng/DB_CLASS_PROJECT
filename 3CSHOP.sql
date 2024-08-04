-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- 主機： localhost
-- 產生時間： 2024 年 08 月 04 日 15:11
-- 伺服器版本： 10.4.28-MariaDB
-- PHP 版本： 8.0.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫： `3CSHOP`
--

-- --------------------------------------------------------

--
-- 資料表結構 `CART`
--

CREATE TABLE `CART` (
  `CID` int(11) NOT NULL,
  `MID` int(11) DEFAULT NULL,
  `CTIME` datetime DEFAULT NULL,
  `tNo` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `CART`
--

INSERT INTO `CART` (`CID`, `MID`, `CTIME`, `tNo`) VALUES
(2, 1, '2024-07-27 17:29:20', 2),
(3, 1, '2024-07-27 17:52:37', 3),
(4, 1, '2024-07-27 17:52:57', 4),
(5, 1, '2024-07-27 17:58:05', 5),
(6, 2, '2024-07-27 17:59:30', 6),
(7, 1, '2024-07-27 18:01:28', 7),
(8, 1, '2024-07-27 18:01:33', 8),
(9, 1, '2024-07-27 18:05:43', 14),
(10, 2, '2024-07-27 18:06:49', 9),
(11, 4, '2024-07-29 08:06:30', 10),
(12, 4, '2024-07-29 08:06:54', 11),
(13, 4, '2024-07-29 08:23:44', 12),
(14, 4, '2024-07-29 08:24:00', 13),
(15, 1, '2024-08-04 21:10:23', NULL),
(16, 2, '2024-08-04 21:10:40', NULL);

-- --------------------------------------------------------

--
-- 資料表結構 `CONTAIN`
--

CREATE TABLE `CONTAIN` (
  `CID` int(11) NOT NULL,
  `UNITS` int(11) DEFAULT NULL,
  `PID` varchar(256) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `CONTAIN`
--

INSERT INTO `CONTAIN` (`CID`, `UNITS`, `PID`) VALUES
(2, 1, 'v83707'),
(3, 1, 'v83707'),
(4, 1, 'v83707'),
(5, 3, 'v83707'),
(6, 2, 'v83707'),
(7, 1, 'T59874'),
(8, 1, 'v83707'),
(9, 1, 'C37370'),
(10, 2, 'T59874'),
(10, 1, 'v83707'),
(11, 5, 'v83707'),
(12, 5, 'v83707'),
(13, 1, 'T59874'),
(13, 1, 'v83707'),
(14, 1, 'T59874'),
(14, 1, 'v83707'),
(16, 1, 'T59874');

-- --------------------------------------------------------

--
-- 資料表結構 `MEMBER`
--

CREATE TABLE `MEMBER` (
  `MID` int(11) NOT NULL,
  `NAME` varchar(128) DEFAULT NULL,
  `ACCOUNT` varchar(128) NOT NULL,
  `PASSWORD` varchar(128) DEFAULT NULL,
  `IDENTITY` varchar(128) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `MEMBER`
--

INSERT INTO `MEMBER` (`MID`, `NAME`, `ACCOUNT`, `PASSWORD`, `IDENTITY`) VALUES
(1, 'Alan', 'alan', 'test', 'user'),
(2, 'Yuyu', 'yuyu', 'test', 'user'),
(3, 'Admin', 'admin', 'test', 'manager'),
(4, 'Sam', 'sam', 'test', 'user');

-- --------------------------------------------------------

--
-- 資料表結構 `PRODUCT`
--

CREATE TABLE `PRODUCT` (
  `PID` varchar(256) NOT NULL,
  `PNAME` varchar(128) DEFAULT NULL,
  `PRICE` decimal(10,2) DEFAULT NULL,
  `SNAME` varchar(128) DEFAULT NULL,
  `PDESC` text DEFAULT NULL,
  `PIMAGE` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `PRODUCT`
--

INSERT INTO `PRODUCT` (`PID`, `PNAME`, `PRICE`, `SNAME`, `PDESC`, `PIMAGE`) VALUES
('C37370', 'Sony VAIO', 40000.00, 'Sony VAIO', 'Soooooo gooood', 'C37370.jpg'),
('T59874', 'VIVOBOOK', 20000.00, 'ASUS', '好電腦不買嗎？', 'T59874.png'),
('v83707', 'Macbook', 30000.00, 'Apple 蘋果👍', 'Macbook is good!!!', 'v83707.jpeg');

-- --------------------------------------------------------

--
-- 資料表結構 `RECORD`
--

CREATE TABLE `RECORD` (
  `TNO` int(11) NOT NULL,
  `PID` varchar(256) NOT NULL,
  `AMOUNT` int(11) DEFAULT NULL,
  `SALEPRICE` decimal(10,2) DEFAULT NULL,
  `TOTAL` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `RECORD`
--

INSERT INTO `RECORD` (`TNO`, `PID`, `AMOUNT`, `SALEPRICE`, `TOTAL`) VALUES
(6, 'v83707', 2, 30000.00, 60000.00),
(8, 'v83707', 1, 30000.00, 30000.00),
(9, 'T59874', 2, 20000.00, 40000.00),
(9, 'v83707', 1, 30000.00, 30000.00),
(12, 'T59874', 1, 20000.00, 20000.00),
(12, 'v83707', 1, 30000.00, 30000.00),
(13, 'T59874', 1, 20000.00, 20000.00),
(13, 'v83707', 1, 30000.00, 30000.00),
(14, 'C37370', 1, 40000.00, 40000.00);

-- --------------------------------------------------------

--
-- 資料表結構 `SUPPLIER`
--

CREATE TABLE `SUPPLIER` (
  `SNAME` varchar(256) NOT NULL,
  `SDESC` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `SUPPLIER`
--

INSERT INTO `SUPPLIER` (`SNAME`, `SDESC`) VALUES
('Apple 蘋果👍', 'An apple a day keeps the doctor away.'),
('ASUS', '堅如磐石？'),
('Sony VAIO', 'SOOOOORY');

-- --------------------------------------------------------

--
-- 資料表結構 `TRANSACTION`
--

CREATE TABLE `TRANSACTION` (
  `TNO` int(11) NOT NULL,
  `MID` int(11) DEFAULT NULL,
  `TTIME` datetime DEFAULT NULL,
  `CID` int(11) DEFAULT NULL,
  `PAYMENT` varchar(256) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `TRANSACTION`
--

INSERT INTO `TRANSACTION` (`TNO`, `MID`, `TTIME`, `CID`, `PAYMENT`) VALUES
(6, 2, '2024-07-27 17:59:34', 6, '轉帳'),
(8, 1, '2024-07-27 18:01:35', 8, '轉帳'),
(9, 2, '2024-07-27 18:13:24', 10, '轉帳'),
(12, 4, '2024-07-29 08:23:51', 13, '轉帳'),
(13, 4, '2024-07-29 08:24:21', 14, '轉帳'),
(14, 1, '2024-07-31 11:51:56', 9, '轉帳');

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `CART`
--
ALTER TABLE `CART`
  ADD PRIMARY KEY (`CID`);

--
-- 資料表索引 `CONTAIN`
--
ALTER TABLE `CONTAIN`
  ADD PRIMARY KEY (`CID`,`PID`);

--
-- 資料表索引 `MEMBER`
--
ALTER TABLE `MEMBER`
  ADD PRIMARY KEY (`MID`),
  ADD UNIQUE KEY `ACCOUNT` (`ACCOUNT`);

--
-- 資料表索引 `PRODUCT`
--
ALTER TABLE `PRODUCT`
  ADD PRIMARY KEY (`PID`);

--
-- 資料表索引 `RECORD`
--
ALTER TABLE `RECORD`
  ADD PRIMARY KEY (`TNO`,`PID`);

--
-- 資料表索引 `SUPPLIER`
--
ALTER TABLE `SUPPLIER`
  ADD PRIMARY KEY (`SNAME`);

--
-- 資料表索引 `TRANSACTION`
--
ALTER TABLE `TRANSACTION`
  ADD PRIMARY KEY (`TNO`);

--
-- 在傾印的資料表使用自動遞增(AUTO_INCREMENT)
--

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `CART`
--
ALTER TABLE `CART`
  MODIFY `CID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `MEMBER`
--
ALTER TABLE `MEMBER`
  MODIFY `MID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `TRANSACTION`
--
ALTER TABLE `TRANSACTION`
  MODIFY `TNO` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
