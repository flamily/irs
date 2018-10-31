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
  '$5$rounds=535000$fHNettCoJWtNUYkf$FFzzNYIpZ4nqpgLfa5aMOuCTxV3a2PP5AJkrxJQHCy2', --password is 'jclank' sha256_crypt
  'johnny',
  'clank',
  'robot'
);

INSERT INTO staff (username, password, first_name, last_name, permission)
VALUES (
  'ckramer',
  '$5$rounds=535000$OvSwVSaJ2RcK0jpS$G/cukyv6qmoDkT3YcCf.O6VDrmuCtv9wBi4p12agCH2', --password is 'ckramer' sha256_crypt
  'cosmo',
  'kramer',
  'wait_staff'
);

INSERT INTO staff (username, password, first_name, last_name, permission)
VALUES (
  'gcostanza',
  '$5$rounds=535000$x7FdjKGvYTQPWoML$1RgQMrBI4j9Y1sHfE1tpONChJeqtidxYwSl/O9Y/XL8', --password is 'gcostanza' sha256_crypt
  'george',
  'Costanza',
  'management'
);

-- Create a restaurant table and specify the first event for it
BEGIN;
WITH temp(id) as (
  INSERT INTO restaurant_table (capacity, x_pos, y_pos, width, height, shape)
  VALUES (3, 4, 5, 6, 7, 'rectangle')
  RETURNING restaurant_table_id
)

INSERT INTO event (description, restaurant_table_id, staff_id)
VALUES ('ready', (SELECT id from temp), 1);
END;

-- Create a reservation at the restaurant table and seat the customers
BEGIN;
WITH res(id) as (
  INSERT INTO reservation (group_size)
  VALUES (1) -- Table for one :(
  RETURNING reservation_id
)

-- Create a seated event and link to reservation
, ev(id) as (
  INSERT INTO event (description, restaurant_table_id, staff_id)
  VALUES ('seated', (SELECT restaurant_table_id from restaurant_table LIMIT 1), 1)
  RETURNING event_id
)

INSERT INTO customer_event (event_id, reservation_id)
VALUES (
  (SELECT id from ev),
  (SELECT id from res)
);
END;
