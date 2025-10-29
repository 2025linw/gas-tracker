INSERT INTO gas_tracker.users (user_id, username) VALUES
('00000000-0000-0000-0000-000000000000', 'testuser1'),
('00000000-0000-0000-0000-000000000001', 'testuser2');

INSERT INTO gas_tracker.gas_stations (company) VALUES
('Holiday'),
('Marathon'),
('Cenex'),
('Costco');

INSERT INTO gas_tracker.vehicles (vehicle_id, owner_id, label, color) VALUES
('00000000-0000-0000-0000-000000000000', '00000000-0000-0000-0000-000000000000', 'Test Car 1', 'gray'),
('00000000-0000-0000-0000-000000000001', '00000000-0000-0000-0000-000000000001', 'Test Car 2', 'blue'),
('00000000-0000-0000-0000-000000000002', '00000000-0000-0000-0000-000000000001', 'Test Car 3', 'silver');

INSERT INTO gas_tracker.has_access (user_id, vehicle_id) VALUES
(
    '00000000-0000-0000-0000-000000000000', '00000000-0000-0000-0000-000000000002'
);
