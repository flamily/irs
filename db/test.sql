/*
 * Purpose: Using the data model definined by `schema.sql`, this script will
 *          load the database with a series of test records.
 *
 * Author: Andrew Pope
 * Date: 2018-09-14
 */

-- Create some staff profiles
INSERT INTO staff (username, password, first_name, last_name, permission)
VALUES (
  'jclank',
  'c0cfd5754185d29c6ffea84f2fa16207697c3ccb472356b931e06d0478e7c1d1', --password is 'jclank' SHA256
  'johnny',
  'clank',
  'robot'
);

INSERT INTO staff (username, password, first_name, last_name, permission)
VALUES (
  'ckramer',
  '35425042f61ef16208c366831f67b78d35302ce99c1d5d33958307e478b8088e', --password is 'ckramer' SHA256
  'cosmo',
  'kramer',
  'wait_staff'
);

INSERT INTO staff (username, password, first_name, last_name, permission)
VALUES (
  'gcostanza',
  'a79cd3eff3ba06db6271ac674503a5cd2fab9ea0d9723591049de31cc08c2ebc', --password is 'gcostanza' SHA256
  'george',
  'Costanza',
  'management'
);

-- Create a dining table and specify the first event for it
BEGIN;
WITH temp(id) as (
  INSERT INTO dining_table (capacity, x_pos, y_pos, width, height, shape)
  VALUES (3, 4, 5, 6, 7, 'rectangle')
  RETURNING dining_table_id
)

INSERT INTO event (description, dining_table_id)
VALUES ('ready', (SELECT id from temp));

END;

-- Create a reservation at the dining table and seat the customers
BEGIN;
WITH res(id) as (
  INSERT INTO reservation (group_size)
  VALUES (1) -- Table for one :(
  RETURNING reservation_id
)

-- Create a seated event and link to reservation
, ev(id) as (
  INSERT INTO event (description, dining_table_id)
  VALUES ('seated', (SELECT dining_table_id from dining_table LIMIT 1))
  RETURNING event_id
)

INSERT INTO customer_event (event_id, reservation_id, staff_id)
VALUES (
  (SELECT id from ev),
  (SELECT id from res),
  (SELECT staff_id from staff WHERE staff.username='ckramer')
);

END;
