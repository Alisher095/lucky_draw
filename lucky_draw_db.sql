-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 19, 2025 at 07:41 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `lucky_draw_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `accounts_draw`
--

CREATE TABLE `accounts_draw` (
  `id` bigint(20) NOT NULL,
  `title` varchar(255) NOT NULL,
  `draw_type` varchar(10) NOT NULL,
  `description` text DEFAULT NULL,
  `prize_name` varchar(200) NOT NULL,
  `prize_value` decimal(10,2) NOT NULL,
  `winners_count` int(10) UNSIGNED NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `result_date` date NOT NULL,
  `created_by_id` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `accounts_draw`
--

INSERT INTO `accounts_draw` (`id`, `title`, `draw_type`, `description`, `prize_name`, `prize_value`, `winners_count`, `start_date`, `end_date`, `result_date`, `created_by_id`, `created_at`, `updated_at`) VALUES
(1, 'draw lucky', 'single', 'this is lucky draw', 'amazon gift card', 1000.00, 0, '2025-09-23', '2025-09-25', '2025-09-27', 2, '2025-11-10 11:04:02', '2025-11-10 11:09:04'),
(2, 'Lucky wheel', 'multi', 'This is Lucky wheel', 'Amazon USD gift card', 25.00, 15, '2025-09-23', '2025-09-27', '2025-09-30', 2, '2025-11-10 11:04:02', '2025-11-10 11:09:04'),
(3, 'PRIZE POOL', 'single', 'This is prize pool , lucky wheel , spin and get a chance to win the prizes', 'LUCKY WHEEL', 300.00, 0, '2025-10-31', '2025-11-01', '2025-11-03', 2, '2025-11-10 11:04:02', '2025-11-10 11:09:04'),
(4, 'Win Bike at 1', 'single', 'You can win bike at 1 RS only', 'Bike', 150000.00, 1, '2025-11-05', '2025-11-06', '2025-11-07', 2, '2025-11-10 11:04:02', '2025-11-10 11:09:04');

-- --------------------------------------------------------

--
-- Table structure for table `accounts_entry`
--

CREATE TABLE `accounts_entry` (
  `id` bigint(20) NOT NULL,
  `entry_time` datetime(6) NOT NULL,
  `draw_id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT 1,
  `is_verified` tinyint(1) NOT NULL DEFAULT 0,
  `note` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `accounts_entry`
--

INSERT INTO `accounts_entry` (`id`, `entry_time`, `draw_id`, `user_id`, `is_active`, `is_verified`, `note`) VALUES
(1, '2025-09-23 15:03:59.751285', 1, 3, 1, 0, NULL),
(2, '2025-09-23 15:17:54.564389', 2, 3, 1, 0, NULL),
(3, '2025-10-30 05:51:51.223341', 3, 4, 1, 0, NULL),
(4, '2025-11-05 08:49:44.129181', 4, 3, 1, 0, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `accounts_profile`
--

CREATE TABLE `accounts_profile` (
  `id` bigint(20) NOT NULL,
  `role` varchar(10) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `accounts_profile`
--

INSERT INTO `accounts_profile` (`id`, `role`, `user_id`) VALUES
(1, 'admin', 2),
(2, 'user', 3),
(3, 'user', 4);

-- --------------------------------------------------------

--
-- Table structure for table `accounts_winner`
--

CREATE TABLE `accounts_winner` (
  `id` bigint(20) NOT NULL,
  `position` int(10) UNSIGNED NOT NULL,
  `won_at` datetime(6) NOT NULL,
  `draw_id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add profile', 7, 'add_profile'),
(26, 'Can change profile', 7, 'change_profile'),
(27, 'Can delete profile', 7, 'delete_profile'),
(28, 'Can view profile', 7, 'view_profile'),
(29, 'Can add draw', 8, 'add_draw'),
(30, 'Can change draw', 8, 'change_draw'),
(31, 'Can delete draw', 8, 'delete_draw'),
(32, 'Can view draw', 8, 'view_draw'),
(33, 'Can add entry', 9, 'add_entry'),
(34, 'Can change entry', 9, 'change_entry'),
(35, 'Can delete entry', 9, 'delete_entry'),
(36, 'Can view entry', 9, 'view_entry'),
(37, 'Can add winner', 10, 'add_winner'),
(38, 'Can change winner', 10, 'change_winner'),
(39, 'Can delete winner', 10, 'delete_winner'),
(40, 'Can view winner', 10, 'view_winner');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$600000$4e2OCmVFPVdZs098WtjJ9f$Hyxzt4iWrOYxCTiVliofkN1R8/8UU2CbJxQsDlzCdZI=', NULL, 1, 'Admin', '', '', 'admin@gmail.com', 1, 1, '2025-09-19 04:30:36.791847'),
(2, 'pbkdf2_sha256$600000$3fXSDFKHKpGwwV74OpGeJA$wsDDq/13HUCub0m7NRqGJdHdStcaigff01wK00RvSfo=', '2025-11-19 06:35:28.697665', 0, 'a1@gmail.com', 'a', '1', 'a1@gmail.com', 0, 1, '2025-09-19 07:03:58.209079'),
(3, 'pbkdf2_sha256$600000$wiGC70cvZAFUgEi63tDiNV$Y4PaPVJqzNLwT5a2gYp/I6gq2HQ06I9oLi/rWe897TE=', '2025-11-18 07:18:23.888790', 0, 'u1@gmail.com', 'u', '1', 'u1@gmail.com', 0, 1, '2025-09-19 15:20:06.690093'),
(4, 'pbkdf2_sha256$600000$0ESJljHTeK0aB7YQwdGJ9p$VmbytVM0s4+O8WZ8NQEX9cAkRZWgMdQfTQFctA8wPiE=', '2025-10-30 05:47:51.790859', 0, 'u2@gmail.com', 'Ali', 'Sher', 'u2@gmail.com', 0, 1, '2025-10-30 05:29:55.323192');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(8, 'accounts', 'draw'),
(9, 'accounts', 'entry'),
(7, 'accounts', 'profile'),
(10, 'accounts', 'winner'),
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-09-19 04:26:50.873002'),
(2, 'auth', '0001_initial', '2025-09-19 04:26:51.449086'),
(3, 'admin', '0001_initial', '2025-09-19 04:26:51.592524'),
(4, 'admin', '0002_logentry_remove_auto_add', '2025-09-19 04:26:51.607533'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2025-09-19 04:26:51.632004'),
(6, 'contenttypes', '0002_remove_content_type_name', '2025-09-19 04:26:51.797497'),
(7, 'auth', '0002_alter_permission_name_max_length', '2025-09-19 04:26:51.873082'),
(8, 'auth', '0003_alter_user_email_max_length', '2025-09-19 04:26:51.899696'),
(9, 'auth', '0004_alter_user_username_opts', '2025-09-19 04:26:51.918729'),
(10, 'auth', '0005_alter_user_last_login_null', '2025-09-19 04:26:52.007560'),
(11, 'auth', '0006_require_contenttypes_0002', '2025-09-19 04:26:52.012706'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2025-09-19 04:26:52.031491'),
(13, 'auth', '0008_alter_user_username_max_length', '2025-09-19 04:26:52.051590'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2025-09-19 04:26:52.070555'),
(15, 'auth', '0010_alter_group_name_max_length', '2025-09-19 04:26:52.092075'),
(16, 'auth', '0011_update_proxy_permissions', '2025-09-19 04:26:52.105421'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2025-09-19 04:26:52.134883'),
(18, 'sessions', '0001_initial', '2025-09-19 04:26:52.187150'),
(19, 'accounts', '0001_initial', '2025-09-19 06:51:11.257694'),
(20, 'accounts', '0002_draw_winner_entry', '2025-09-22 04:02:24.394116'),
(21, 'accounts', '0003_alter_entry_draw_alter_entry_user', '2025-09-22 04:30:00.622887'),
(22, 'accounts', '0004_alter_winner_options_remove_draw_eligibility_and_more', '2025-09-22 07:08:23.329451');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('eexr45bfpjvrvdpxkq8crfa8hsef7wb0', '.eJxVjMsOwiAQRf-FtSFAeQSX7v0GMswwUjWQlHZl_Hdt0oVu7znnvkSCba1pG2VJM4mzMOL0u2XAR2k7oDu0W5fY27rMWe6KPOiQ107leTncv4MKo35rUJ4BFZfATgGiggyxoFdGe9bRTllTJA5WO28ZXbA5m8lH7dgQgRHvDwqpOH0:1v14X8:gPiZ38hZV0XJ9w8KFdoqXNHrbWXenYS0h4ceSQFhZAY', '2025-10-07 15:02:22.017199'),
('gwv7v0b9w73gg355h1jb0405yt7ac1c1', '.eJxVjDsOwjAQBe_iGlmOvf5R0nMGa9cfHEC2FCcV4u4QKQW0b2beiwXc1hq2kZcwJ3Zmip1-N8L4yG0H6Y7t1nnsbV1m4rvCDzr4taf8vBzu30HFUb816QJZOiEAjNJCFyvRyQIWjdQWKMkJpuiQIkkgcNZ4SKQ8ZJ-FMYm9P75BNxY:1vBPvb:EisLCmIl33_RiQb8O60xE7q0CpzF5mN6kMSf7YaZjyo', '2025-11-05 03:54:23.262452'),
('gzlhlss0v09fdjfynqy94er5qu0b2jua', '.eJxVjDsOwjAQBe_iGlmOvf5R0nMGa9cfHEC2FCcV4u4QKQW0b2beiwXc1hq2kZcwJ3Zmip1-N8L4yG0H6Y7t1nnsbV1m4rvCDzr4taf8vBzu30HFUb816QJZOiEAjNJCFyvRyQIWjdQWKMkJpuiQIkkgcNZ4SKQ8ZJ-FMYm9P75BNxY:1v22Jl:MjZzi-ATTwV-ZZ8V9YL_H-Y6wvnt9gkVefULnF-DOqQ', '2025-10-10 06:52:33.179088'),
('hm83ahyc4t50yk3mliaamcn81e7xp1s0', '.eJxVjMsOwiAQRf-FtSFAeQSX7v0GMswwUjWQlHZl_Hdt0oVu7znnvkSCba1pG2VJM4mzMOL0u2XAR2k7oDu0W5fY27rMWe6KPOiQ107leTncv4MKo35rUJ4BFZfATgGiggyxoFdGe9bRTllTJA5WO28ZXbA5m8lH7dgQgRHvDwqpOH0:1vKr1d:C-bxXIVK-xbcWjqAOCzSCmFdaSQWBACeKxbdvtR5UsE', '2025-12-01 04:39:37.840553'),
('nrhx0hfxtyn5hh9l4n9bh7bxqwcbbwbg', '.eJxVjMsOwiAQRf-FtSFAeQSX7v0GMswwUjWQlHZl_Hdt0oVu7znnvkSCba1pG2VJM4mzMOL0u2XAR2k7oDu0W5fY27rMWe6KPOiQ107leTncv4MKo35rUJ4BFZfATgGiggyxoFdGe9bRTllTJA5WO28ZXbA5m8lH7dgQgRHvDwqpOH0:1vLbmq:CpvKIHpGZAjCToE0qzDgYV-fShbtjgnqpRswmkvCBk0', '2025-12-03 06:35:28.705815'),
('ov1zl2wfucxqdki0rq4fxf9h2j9uqsyc', '.eJxVjMsOwiAQRf-FtSFAeQSX7v0GMswwUjWQlHZl_Hdt0oVu7znnvkSCba1pG2VJM4mzMOL0u2XAR2k7oDu0W5fY27rMWe6KPOiQ107leTncv4MKo35rUJ4BFZfATgGiggyxoFdGe9bRTllTJA5WO28ZXbA5m8lH7dgQgRHvDwqpOH0:1vLFzc:2OTY631PfAG_OImNisr67iw-gHDQLkeg8nUwNSbEMTU', '2025-12-02 07:19:12.696147'),
('xgv2jk8yv43x74t3x3zz0poi671awef3', '.eJxVjDsOwjAQBe_iGlmOvf5R0nMGa9cfHEC2FCcV4u4QKQW0b2beiwXc1hq2kZcwJ3Zmip1-N8L4yG0H6Y7t1nnsbV1m4rvCDzr4taf8vBzu30HFUb816QJZOiEAjNJCFyvRyQIWjdQWKMkJpuiQIkkgcNZ4SKQ8ZJ-FMYm9P75BNxY:1v13wL:jcz1LZ6QkBNvweE6EsQP5TrmNaj1uvsJ3RcliMq9Emw', '2025-10-07 14:24:21.599146');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `accounts_draw`
--
ALTER TABLE `accounts_draw`
  ADD PRIMARY KEY (`id`),
  ADD KEY `accounts_draw_created_by_id_2617ac14_fk_auth_user_id` (`created_by_id`);

--
-- Indexes for table `accounts_entry`
--
ALTER TABLE `accounts_entry`
  ADD PRIMARY KEY (`id`),
  ADD KEY `accounts_entry_draw_id_b294e8bc_fk_accounts_draw_id` (`draw_id`),
  ADD KEY `accounts_entry_user_id_e390c5ad_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `accounts_profile`
--
ALTER TABLE `accounts_profile`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indexes for table `accounts_winner`
--
ALTER TABLE `accounts_winner`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `accounts_winner_draw_id_user_id_position_bb698119_uniq` (`draw_id`,`user_id`,`position`),
  ADD KEY `accounts_winner_user_id_9fa72d6b_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `accounts_draw`
--
ALTER TABLE `accounts_draw`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `accounts_entry`
--
ALTER TABLE `accounts_entry`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `accounts_profile`
--
ALTER TABLE `accounts_profile`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `accounts_winner`
--
ALTER TABLE `accounts_winner`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `accounts_draw`
--
ALTER TABLE `accounts_draw`
  ADD CONSTRAINT `accounts_draw_created_by_id_2617ac14_fk_auth_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `accounts_entry`
--
ALTER TABLE `accounts_entry`
  ADD CONSTRAINT `accounts_entry_draw_id_b294e8bc_fk_accounts_draw_id` FOREIGN KEY (`draw_id`) REFERENCES `accounts_draw` (`id`),
  ADD CONSTRAINT `accounts_entry_user_id_e390c5ad_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `accounts_profile`
--
ALTER TABLE `accounts_profile`
  ADD CONSTRAINT `accounts_profile_user_id_49a85d32_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `accounts_winner`
--
ALTER TABLE `accounts_winner`
  ADD CONSTRAINT `accounts_winner_draw_id_aab3580a_fk_accounts_draw_id` FOREIGN KEY (`draw_id`) REFERENCES `accounts_draw` (`id`),
  ADD CONSTRAINT `accounts_winner_user_id_9fa72d6b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
