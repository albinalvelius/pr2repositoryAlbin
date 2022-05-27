-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Värd: 127.0.0.1
-- Tid vid skapande: 27 maj 2022 kl 18:19
-- Serverversion: 10.4.22-MariaDB
-- PHP-version: 8.1.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Databas: `databas`
--

-- --------------------------------------------------------

--
-- Tabellstruktur `bus_trips`
--

CREATE TABLE `bus_trips` (
  `id` int(11) NOT NULL,
  `bus_from` varchar(50) NOT NULL,
  `bus_to` varchar(50) NOT NULL,
  `brand` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumpning av Data i tabell `bus_trips`
--

INSERT INTO `bus_trips` (`id`, `bus_from`, `bus_to`, `brand`) VALUES
(3, 'washington', 'moscow', 'bus'),
(4, 'Stockholm', 'Madrid', 'Mercedes');

-- --------------------------------------------------------

--
-- Tabellstruktur `client_booking`
--

CREATE TABLE `client_booking` (
  `id` int(100) NOT NULL,
  `idClient` int(100) NOT NULL,
  `idBus` int(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumpning av Data i tabell `client_booking`
--

INSERT INTO `client_booking` (`id`, `idClient`, `idBus`) VALUES
(3, 5, 3);

-- --------------------------------------------------------

--
-- Tabellstruktur `client_info`
--

CREATE TABLE `client_info` (
  `id` int(100) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `age` int(100) NOT NULL,
  `height` int(100) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumpning av Data i tabell `client_info`
--

INSERT INTO `client_info` (`id`, `first_name`, `last_name`, `age`, `height`, `username`, `password`) VALUES
(1, 'albin', 'alvelius', 12, 157, 'albin5', 'albin55'),
(4, 'man3', 'man5', 12, 67, 'victor', 'foreseebäck'),
(5, 'admin', 'admin', 99, 199, 'admin', 'admin'),
(6, 'Victor', 'Victor', 1993, 180, 'xX_gamingHamzterz_Xx', '[]qrsKtl//4'),
(8, 'victor', 'rufus', 12, 185, 'rey', 'skywalekr'),
(9, 'debug', 'debug', 12, 12, 'user', 'user');

--
-- Index för dumpade tabeller
--

--
-- Index för tabell `bus_trips`
--
ALTER TABLE `bus_trips`
  ADD PRIMARY KEY (`id`);

--
-- Index för tabell `client_booking`
--
ALTER TABLE `client_booking`
  ADD PRIMARY KEY (`id`);

--
-- Index för tabell `client_info`
--
ALTER TABLE `client_info`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT för dumpade tabeller
--

--
-- AUTO_INCREMENT för tabell `bus_trips`
--
ALTER TABLE `bus_trips`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT för tabell `client_booking`
--
ALTER TABLE `client_booking`
  MODIFY `id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT för tabell `client_info`
--
ALTER TABLE `client_info`
  MODIFY `id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
