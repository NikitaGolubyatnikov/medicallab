-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1:3306
-- Время создания: Апр 25 2025 г., 15:34
-- Версия сервера: 8.0.30
-- Версия PHP: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `medicallab`
--

-- --------------------------------------------------------

--
-- Структура таблицы `analyzers`
--

CREATE TABLE `analyzers` (
  `id` int NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `insurance_companies`
--

CREATE TABLE `insurance_companies` (
  `id` int NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `address` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `inn` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `rs` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `bik` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `invoices`
--

CREATE TABLE `invoices` (
  `id` int NOT NULL,
  `insurance_company_id` int NOT NULL,
  `start_period` date DEFAULT NULL,
  `end_period` date DEFAULT NULL,
  `total_amount` decimal(10,2) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `login_logs`
--

CREATE TABLE `login_logs` (
  `id` int NOT NULL,
  `login` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `attempt_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `success` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `login_logs`
--

INSERT INTO `login_logs` (`id`, `login`, `attempt_time`, `success`) VALUES
(1, 'admin', '2025-04-21 13:45:29', 1),
(2, 'admin', '2025-04-21 13:50:11', 1),
(3, 'admin', '2025-04-21 13:56:28', 1),
(4, 'admin', '2025-04-21 14:14:00', 1),
(5, 'admin', '2025-04-21 14:14:09', 1),
(6, 'admin', '2025-04-21 14:14:59', 1),
(7, 'nikita', '2025-04-21 14:15:36', 0),
(8, 'nikita', '2025-04-21 14:15:41', 0),
(9, 'nikita', '2025-04-21 14:15:45', 0),
(10, 'nikita', '2025-04-21 14:15:53', 0),
(11, 'admin', '2025-04-21 14:16:18', 1),
(12, 'qqq', '2025-04-21 14:16:59', 0),
(13, 'qqq', '2025-04-21 14:17:31', 0),
(14, 'qqq', '2025-04-21 14:19:06', 1),
(15, 'qqq', '2025-04-21 14:19:06', 0),
(16, 'qqq', '2025-04-21 14:19:42', 0),
(17, 'admin', '2025-04-21 14:20:52', 0),
(18, 'admin', '2025-04-21 14:28:35', 0),
(19, 'admin', '2025-04-21 14:32:30', 0),
(20, 'admin', '2025-04-21 14:34:31', 0),
(21, 'admin', '2025-04-21 14:36:55', 0),
(22, 'admin', '2025-04-21 14:39:33', 0),
(23, 'admin', '2025-04-21 14:41:03', 0),
(24, 'admin', '2025-04-21 14:43:11', 0),
(25, 'admin', '2025-04-21 14:45:15', 0),
(26, 'admin', '2025-04-21 14:46:01', 0),
(27, 'admin', '2025-04-21 16:20:17', 0),
(28, 'admin', '2025-04-21 16:35:29', 0),
(29, 'admin', '2025-04-21 16:36:13', 0),
(30, 'admin', '2025-04-21 16:40:02', 0),
(31, 'admin2', '2025-04-21 16:42:51', 0),
(32, 'admin2', '2025-04-21 16:49:09', 0),
(33, 'admin', '2025-04-21 16:49:18', 0),
(34, 'admin', '2025-04-21 16:53:00', 0),
(35, 'admin', '2025-04-21 16:56:19', 1),
(36, 'admin', '2025-04-21 16:58:51', 1),
(37, 'qq', '2025-04-21 16:59:12', 0),
(38, 'qq', '2025-04-21 16:59:43', 0),
(39, 'admin2', '2025-04-21 17:00:37', 0),
(40, 'admin', '2025-04-21 17:00:46', 1),
(41, 'qq', '2025-04-21 17:02:38', 0),
(42, 'qwer', '2025-04-21 17:07:48', 0),
(43, 'admin', '2025-04-21 17:13:21', 1),
(44, 'qwer', '2025-04-21 17:15:06', 0),
(45, 'admin', '2025-04-21 17:15:45', 1),
(46, 'admin1', '2025-04-21 17:16:03', 0),
(47, 'admin1', '2025-04-21 17:16:12', 0),
(48, 'admin1', '2025-04-21 17:16:34', 0),
(49, 'admin', '2025-04-22 14:49:01', 1),
(50, 'admin', '2025-04-22 15:01:48', 1),
(51, 'qwerty', '2025-04-22 15:02:34', 0),
(52, 'qwerty', '2025-04-22 15:05:11', 0),
(53, 'qwerty', '2025-04-22 15:08:06', 0),
(54, 'admin', '2025-04-22 15:08:21', 0),
(55, 'admin', '2025-04-22 15:08:27', 1),
(56, 'q', '2025-04-22 15:08:53', 0),
(57, 'qqq', '2025-04-22 15:14:09', 1),
(58, 'qqq', '2025-04-22 15:14:44', 1),
(59, 'admin', '2025-04-22 17:01:51', 1),
(60, 'qq', '2025-04-22 17:02:48', 1),
(61, 'ww', '2025-04-22 17:03:22', 1),
(62, 'ee', '2025-04-22 17:04:04', 1),
(63, 's', '2025-04-22 17:12:01', 0),
(64, 's', '2025-04-22 17:12:02', 0),
(65, 's', '2025-04-22 17:12:03', 0),
(66, 'admin', '2025-04-22 17:12:35', 1),
(67, 'qq', '2025-04-23 15:25:36', 1),
(68, 'ww', '2025-04-23 15:26:36', 1),
(69, 'ee', '2025-04-23 15:29:11', 1),
(70, 'admin', '2025-04-23 15:31:29', 1),
(71, 'admin', '2025-04-24 18:08:39', 1),
(72, 'admin', '2025-04-24 18:17:30', 1),
(73, 'qq', '2025-04-24 18:17:54', 1),
(74, 'ww', '2025-04-24 18:26:12', 1),
(75, 'qq', '2025-04-24 18:31:22', 1),
(76, 'admin', '2025-04-24 21:32:49', 1),
(77, 'admin', '2025-04-24 21:36:13', 1),
(78, 'admin', '2025-04-24 22:55:30', 1),
(79, 'admin', '2025-04-24 22:56:51', 1),
(80, 'admin', '2025-04-24 22:58:11', 1),
(81, 'qq', '2025-04-24 22:58:38', 1),
(82, 'ww', '2025-04-24 22:59:23', 1),
(83, 'ee', '2025-04-24 22:59:46', 1),
(84, 'admin', '2025-04-24 23:03:11', 1),
(85, 'admin', '2025-04-24 23:05:03', 1),
(86, 'admin', '2025-04-24 23:10:06', 1),
(87, 'admin', '2025-04-25 14:58:30', 1),
(88, 'admin', '2025-04-25 14:59:53', 1),
(89, 'admin', '2025-04-25 15:05:09', 1),
(90, 'qq', '2025-04-25 15:13:58', 1),
(91, 'ww', '2025-04-25 15:26:46', 1),
(92, 'ee', '2025-04-25 15:27:08', 1);

-- --------------------------------------------------------

--
-- Структура таблицы `orders`
--

CREATE TABLE `orders` (
  `id` int NOT NULL,
  `patient_id` int NOT NULL,
  `tube_code` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `order_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `status` enum('new','in_progress','completed','archived') COLLATE utf8mb4_unicode_ci DEFAULT 'new',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `archived` tinyint(1) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `orders`
--

INSERT INTO `orders` (`id`, `patient_id`, `tube_code`, `order_date`, `status`, `created_at`, `archived`) VALUES
(2, 1, 'TUBE-001', '2025-04-15 15:20:27', 'new', '2025-04-22 15:54:47', 0),
(9, 2, 'TUBE-001', '2025-04-15 17:44:20', 'new', '2025-04-22 15:54:47', 0),
(10, 3, 'TUBE-001', '2025-04-15 17:46:07', 'new', '2025-04-22 15:54:47', 0),
(11, 1, 'TUBE-0004', '2025-04-15 17:53:12', 'new', '2025-04-22 15:54:47', 0),
(12, 3, 'TUBE-0005', '2025-04-15 17:58:51', 'new', '2025-04-22 15:54:47', 0),
(13, 3, 'TUBE-0006', '2025-04-15 18:15:45', 'new', '2025-04-22 15:54:47', 0),
(14, 1, 'TUBE-0007', '2025-04-15 18:17:36', 'new', '2025-04-22 15:54:47', 0),
(15, 1, 'TUBE-0008', '2025-04-15 18:21:53', 'new', '2025-04-22 15:54:47', 0),
(16, 1, 'TUBE-0009', '2025-04-15 18:24:09', 'new', '2025-04-22 15:54:47', 0),
(17, 1, 'TUBE-0010', '2025-04-15 18:27:07', 'new', '2025-04-22 15:54:47', 0),
(18, 3, 'TUBE-0011', '2025-04-15 18:28:44', 'new', '2025-04-22 15:54:47', 0),
(19, 1, 'TUBE-0012', '2025-04-15 18:32:10', 'new', '2025-04-22 15:54:47', 0),
(20, 3, 'TUBE-0013', '2025-04-15 18:33:48', 'new', '2025-04-22 15:54:47', 0),
(21, 1, 'TUBE-0014', '2025-04-15 18:37:38', 'new', '2025-04-22 15:54:47', 0),
(22, 1, 'TUBE-0015', '2025-04-15 18:40:14', 'new', '2025-04-22 15:54:47', 0),
(23, 2, 'TUBE-0016', '2025-04-15 18:42:18', 'new', '2025-04-22 15:54:47', 0),
(24, 3, 'TUBE-0017', '2025-04-15 18:43:36', 'new', '2025-04-22 15:54:47', 0),
(25, 1, 'TUBE-0018', '2025-04-15 18:47:53', 'new', '2025-04-22 15:54:47', 0),
(26, 1, 'TUBE-0019', '2025-04-15 18:48:53', 'new', '2025-04-22 15:54:47', 0),
(27, 1, 'TUBE-0020', '2025-04-15 18:49:12', 'new', '2025-04-22 15:54:47', 0),
(28, 1, 'TUBE-0021', '2025-04-15 18:49:55', 'new', '2025-04-22 15:54:47', 0),
(29, 1, 'TUBE-0022', '2025-04-15 18:50:41', 'new', '2025-04-22 15:54:47', 0),
(30, 1, 'TUBE-0023', '2025-04-15 18:52:22', 'new', '2025-04-22 15:54:47', 0),
(31, 1, 'TUBE-0024', '2025-04-15 18:53:58', 'new', '2025-04-22 15:54:47', 0),
(32, 1, 'TUBE-0025', '2025-04-15 18:54:31', 'new', '2025-04-22 15:54:47', 0),
(33, 1, 'TUBE-0026', '2025-04-15 18:57:36', 'new', '2025-04-22 15:54:47', 0),
(34, 1, 'TUBE-0027', '2025-04-15 18:59:03', 'new', '2025-04-22 15:54:47', 0),
(35, 1, 'TUBE-0028', '2025-04-15 19:19:52', 'new', '2025-04-22 15:54:47', 0),
(36, 1, 'TUBE-0029', '2025-04-15 19:20:24', 'new', '2025-04-22 15:54:47', 0),
(37, 1, 'TUBE-0030', '2025-04-15 19:22:49', 'new', '2025-04-22 15:54:47', 0),
(38, 1, 'TUBE-0031', '2025-04-20 15:51:19', 'new', '2025-04-22 15:54:47', 1),
(39, 2, 'TUBE-0032', '2025-04-22 16:29:11', 'new', '2025-04-22 16:29:11', 1),
(40, 1, 'TUBE-0033', '2025-04-22 17:03:46', 'new', '2025-04-22 17:03:46', 1),
(41, 2, 'TUBE-0034', '2025-04-23 15:27:41', 'new', '2025-04-23 15:27:41', 1),
(42, 1, 'TUBE-0035', '2025-04-24 21:28:30', 'new', '2025-04-24 21:28:30', 0),
(43, 1, 'TUBE-0036', '2025-04-24 21:54:39', 'new', '2025-04-24 21:54:39', 0),
(44, 3, 'TUBE-0037', '2025-04-24 22:57:14', 'new', '2025-04-24 22:57:14', 0),
(45, 5, 'TUBE-0038', '2025-04-24 22:58:21', 'new', '2025-04-24 22:58:21', 0),
(46, 10, 'TUBE-0039', '2025-04-25 15:32:27', 'new', '2025-04-25 15:32:27', 0);

-- --------------------------------------------------------

--
-- Структура таблицы `order_services`
--

CREATE TABLE `order_services` (
  `id` int NOT NULL,
  `order_id` int NOT NULL,
  `service_id` int NOT NULL,
  `status` enum('pending','sent_to_analyzer','completed','rejected') COLLATE utf8mb4_unicode_ci DEFAULT 'pending',
  `analyzer_id` int DEFAULT NULL,
  `result_value` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `order_services`
--

INSERT INTO `order_services` (`id`, `order_id`, `service_id`, `status`, `analyzer_id`, `result_value`) VALUES
(13, 9, 12, 'pending', NULL, NULL),
(14, 9, 17, 'pending', NULL, NULL),
(15, 9, 1, 'pending', NULL, NULL),
(16, 10, 12, 'pending', NULL, NULL),
(17, 11, 1, 'pending', NULL, NULL),
(18, 12, 3, 'pending', NULL, NULL),
(19, 12, 14, 'pending', NULL, NULL),
(20, 12, 16, 'pending', NULL, NULL),
(21, 13, 2, 'pending', NULL, NULL),
(22, 14, 1, 'pending', NULL, NULL),
(23, 15, 1, 'pending', NULL, NULL),
(24, 16, 8, 'pending', NULL, NULL),
(25, 17, 3, 'pending', NULL, NULL),
(26, 18, 15, 'pending', NULL, NULL),
(27, 19, 8, 'pending', NULL, NULL),
(28, 20, 8, 'pending', NULL, NULL),
(29, 21, 2, 'pending', NULL, NULL),
(30, 22, 6, 'pending', NULL, NULL),
(31, 23, 8, 'pending', NULL, NULL),
(32, 24, 1, 'pending', NULL, NULL),
(33, 25, 5, 'pending', NULL, NULL),
(34, 26, 16, 'pending', NULL, NULL),
(35, 27, 1, 'pending', NULL, NULL),
(36, 28, 1, 'pending', NULL, NULL),
(37, 29, 6, 'pending', NULL, NULL),
(38, 30, 7, 'pending', NULL, NULL),
(39, 31, 1, 'pending', NULL, NULL),
(40, 32, 1, 'pending', NULL, NULL),
(41, 33, 5, 'pending', NULL, NULL),
(42, 34, 4, 'pending', NULL, NULL),
(43, 35, 1, 'pending', NULL, NULL),
(44, 36, 1, 'pending', NULL, NULL),
(45, 37, 15, 'pending', NULL, NULL),
(46, 37, 16, 'pending', NULL, NULL),
(47, 37, 2, 'pending', NULL, NULL),
(48, 38, 5, 'pending', NULL, NULL),
(49, 38, 7, 'pending', NULL, NULL),
(50, 38, 15, 'pending', NULL, NULL),
(51, 39, 15, 'pending', NULL, NULL),
(52, 39, 2, 'pending', NULL, NULL),
(53, 40, 2, 'pending', NULL, NULL),
(54, 41, 16, 'pending', NULL, NULL),
(55, 41, 13, 'pending', NULL, NULL),
(56, 41, 6, 'pending', NULL, NULL),
(57, 41, 2, 'pending', NULL, NULL),
(58, 41, 16, 'pending', NULL, NULL),
(59, 41, 1, 'pending', NULL, NULL),
(60, 42, 6, 'pending', NULL, NULL),
(61, 43, 4, 'pending', NULL, NULL),
(62, 43, 16, 'pending', NULL, NULL),
(63, 43, 17, 'pending', NULL, NULL),
(64, 43, 4, 'pending', NULL, NULL),
(65, 44, 3, 'pending', NULL, NULL),
(66, 44, 2, 'pending', NULL, NULL),
(67, 44, 16, 'pending', NULL, NULL),
(68, 45, 7, 'pending', NULL, NULL),
(69, 45, 10, 'pending', NULL, NULL),
(70, 46, 5, 'pending', NULL, NULL);

-- --------------------------------------------------------

--
-- Структура таблицы `patients`
--

CREATE TABLE `patients` (
  `id` int NOT NULL,
  `full_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `date_of_birth` date DEFAULT NULL,
  `passport_series_number` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `phone` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `insurance_number` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `insurance_type` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `insurance_company_id` int DEFAULT NULL,
  `is_archived` tinyint(1) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `patients`
--

INSERT INTO `patients` (`id`, `full_name`, `date_of_birth`, `passport_series_number`, `phone`, `email`, `insurance_number`, `insurance_type`, `insurance_company_id`, `is_archived`) VALUES
(1, 'Иванов Иван Иванович', '1990-01-01', '1234 567890', '+79991234567', 'ivanov@mail.ru', 'INS-001', 'ОМС', NULL, 0),
(2, 'Петров Пётр Петрович', '1985-05-15', '2345 678901', '+79995678901', 'petrov@mail.ru', 'INS-002', 'ДМС', NULL, 0),
(3, 'Сидорова Мария Павловна', '1993-03-23', '3456 789012', '+79991112233', 'sidorova@mail.ru', 'INS-003', 'ОМС', NULL, 0),
(4, 'Иванинка', '2005-04-04', '3434234', '23434', '3434', '3434234234', '34234', NULL, 1),
(5, 'Гоша', '2005-04-04', '342343', '23423423', '234234', '4324234', '23423432', NULL, 0),
(6, 'fgfgfg', '2005-04-04', '675676', '6566', '5675676767', '7676', '756767', NULL, 1),
(7, '6765767', '2005-04-04', '4564563456', '2565657', '26563456', '256562', '256565', NULL, 1),
(8, '25626562456', '2005-04-04', '543545', '43523451', '4353454', '234545', '2345435', NULL, 1),
(9, 'gosha', '2005-05-05', '34234', '343', '23434', '343434343', '443', NULL, 1),
(10, 'sidr', '1999-03-03', '23423', '22323', '2344', '23234', '43423', NULL, 0);

-- --------------------------------------------------------

--
-- Структура таблицы `services`
--

CREATE TABLE `services` (
  `id` int NOT NULL,
  `code` int NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `cost` decimal(10,2) NOT NULL,
  `result_type` enum('Integer','String') COLLATE utf8mb4_unicode_ci NOT NULL,
  `available_analyzers` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `services`
--

INSERT INTO `services` (`id`, `code`, `name`, `cost`, `result_type`, `available_analyzers`) VALUES
(1, 619, 'TSH', '262.71', 'Integer', 'Ledetect | Biorad'),
(2, 311, 'Амилаза', '361.88', 'Integer', 'Ledetect | Biorad'),
(3, 548, 'Альбумин', '234.09', 'Integer', 'Ledetect | Biorad'),
(4, 258, 'Креатинин', '143.22', 'Integer', 'Ledetect | Biorad'),
(5, 176, 'Билирубин общий', '102.85', 'Integer', 'Ledetect | Biorad'),
(6, 501, 'Гепатит В', '176.83', 'Integer', 'Ledetect | Biorad'),
(7, 543, 'Гепатит С', '289.99', 'Integer', 'Ledetect | Biorad'),
(8, 557, 'ВИЧ', '490.77', 'Integer', 'Ledetect | Biorad'),
(9, 229, 'СПИД', '341.78', 'Integer', 'Ledetect | Biorad'),
(10, 415, 'Кальций общий', '419.90', 'Integer', 'Ledetect | Biorad'),
(11, 323, 'Глюкоза', '447.65', 'Integer', 'Ledetect | Biorad'),
(12, 855, 'Ковид IgM', '209.78', 'Integer', 'Ledetect | Biorad'),
(13, 346, 'Общий белок', '396.03', 'Integer', 'Ledetect | Biorad'),
(14, 836, 'Железо', '105.32', 'Integer', 'Ledetect | Biorad'),
(15, 659, 'Сифилис RPR', '443.66', 'Integer', 'Ledetect | Biorad'),
(16, 797, 'АТ и АГ к ВИЧ 1/2', '370.62', 'Integer', 'Ledetect | Biorad'),
(17, 287, 'Волчаночный антикоагулянт', '290.11', 'Integer', 'Ledetect | Biorad');

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

CREATE TABLE `users` (
  `id` int NOT NULL,
  `login` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password_hash` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `full_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `role` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `last_login` datetime DEFAULT NULL,
  `is_archived` tinyint(1) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `users`
--

INSERT INTO `users` (`id`, `login`, `password_hash`, `full_name`, `role`, `last_login`, `is_archived`) VALUES
(1, 'admin', '$2b$12$5tYpNSg/xBi.pQwihow6eO7uXcZAp44V.XbAaVsIuDglR8vlPGT4a', 'Администратор Системы', 'admin', '2025-04-25 15:05:09', 0),
(2, 'chacking0', '$2b$12$mz.HRoUi8r1XO4V7WDT/f.wbG67ryqumu5ztdru3YPyQHropovy7e', 'Clareta Hocking', 'lab_assistant', NULL, 0),
(3, 'nmably1', '$2b$12$LRzz5QtfZPjy6mrZzdwi..on7Sm3XnMynBa7RyZefqjhlGDiMcdGO', 'Northrop Mably', 'researcher', NULL, 0),
(4, 'frolf2', '$2b$12$uGRzQ6kWhVIEzug6A.6Ax.M8dc2.Ts06ZV3Mx2MaUKFWgUhJScfua', 'Fabian Ralf', 'lab_assistant', NULL, 0),
(5, 'lraden3', '$2b$12$f4EPrf6NjZAFqx4.8coyw.5T3DEqz7jnLMtXoL4QwHsuITuxD9dIy', 'Lauree Raden', 'lab_assistant', NULL, 1),
(6, 'bfollos4', '$2b$12$0dAwG6UCGWcff3fMax7kLeLaSWr8V.I0TSzIAIBGzpxyWJvzlpxwq', 'Barby Follos', 'lab_assistant', NULL, 0),
(7, 'menterle5', '$2b$12$mM/ttDj8a0N0a6bTq63fhuz3xNoZDtC1x8ftWGUQAKQPggp2tvVGC', 'Mile Enterle', 'researcher', NULL, 0),
(8, 'mpeaker6', '$2b$12$DNHXnaFuuqIl8IIxPyIJJ.M72eWRYo2HFmZUDPPXEeIpI3s4hwtay', 'Midge Peaker', 'researcher', NULL, 0),
(9, 'mrobichon7', '$2b$12$qA0uSj94w4CgmqIxsEBFDOglrIB8OH57cJ0N74WwvL2Za1n6P6xm6', 'Manon Robichon', 'researcher', NULL, 0),
(10, 'srobken8', '$2b$12$.6P.gUWbaNFQknxMUg8zk.0YILIZSWencCYCPncS./W3JS4pz2/cq', 'Stavro Robken', 'accountant', NULL, 0),
(11, 'btidmas9', '$2b$12$F1Mjg9.4AWIUUFoZcxh0VeYajlPtL2/BlKpLlYn730PKoXauCSrXK', 'Bryan Tidmas', 'accountant', NULL, 0),
(12, 'jfussiea', '$2b$12$zUJdki4m0KhOR81jxoFK..RW8700Ygr4YShmQfG1x5aOcixylCxaW', 'Jeannette Fussie', 'researcher', NULL, 0),
(13, 'santonaccib', '$2b$12$ljgyQp77Zk0/cJ61oVL0beWc1OKIzgyKGqGf8gy3HBcEDpc9J5AoW', 'Stephen Antonacci', 'researcher', NULL, 0),
(14, 'nbountiffc', '$2b$12$JK88lf.uqCERbduZFsiVnOiQK0K//ppjjp65q4cmCfp.KMULe/7Je', 'Niccolo Bountiff', 'lab_assistant', NULL, 0),
(15, 'cbenjefieldd', '$2b$12$eRBaYUv4UG2grXUqK3bIKee8eMjooMFQIAg6oL6E7XfI0Glayjb.i', 'Clemente Benjefield', 'accountant', NULL, 0),
(16, 'ocorbyne', '$2b$12$0l720FPdEECohA.ee4Jwg.nO4UObEFCuVsjAxl1q0yyXqOGJFpXlC', 'Orlan Corbyn', 'accountant', NULL, 0),
(17, 'cstickinsf', '$2b$12$I6jahLJ9bqqajMXyINajjuVW2xzt0FMmJNR1cFzHVAd/L.NJ40HnO', 'Coreen Stickins', 'lab_assistant', NULL, 0),
(18, 'dclarageg', '$2b$12$8l6Wr9T7vQ1XsCkULHDHzOMbYRgNdcyLhaULwtjLz9OjQDsuDQgES', 'Daveta Clarage', 'accountant', NULL, 0),
(19, 'jmccawleyh', '$2b$12$qJoCtE8fC0SdI8.23E90i.0aplP8OCfM.xo5J4B9lsS6mDRdkEF6W', 'Javier McCawley', 'accountant', NULL, 0),
(20, 'dbandi', '$2b$12$A4ZmnRWI72Bzk2oVOt2P0uBgMXTSKV1IMRNxgcxCLbBWisjSCcqAS', 'Daile Band', 'accountant', NULL, 0),
(21, 'abutteryj', '$2b$12$xDuWdiXTnunCfR4.TI02muheMRJQij3l4KbfyrZdppbhICbOUMk.e', 'Angil Buttery', 'researcher', NULL, 0),
(22, 'kkinmank', '$2b$12$JpfqsgyQdDqUA1ctWr5RruWG/0FeTAstVUgW5XdYMfXO3UvqM4hPy', 'Kyla Kinman', 'lab_assistant', NULL, 0),
(23, 'sskepperl', '$2b$12$c9GU94QacTjhyd45lNwTRuNuHTwfekPorZG8AL.m35egsrOFnNd3m', 'Selena Skepper', 'accountant', NULL, 0),
(24, 'ayeolandm', '$2b$12$L03Y6oDe9GMsU1fT.PwVy.eXMXEESOWWFF77mWpO259tR3qfzLaRa', 'Alyson Yeoland', 'accountant', NULL, 0),
(25, 'cspeedingn', '$2b$12$fzk7NYfjk/p2W0oe9fAHmeaHP3yEBzIDLQ.jStvoByqMA3yaYnUIm', 'Claudie Speeding', 'researcher', NULL, 0),
(26, 'ascarisbricko', '$2b$12$LjAUX3DlbdocRwY4GRw.I.RfDRF9xz5mLC3Nsbz5f54ySHklZx/wq', 'Alaric Scarisbrick', 'accountant', NULL, 0),
(27, 'mthurbyp', '$2b$12$wzKyCohVQ48pAANMeGbmceTGcihIpWNgrA9D67OlEKgb5NKu8lDKy', 'Marie Thurby', 'lab_assistant', NULL, 0),
(28, 'croxbroughq', '$2b$12$HerAQmyLX.LnvbyUvJwCfusyXwnoE0b8kD.Uq9vxAxI1yPsqN.Qz2', 'Cloe Roxbrough', 'researcher', NULL, 0),
(29, 'pmccotterr', '$2b$12$Isdx82MX38a.rdpmKR4W4uLOAZuFmbIo9Sl8Mzi4wbjZ1RT9tCnPy', 'Pegeen McCotter', 'accountant', NULL, 0),
(30, 'icallejas', '$2b$12$hReseY2Q3vFYEwT8.WVQ.uAo1HioKw9o8z.rs.070KZQOOr0iugnG', 'Iggie Calleja', 'researcher', NULL, 0),
(31, 'nbroscht', '$2b$12$Ox8Bkbr23ZgVLgpm2XKxSe1xFtDf787xRqi.D22WrQmRaDHMF9.AC', 'Nelle Brosch', 'accountant', NULL, 0),
(32, 'sallseppu', '$2b$12$1e98ZBnjbbFV3VevFUT3A.Lp4j2wNQoEMIEOV/UNgGWEEHqIxyJh6', 'Shae Allsepp', 'researcher', NULL, 0),
(33, 'eabbatucciv', '$2b$12$VAFKq/9ROa5TtZq7EGbnuu4xfazAfLgWRvBhIeHS7uhz0MMZAQGOi', 'Eldridge Abbatucci', 'researcher', NULL, 0),
(34, 'sgarnhamw', '$2b$12$/D9A7pMDQ/DCatWPJOTAg.sy/mnhVsmsYQHf6p8XldicT5EaqEEIq', 'Skip Garnham', 'researcher', NULL, 0),
(35, 'rkitchensidex', '$2b$12$V9dVI4jkxWkI7iKBfiEmHeXiY9agjzaz5h9gyxOoBtQNm8wLYHN8W', 'Ric Kitchenside', 'researcher', NULL, 0),
(36, 'udiy', '$2b$12$scVldeWNIEdpiS1hfIJ7q.1yd0YIzkSAJ/prkZHOxOcgGVf6cVeVi', 'Urbanus Di Meo', 'researcher', NULL, 0),
(37, 'mbeidebekez', '$2b$12$jQcY3xeCEcVmt3Ly2I.4vuDl4fmYZI9q4RWKw7f0YXGfmzfHtNhvS', 'Monty Beidebeke', 'researcher', NULL, 0),
(38, 'bsavins10', '$2b$12$YB5/YFSKDxl6lLw913ztp.FtL0YiJUPOVSqMqMOadhjboV53TjW1O', 'Byrann Savins', 'researcher', NULL, 0),
(39, 'sriby11', '$2b$12$pNm.eBFZie8RJugC3zvT2ukk/ED3dL84sDm3mHd1EP1BZxDOV1vY.', 'Sonnie Riby', 'researcher', NULL, 0),
(40, 'sbirney12', '$2b$12$HOB.VDbSL8Q0NLUxDkcnE.FBen0HHkgn6fWtyCW0d1pRVMTqMzbV2', 'Sherill Birney', 'lab_assistant', NULL, 0),
(41, 'ikleanthous13', '$2b$12$VwWJ92jywuKwto6FZqEA.O4oweCBWIDkYGPLibDeIDCtjO5nzsiu6', 'Indira Kleanthous', 'researcher', NULL, 0),
(42, 'mskerme14', '$2b$12$6RyTJ33LqFn/ZEerSnuSLedl5uPSPpSYbUF.L.eZ3NZ2UstqjrAzm', 'Maison Skerme', 'researcher', NULL, 0),
(43, 'hcahey15', '$2b$12$ENHIqSwRfnlniO0qiZAs2u.mdoFZkDuGq9Pp5LyjTwFL6X6VJQQZW', 'Hanan Cahey', 'accountant', NULL, 0),
(44, 'trusling16', '$2b$12$KtFqntY5Z1jhymmi3FaZBOcAKp41kB8CF7eDRfx4xVZ/z7jcyj/gW', 'Tore Rusling', 'researcher', NULL, 0),
(45, 'jde17', '$2b$12$b8qjyLzIYMie3sDEWK.qG.uSpjOzrV6Fnz6m8uH2OFN8VtFs08M9W', 'Jeddy De Souza', 'researcher', NULL, 0),
(46, 'fmcleoid18', '$2b$12$FxRyYoelwHBKOJfpaiUGOuMKWFMSW7yuKjFW52Z2zezDTOTnBN6r6', 'Flossi McLeoid', 'researcher', NULL, 0),
(47, 'nmegainey19', '$2b$12$cQ2T07YDwMl8kqFnO7lOwuGUdK2D7xc.y312xZna9qx0RYhXCg6l6', 'Nikoletta Megainey', 'researcher', NULL, 0),
(48, 'abliven1a', '$2b$12$YPfYx5Hi3fB5GQaiJKSOue9Zmik2r5exWMR2/sWIAWGPT.nbIJeLq', 'Adan Bliven', 'accountant', NULL, 0),
(49, 'mrossoni1b', '$2b$12$0vEhRYA/WtUlHp5JQtDaiOWjP.yqeUFyURUNHuXwVbFofXvPFXK7C', 'Mohandis Rossoni', 'accountant', NULL, 0),
(50, 'nredington1c', '$2b$12$GiWZ4iKrC56ZnLnhL1l1.emVZx2vPKX4jpddB7Y7uuX.bSf90b8vq', 'Nappie Redington', 'researcher', NULL, 0),
(51, 'lfrancie1d', '$2b$12$UqSk6v4.3eGxLuCxl5hoYuup4sC8IPVd2X44jvIJxt6a/pOXuuk3K', 'Lenka Francie', 'researcher', NULL, 0),
(52, 'ablowin1e', '$2b$12$kLxicw0wjiKbRMy08Iq.3ut7u/FLghyMZeqtG82rpqSMeiEgv/CUe', 'Ashley Blowin', 'researcher', NULL, 0),
(53, 'vgoroni1f', '$2b$12$vV6CidI67BzuOkv92QpS2uZy5jborGfwYmSWC2Vsp.zdzmrewLgh2', 'Vale Goroni', 'accountant', NULL, 0),
(54, 'sgrafom1g', '$2b$12$YO4XO3jMbPlZCLDJedmXveiPRWCNCUzmORmgSy3pBokEzMOcB/aKW', 'Suki Grafom', 'accountant', NULL, 0),
(55, 'jgianneschi1h', '$2b$12$6Bl1inhQ.WLx7SfjGFzQ7.uc2s8acJ0ziR61lhKEYYLXtlHWDU2Ey', 'Justis Gianneschi', 'accountant', NULL, 0),
(56, 'ecollett1i', '$2b$12$3GHqr6FmKFYISIUbqYOvh.avDS21dHZDVLwOM3prtZEthM3fKHdRK', 'Emilie Collett', 'researcher', NULL, 0),
(57, 'bterrell1j', '$2b$12$I1cXEsAg0uA71CQUJqq7/OhJwFBOrXHHVH1VJa68WXpDQrYsTqP1m', 'Byrom Terrell', 'lab_assistant', NULL, 0),
(58, 'dbifield1k', '$2b$12$wetWbgrJuBAxA5xiZ5U9ouRxY3PtBP2t.7Elg3HHHXWFSuIln9aMq', 'Daphne Bifield', 'lab_assistant', NULL, 0),
(59, 'bstaig1l', '$2b$12$49rA8G4dJc8tkvRJgRL76ehqRVIF4lix2.7.9rKukaO4jEg3i7gHi', 'Blanca Staig', 'accountant', NULL, 0),
(60, 'akennsley1m', '$2b$12$mOknOyFxOLkWgAr7KwPMPul0ErNmD0i1JiqFPeAzdStC8EiZc6oma', 'Adriaens Kennsley', 'accountant', NULL, 0),
(61, 'ebartak1n', '$2b$12$kaQW0IA/aXj3xkBxr9iPJOPQDp.0mIG2YHgv/K2yEsxKB8IgTPdL6', 'Emlyn Bartak', 'lab_assistant', NULL, 0),
(62, 'vwillshire1o', '$2b$12$Wb3BbIY6J.1zIKYuuK4TmOuhJbijC6akc6UvBltPeepQU0LimQFIS', 'Victoria Willshire', 'lab_assistant', NULL, 0),
(63, 'esavin1p', '$2b$12$YkzC5AYjisQawLUEa37AUeT1jIilSKGyjYebtpHNnHDNmLxzNmOc.', 'Egon Savin', 'researcher', NULL, 0),
(64, 'pelsom1q', '$2b$12$0jiErsZAHRpjyqHVQqZcW.SqDSarUnGbBmBOUrLw0wd/NqapgzmMy', 'Phillie Elsom', 'researcher', NULL, 0),
(65, 'asemaine1r', '$2b$12$EXqbfGs19k72aGGeISqp5.d1SuQdUG2TKDbo8Q/C2nUp4fpLFlY.G', 'Adan Semaine', 'researcher', NULL, 0),
(66, 'cnorthrop1s', '$2b$12$jUN4bmmutnhRGOK6ZkaAK..t.j4wLSmAS4qKsrzRCKm0lDk8Tf2ti', 'Constantino Northrop', 'lab_assistant', NULL, 0),
(67, 'reasson1t', '$2b$12$Rm0veRqDviBeBl6EQyQm1O.QEKpwhVlNU0aY/70tshKS0NyWnwKqG', 'Rodie Easson', 'researcher', NULL, 0),
(68, 'aboleyn1u', '$2b$12$vN6yLm3gxuSwXm6mFeddS.RgHtY7xIx2LnymQGxed.EyYVG5RLuCW', 'Alida Boleyn', 'accountant', NULL, 0),
(69, 'hscholfield1v', '$2b$12$G72VWjrn6sUz7hIYcpXVpuEFnZPCv6DmgBNA87JkhitmQZq3tp3my', 'Hill Scholfield', 'researcher', NULL, 0),
(70, 'ccowpe1w', '$2b$12$0c9kmCFo0IgEpgljz.xM.OyvHwX6NqhBA9YUeCKQKkHAi36FjrUf6', 'Cordell Cowpe', 'accountant', NULL, 0),
(71, 'aeldon1x', '$2b$12$zl9V3Sm7ctYljynr0rOq0.qPoldkY9ymukIYCtiza0z1oNl8h9Zn2', 'Alexandro Eldon', 'lab_assistant', NULL, 0),
(72, 'kcollin1y', '$2b$12$u4IH.MSLw821ExoG7atkCuC14Cze8Oe11iN6Fz6qCjLtpeIhUtmzG', 'Kayle Collin', 'lab_assistant', NULL, 0),
(73, 'ilarkins1z', '$2b$12$vDQ3f4KnT3WYx1DK5Lb0f.Ib/902FbPcaazhjvwxIRUuwhrBFPTva', 'Inesita Larkins', 'lab_assistant', NULL, 0),
(74, 'wlound20', '$2b$12$yQZ9xlNcUDftXV5.PR4FtOdR2RyJTi7eLCrlQwaoc15m77xhSvc8i', 'Waylin Lound', 'lab_assistant', NULL, 0),
(75, 'mgillogley21', '$2b$12$fLVyLgIGDZThDQq8q9XyNOW59UM5f0BlHPODIZ.eKtPaXqXMVIbdm', 'Mechelle Gillogley', 'researcher', NULL, 0),
(76, 'dmuccino22', '$2b$12$XHtdX3vvxiid2vuulcxE0uHNdtX9xKQ2t9nwYEwwKs0f4Uwmbrg5W', 'Donal Muccino', 'accountant', NULL, 0),
(77, 'jleadbetter23', '$2b$12$rTcChDCuyYcP0Uww0yiBPee4tOdIDKihFh9NRmjG6AK1WfZCPAlPK', 'Joye Leadbetter', 'researcher', NULL, 0),
(78, 'gtrump24', '$2b$12$HkAnp8gcY5I1.R4WdTbxUuwKRTnYyuiuF9jFs.PnOnkKD/TsSD1BS', 'Gianina Trump', 'accountant', NULL, 0),
(79, 'rleestut25', '$2b$12$3kmvZkUqf96SJGe5iLXyGuJyXag5iX1sXXmsfle2gKCcqmOHFLG3W', 'Read LeEstut', 'lab_assistant', NULL, 0),
(80, 'janscott26', '$2b$12$csaX0JxHQJNHeL2BAjbSj.3vNl7PGDq2mxZ3EB77kM8Tny9PkLo/i', 'Jill Anscott', 'accountant', NULL, 0),
(81, 'bdouch27', '$2b$12$/7yna..EkvB6VXVsTp1IU.4nkxhtwzcy.6Df3bdq5uvQinMmgOqle', 'Bud Douch', 'lab_assistant', NULL, 0),
(82, 'cossenna28', '$2b$12$Imqj1dkw0CuFFRZgILJ.rOA6qvkgcVTu1Mlv0pUjhEgc0/6JFHA7a', 'Cicily Ossenna', 'accountant', NULL, 0),
(83, 'hizzat29', '$2b$12$AwwGpevujvvl/JPr03EW6OhS8hhMLqfhg5ZrLW54YqHrUntVMuAMq', 'Hew Izzat', 'lab_assistant', NULL, 0),
(84, 'egimeno2a', '$2b$12$LD3tbIhl6rUFaSaGdOjckuUcxqdJpTXAW84bYTWrFvUgQBIGAJ52C', 'Eddie Gimeno', 'accountant', NULL, 0),
(85, 'sfierro2b', '$2b$12$wKI/OcGbbsNT95rJqkhHQu1ay9KdWhNEHF/5OhS0gCOHshegJ2g5u', 'Sybyl Fierro', 'researcher', NULL, 0),
(86, 'ntroup2c', '$2b$12$d6TYbxOveaJbRek1NDkvMuQazPv/8TdENVxUSU/M75tZNeEaRBA8u', 'Nicol Troup', 'researcher', NULL, 0),
(87, 'bpattenden2d', '$2b$12$TxjEvn/JvpB0lz9I3Ch8eeVfuq4.qUbwFRnEYsfN550KztU4E4WRO', 'Bondy Pattenden', 'lab_assistant', NULL, 0),
(88, 'acockman2e', '$2b$12$joRKULeIV1BCVJ3REr8tDeQUJsd501r/8xTpOkv95jN500WL5mg26', 'Angus Cockman', 'lab_assistant', NULL, 0),
(89, 'mhanscome2f', '$2b$12$ISBk28bZRaZe1vz11am4rukWnrWhcr.j3psrLy.vJCQZlwuoqS8Jm', 'Mord Hanscome', 'researcher', NULL, 0),
(90, 'sleblanc2g', '$2b$12$DeB8VYMQN5oHuZwW5./pEenAVqCB3zLVtJ9SLJRDRmmjfnlRyuou6', 'Susy Leblanc', 'researcher', NULL, 0),
(91, 'gciccoloi2h', '$2b$12$UNlpimx/d.NZVu82fIsPIevGeogdJveWvdWWpPAcZJZSHOQrNOLK6', 'Gerard Ciccoloi', 'lab_assistant', NULL, 0),
(92, 'ssayburn2i', '$2b$12$mwbsw9POFNI0k/KVO2Pr5.chmdgVZD9St8Zqekn0jxSx6j3/OyYcm', 'Seamus Sayburn', 'researcher', NULL, 0),
(93, 'wgentiry2j', '$2b$12$w5imu83Lh9.UIaJ7T2lQ.OHdTxjjWUKh9k3VAmeVZp4NxUUQAZZ/K', 'Washington Gentiry', 'lab_assistant', NULL, 0),
(94, 'rwestall2k', '$2b$12$QHvBda8NqT9v0fjaw0Fda.bOChwEuqa29o/zFjR9VarpEk3iMZl7.', 'Rebekkah Westall', 'researcher', NULL, 0),
(95, 'ckulic2l', '$2b$12$2NfYl3gYeNUgXv4LpJm.o.icHQVcuhB3w5jTHnDg88p7MPt0XpcT.', 'Court Kulic', 'lab_assistant', NULL, 0),
(96, 'lroux2m', '$2b$12$9kNlOfIYrQ3ASX3Gsw/v7.ZbbEhvGHboSGncnnJnxKS4dy/yJM1ee', 'Lorilee Roux', 'accountant', NULL, 0),
(97, 'mrolinson2n', '$2b$12$6Z0s/F3sn7Y9wVdSMfN1ZulBBcdQpHYPPQazR6VmZmI42CA3NvkL6', 'Modestine Rolinson', 'lab_assistant', NULL, 0),
(98, 'sellgood2o', '$2b$12$LY/d/sDrMgRUTLIYWtoVpekg.mcU1D3RVV8gzahXmI3Cdqzc7xeV6', 'Shelbi Ellgood', 'accountant', NULL, 0),
(99, 'bretchless2p', '$2b$12$09A2dmCj1lNwUrA95pPEPeCqIt0L2sXiOVjWaqY0alfl3oTzbIU0C', 'Barbabra Retchless', 'researcher', NULL, 0),
(100, 'rjerzak2q', '$2b$12$i4YkbaVoIyq9xl4Uk/VjB.VGh5OBZaLPuQDljxmhYjqIGFnU3OlkC', 'Robinetta Jerzak', 'researcher', NULL, 0),
(219, 'qq', '$2b$12$vjIAYh8E2E7d4yoB4XAxI.druVIlVX3rszW0AVxXeTXZUV0cNF0bu', 'qqq', 'researcher', '2025-04-25 15:13:58', 0),
(220, 'ww', '$2b$12$MUUB22aXvI1q7Tv2jPiTjOYal2udKJlqjNBFaFY0ObI7YG5BPx7xe', 'dfd', 'lab_assistant', '2025-04-25 15:26:46', 0),
(221, 'ee', '$2b$12$B3CIdBWlRGdPBRv9sOEsJeRFtH4AhzhywuB/eSTd0emviCVp0qeEG', 'sdsd', 'accountant', '2025-04-25 15:27:08', 0),
(222, 'вава', '$2b$12$SyY0W3LQWY5bN2GERLi2qed3mJbrHuOkGmxi04nRHAaenLaiPHmFW', 'вава', 'researcher', NULL, 0),
(223, 'e', '$2b$12$gi/Vg7eVutzg4VfXn43RI.6wnowwQTNa7OxxgeUBwRrLP0ufXG7UK', 'efterr', 'accountant', NULL, 0),
(224, 'qwerty', '$2b$12$1Kxt8fI7Frhy1NOnimeBouGYwg2q3ALOC1WZ8WCdDJ9pxGKZaPMBG', 'qqq www eee', 'lab_assistant', NULL, 0);

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `analyzers`
--
ALTER TABLE `analyzers`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Индексы таблицы `insurance_companies`
--
ALTER TABLE `insurance_companies`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `invoices`
--
ALTER TABLE `invoices`
  ADD PRIMARY KEY (`id`),
  ADD KEY `insurance_company_id` (`insurance_company_id`);

--
-- Индексы таблицы `login_logs`
--
ALTER TABLE `login_logs`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`),
  ADD KEY `patient_id` (`patient_id`);

--
-- Индексы таблицы `order_services`
--
ALTER TABLE `order_services`
  ADD PRIMARY KEY (`id`),
  ADD KEY `order_id` (`order_id`),
  ADD KEY `service_id` (`service_id`),
  ADD KEY `analyzer_id` (`analyzer_id`);

--
-- Индексы таблицы `patients`
--
ALTER TABLE `patients`
  ADD PRIMARY KEY (`id`),
  ADD KEY `insurance_company_id` (`insurance_company_id`);

--
-- Индексы таблицы `services`
--
ALTER TABLE `services`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code` (`code`);

--
-- Индексы таблицы `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `login` (`login`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `analyzers`
--
ALTER TABLE `analyzers`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `insurance_companies`
--
ALTER TABLE `insurance_companies`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `invoices`
--
ALTER TABLE `invoices`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `login_logs`
--
ALTER TABLE `login_logs`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=93;

--
-- AUTO_INCREMENT для таблицы `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=47;

--
-- AUTO_INCREMENT для таблицы `order_services`
--
ALTER TABLE `order_services`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=71;

--
-- AUTO_INCREMENT для таблицы `patients`
--
ALTER TABLE `patients`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT для таблицы `services`
--
ALTER TABLE `services`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT для таблицы `users`
--
ALTER TABLE `users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=225;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `invoices`
--
ALTER TABLE `invoices`
  ADD CONSTRAINT `invoices_ibfk_1` FOREIGN KEY (`insurance_company_id`) REFERENCES `insurance_companies` (`id`);

--
-- Ограничения внешнего ключа таблицы `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`);

--
-- Ограничения внешнего ключа таблицы `order_services`
--
ALTER TABLE `order_services`
  ADD CONSTRAINT `order_services_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`),
  ADD CONSTRAINT `order_services_ibfk_2` FOREIGN KEY (`service_id`) REFERENCES `services` (`id`),
  ADD CONSTRAINT `order_services_ibfk_3` FOREIGN KEY (`analyzer_id`) REFERENCES `analyzers` (`id`);

--
-- Ограничения внешнего ключа таблицы `patients`
--
ALTER TABLE `patients`
  ADD CONSTRAINT `patients_ibfk_1` FOREIGN KEY (`insurance_company_id`) REFERENCES `insurance_companies` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
