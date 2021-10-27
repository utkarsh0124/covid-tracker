# Create and use database specifically for covid tracker
CREATE DATABASE IF NOT EXISTS covid_tracker;
USE covid_tracker;

# Create Table
CREATE TABLE IF NOT EXISTS cv_state_wise(
	s_no INT AUTO_INCREMENT PRIMARY KEY,
    data_date DATE,
	state_name VARCHAR(255) NOT NULL,
	active_today INT,
    total_death INT,
    total_discharged INT
);
