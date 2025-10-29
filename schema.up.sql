-- Create gas_tracker schema
CREATE SCHEMA IF NOT EXISTS AUTHORIZATION gas_tracker;

-- Set role to gas_tracker user;
SET ROLE gas_tracker;

-- Create users table
CREATE TABLE IF NOT EXISTS gas_tracker.users
(
    user_id varchar(255) NOT NULL,

    username varchar(255) NOT NULL,

    f_name varchar(255),
    l_name varchar(255),

    email varchar(255),

    PRIMARY KEY (user_id)
);


-- Create vehicles table
CREATE TABLE IF NOT EXISTS gas_tracker.vehicles
(
    vehicle_id uuid UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    owner_id varchar(255) NOT NULL,

    label varchar(255),

    make varchar(255),
    model varchar(255),
    color varchar(255),

    created_on timestamp(0) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_on timestamp(0) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (vehicle_id),
    FOREIGN KEY (owner_id) REFERENCES gas_tracker.users(user_id)
);


-- Create has_access relation table
CREATE TABLE IF NOT EXISTS gas_tracker.has_access
(
    user_id varchar(255) NOT NULL,
    vehicle_id uuid NOT NULL,

    PRIMARY KEY (user_id, vehicle_id),
    FOREIGN KEY (user_id) REFERENCES gas_tracker.users(user_id),
    FOREIGN KEY (vehicle_id) REFERENCES gas_tracker.vehicles(vehicle_id)
);


-- Create gas_stations table
CREATE TABLE IF NOT EXISTS gas_tracker.gas_stations
(
    station_id serial NOT NULL,

    company varchar(255) NOT NULL,

    PRIMARY KEY (station_id)
);


-- Create gas_datas table
CREATE TABLE IF NOT EXISTS gas_tracker.receipts
(
    receipt_id uuid NOT NULL DEFAULT gen_random_uuid(),

    user_id varchar(255) NOT NULL, -- Allow different user to add receipt
    vehicle_id uuid NOT NULL,

    station_id serial NOT NULL,
    gallons numeric(6, 3) NOT NULL CHECK (gallons >= 0), -- Range [0, 999.999]
    price_per_gallon numeric(5, 3) NOT NULL CHECK (price_per_gallon >= 0), -- Range [0, 99.999]
    total_cost numeric(9, 2) GENERATED ALWAYS AS (gallons * price_per_gallon) STORED,

    created_on timestamp(0) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_on timestamp(0) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_on timestamp(0) with time zone,

    PRIMARY KEY (receipt_id),
    FOREIGN KEY (user_id) REFERENCES gas_tracker.users(user_id),
    FOREIGN KEY (vehicle_id) REFERENCES gas_tracker.vehicles(vehicle_id) ON DELETE CASCADE,
    FOREIGN KEY (station_id) REFERENCES gas_tracker.gas_stations(station_id) ON DELETE CASCADE
);
