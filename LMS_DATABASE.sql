-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Dec 22, 2024 at 07:48 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `LMS_DATABASE`
--

-- --------------------------------------------------------

--
-- Table structure for table `ADMINS`
--

CREATE TABLE `ADMINS` (
  `admin_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `admin_level` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `BOOKS`
--

CREATE TABLE `BOOKS` (
  `book_id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `author` varchar(255) NOT NULL,
  `genre` varchar(100) DEFAULT NULL,
  `stock` int(11) DEFAULT 0,
  `location` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `BOOKS`
--

INSERT INTO `BOOKS` (`book_id`, `title`, `author`, `genre`, `stock`, `location`, `created_at`) VALUES
(1, 'The Great Gatsby (Updated)', 'F. Scott Fitzgerald', 'Fiction', 7, 'Shelf A2', '2024-12-20 14:03:45'),
(2, 'To Kill a Mockingbird', 'Harper Lee', 'Fiction', 5, 'Shelf B2', '2024-12-20 14:03:45'),
(3, '1984', 'George Orwell', 'Dystopian', 8, 'Shelf C3', '2024-12-20 14:03:45'),
(4, 'Sapiens', 'Yuval Noah Harari', 'Non-Fiction', 12, 'Shelf D4', '2024-12-20 14:03:45');

-- --------------------------------------------------------

--
-- Table structure for table `BOOK_ORDERS`
--

CREATE TABLE `BOOK_ORDERS` (
  `order_id` int(11) NOT NULL,
  `book_id` int(11) NOT NULL,
  `vendor_name` varchar(255) NOT NULL,
  `quantity` int(11) NOT NULL,
  `order_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `expected_delivery_date` date NOT NULL,
  `order_status` varchar(50) DEFAULT 'Pending'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `BOOK_ORDERS`
--

INSERT INTO `BOOK_ORDERS` (`order_id`, `book_id`, `vendor_name`, `quantity`, `order_date`, `expected_delivery_date`, `order_status`) VALUES
(2, 1, 'ABC Books Supplies', 10, '2024-12-22 16:06:29', '2024-12-30', 'Pending');

-- --------------------------------------------------------

--
-- Table structure for table `BORROWED_BOOKS`
--

CREATE TABLE `BORROWED_BOOKS` (
  `borrow_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `book_id` int(11) NOT NULL,
  `borrow_date` date NOT NULL,
  `due_date` date NOT NULL,
  `return_date` date DEFAULT NULL,
  `fine_amount` decimal(10,2) DEFAULT 0.00
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `DIGITAL_ACCESS`
--

CREATE TABLE `DIGITAL_ACCESS` (
  `digital_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `eBook_title` varchar(255) NOT NULL,
  `access_date` date NOT NULL,
  `backup_status` enum('pending','completed') DEFAULT 'pending'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `FINES`
--

CREATE TABLE `FINES` (
  `fine_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `borrow_id` int(11) NOT NULL,
  `fine_rate` decimal(10,2) NOT NULL,
  `fine_amount` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `LIBRARIANS`
--

CREATE TABLE `LIBRARIANS` (
  `librarian_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `hire_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `MEMBERS`
--

CREATE TABLE `MEMBERS` (
  `member_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `membership_date` date NOT NULL,
  `status` enum('active','inactive') DEFAULT 'active'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `MEMBERSHIP_TIERS`
--

CREATE TABLE `MEMBERSHIP_TIERS` (
  `tier_id` int(11) NOT NULL,
  `tier_name` varchar(50) NOT NULL,
  `borrowing_limit` int(11) NOT NULL,
  `fine_discount` decimal(5,2) DEFAULT 0.00
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `MEMBERSHIP_TIERS`
--

INSERT INTO `MEMBERSHIP_TIERS` (`tier_id`, `tier_name`, `borrowing_limit`, `fine_discount`) VALUES
(1, 'Basic', 3, 0.00),
(2, 'Premium', 5, 10.00),
(3, 'Elite', 10, 20.00);

-- --------------------------------------------------------

--
-- Table structure for table `MEMBER_TIERS`
--

CREATE TABLE `MEMBER_TIERS` (
  `member_tier_id` int(11) NOT NULL,
  `member_id` int(11) NOT NULL,
  `tier_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `NOTIFICATIONS`
--

CREATE TABLE `NOTIFICATIONS` (
  `notification_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `type` enum('email','sms') NOT NULL,
  `message` text NOT NULL,
  `sent_date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `SYSTEM_POLICIES`
--

CREATE TABLE `SYSTEM_POLICIES` (
  `policy_id` int(11) NOT NULL,
  `policy_name` varchar(255) NOT NULL,
  `policy_value` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `SYSTEM_POLICIES`
--

INSERT INTO `SYSTEM_POLICIES` (`policy_id`, `policy_name`, `policy_value`, `created_at`) VALUES
(1, 'Max Borrow Limit', '5', '2024-12-20 14:05:39'),
(2, 'Overdue Fine Per Day', '2.00', '2024-12-20 14:05:39'),
(3, 'Membership Renewal Fee', '50.00', '2024-12-20 14:05:39');

-- --------------------------------------------------------

--
-- Table structure for table `USERS`
--

CREATE TABLE `USERS` (
  `user_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `user_type` enum('member','librarian','admin') NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `USERS`
--

INSERT INTO `USERS` (`user_id`, `name`, `email`, `password`, `phone`, `user_type`, `created_at`) VALUES
(5, 'Librarian User', 'librarian@example.com', 'pbkdf2:sha256:1000000$N7oxMAheAKn5dHid$73b3464a3a8d4cd4ed522926c299bec89888f5f5a8d6fd219662bb70302483f2', '1234567890', 'librarian', '2024-12-22 16:29:44'),
(6, 'Admin User', 'admin@example.com', 'pbkdf2:sha256:1000000$SFX9uhnyEbIUQUxA$952eb8a05c360b524418cfe561844e34879980535056ffeb7c0c87cc786890e8', '0987654321', 'admin', '2024-12-22 16:29:44'),
(7, 'Member User', 'member@example.com', 'pbkdf2:sha256:1000000$HqtZCKeNVjHZL3Wo$dcd6d1c5c693fad4a046dbb61a7b22ea76e87161f37f83f7e806d8887cf93bb4', '1122334455', 'member', '2024-12-22 16:29:45');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `ADMINS`
--
ALTER TABLE `ADMINS`
  ADD PRIMARY KEY (`admin_id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indexes for table `BOOKS`
--
ALTER TABLE `BOOKS`
  ADD PRIMARY KEY (`book_id`);

--
-- Indexes for table `BOOK_ORDERS`
--
ALTER TABLE `BOOK_ORDERS`
  ADD PRIMARY KEY (`order_id`),
  ADD KEY `book_id` (`book_id`);

--
-- Indexes for table `BORROWED_BOOKS`
--
ALTER TABLE `BORROWED_BOOKS`
  ADD PRIMARY KEY (`borrow_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `book_id` (`book_id`);

--
-- Indexes for table `DIGITAL_ACCESS`
--
ALTER TABLE `DIGITAL_ACCESS`
  ADD PRIMARY KEY (`digital_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `FINES`
--
ALTER TABLE `FINES`
  ADD PRIMARY KEY (`fine_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `borrow_id` (`borrow_id`);

--
-- Indexes for table `LIBRARIANS`
--
ALTER TABLE `LIBRARIANS`
  ADD PRIMARY KEY (`librarian_id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indexes for table `MEMBERS`
--
ALTER TABLE `MEMBERS`
  ADD PRIMARY KEY (`member_id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indexes for table `MEMBERSHIP_TIERS`
--
ALTER TABLE `MEMBERSHIP_TIERS`
  ADD PRIMARY KEY (`tier_id`);

--
-- Indexes for table `MEMBER_TIERS`
--
ALTER TABLE `MEMBER_TIERS`
  ADD PRIMARY KEY (`member_tier_id`),
  ADD KEY `member_id` (`member_id`),
  ADD KEY `tier_id` (`tier_id`);

--
-- Indexes for table `NOTIFICATIONS`
--
ALTER TABLE `NOTIFICATIONS`
  ADD PRIMARY KEY (`notification_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `SYSTEM_POLICIES`
--
ALTER TABLE `SYSTEM_POLICIES`
  ADD PRIMARY KEY (`policy_id`);

--
-- Indexes for table `USERS`
--
ALTER TABLE `USERS`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `BOOKS`
--
ALTER TABLE `BOOKS`
  MODIFY `book_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `BOOK_ORDERS`
--
ALTER TABLE `BOOK_ORDERS`
  MODIFY `order_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `BORROWED_BOOKS`
--
ALTER TABLE `BORROWED_BOOKS`
  MODIFY `borrow_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `DIGITAL_ACCESS`
--
ALTER TABLE `DIGITAL_ACCESS`
  MODIFY `digital_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `FINES`
--
ALTER TABLE `FINES`
  MODIFY `fine_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `MEMBERSHIP_TIERS`
--
ALTER TABLE `MEMBERSHIP_TIERS`
  MODIFY `tier_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `MEMBER_TIERS`
--
ALTER TABLE `MEMBER_TIERS`
  MODIFY `member_tier_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `NOTIFICATIONS`
--
ALTER TABLE `NOTIFICATIONS`
  MODIFY `notification_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `SYSTEM_POLICIES`
--
ALTER TABLE `SYSTEM_POLICIES`
  MODIFY `policy_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `USERS`
--
ALTER TABLE `USERS`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `ADMINS`
--
ALTER TABLE `ADMINS`
  ADD CONSTRAINT `admins_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `USERS` (`user_id`) ON DELETE CASCADE;

--
-- Constraints for table `BOOK_ORDERS`
--
ALTER TABLE `BOOK_ORDERS`
  ADD CONSTRAINT `book_orders_ibfk_1` FOREIGN KEY (`book_id`) REFERENCES `BOOKS` (`book_id`);

--
-- Constraints for table `BORROWED_BOOKS`
--
ALTER TABLE `BORROWED_BOOKS`
  ADD CONSTRAINT `borrowed_books_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `USERS` (`user_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `borrowed_books_ibfk_2` FOREIGN KEY (`book_id`) REFERENCES `BOOKS` (`book_id`) ON DELETE CASCADE;

--
-- Constraints for table `DIGITAL_ACCESS`
--
ALTER TABLE `DIGITAL_ACCESS`
  ADD CONSTRAINT `digital_access_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `USERS` (`user_id`) ON DELETE CASCADE;

--
-- Constraints for table `FINES`
--
ALTER TABLE `FINES`
  ADD CONSTRAINT `fines_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `USERS` (`user_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fines_ibfk_2` FOREIGN KEY (`borrow_id`) REFERENCES `BORROWED_BOOKS` (`borrow_id`) ON DELETE CASCADE;

--
-- Constraints for table `LIBRARIANS`
--
ALTER TABLE `LIBRARIANS`
  ADD CONSTRAINT `librarians_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `USERS` (`user_id`) ON DELETE CASCADE;

--
-- Constraints for table `MEMBERS`
--
ALTER TABLE `MEMBERS`
  ADD CONSTRAINT `members_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `USERS` (`user_id`) ON DELETE CASCADE;

--
-- Constraints for table `MEMBER_TIERS`
--
ALTER TABLE `MEMBER_TIERS`
  ADD CONSTRAINT `member_tiers_ibfk_1` FOREIGN KEY (`member_id`) REFERENCES `MEMBERS` (`member_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `member_tiers_ibfk_2` FOREIGN KEY (`tier_id`) REFERENCES `MEMBERSHIP_TIERS` (`tier_id`) ON DELETE CASCADE;

--
-- Constraints for table `NOTIFICATIONS`
--
ALTER TABLE `NOTIFICATIONS`
  ADD CONSTRAINT `notifications_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `USERS` (`user_id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
