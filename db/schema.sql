/*
 * Purpose: Definition of persistent data model for the IRS relational database.
 *
 * Author: Andrew Pope
 * Date: 2018-09-14
 */

/* Definition of system specific enums */
CREATE TYPE event_e       AS ENUM ('ready', 'seated', 'attending', 'paid', 'maintaining');
CREATE TYPE permission_e  AS ENUM ('robot', 'wait_staff', 'management');
CREATE TYPE shape_e       AS ENUM ('rectangle', 'ellipse');


/*** Definition of relational entities in the system ***/

/* Entity: Staff
 * Purpose: Stores information pertinent to resturant staff. Also used in system authentication.
 */
CREATE TABLE staff (
  staff_id           serial        PRIMARY KEY,
  username           text          NOT NULL UNIQUE,
  password           text          NOT NULL,	-- Should not be stored in plaintext. Stored as a hash.
  first_name         text          NOT NULL,
  last_name          text          NOT NULL,
  start_dt           timestamptz   NOT NULL DEFAULT now(),
  permission         permission_e  NOT NULL
);

/* Entity: Restaurant Table
 * Purpose: Stores information pertinent to a restaurant table. This includes
 *          the capacity of the restaurant table and geometric information for UI rendering.
 */
CREATE TABLE restaurant_table (
  restaurant_table_id     serial        PRIMARY KEY,
  capacity                numeric       NOT NULL CHECK(capacity > 0),
  x_pos                   integer       NOT NULL,
  y_pos                   integer       NOT NULL,
  width                   integer       NOT NULL CHECK(width > 0),
  height                  integer       NOT NULL CHECK(height > 0),
  shape                   shape_e       NOT NULL
);

/* Entity: Event
 * Purpose: Used to maintain a history of what happened at a restaurant table over time.
 *          Also used to infer a restaurant table's state / availability.
 */
CREATE TABLE event (
  event_id                serial        PRIMARY KEY,
  description             event_e       NOT NULL,
  event_dt                timestamptz   NOT NULL DEFAULT now(),
  restaurant_table_id     integer       NOT NULL REFERENCES restaurant_table (restaurant_table_id),
  staff_id                integer       NOT NULL REFERENCES staff (staff_id)
);

/* Entity: Reservation
 * Purpose: A reservation represents knowledge of a restaurant, or previously dined, customer.
 */
CREATE TABLE reservation (
  reservation_id     serial        PRIMARY KEY,
  group_size         numeric       NOT NULL CHECK(group_size > 0),
  reservation_dt     timestamptz   NOT NULL DEFAULT now()
);

/* Entity: Customer Event
 * Purpose: Bridges the relationship between an event that can occur at a restaurant table,
 *          and a customer reservation.
 */
CREATE TABLE customer_event (
  event_id           integer       NOT NULL UNIQUE,
  reservation_id     integer       NOT NULL,
  -- Key definitions
  FOREIGN KEY  (event_id)          REFERENCES event (event_id),
  FOREIGN KEY  (reservation_id)    REFERENCES reservation (reservation_id),
  PRIMARY KEY  (event_id, reservation_id)
);

/* Entity: Satisfaction
 * Purpose: Stores the customer's satisfaction during a specific event.
 */
CREATE TABLE satisfaction (
  event_id           integer       NOT NULL,
  reservation_id     integer       NOT NULL,
  score              numeric       NOT NULL CHECK (score >= 0 AND score <= 100),
  -- Key definitions
  FOREIGN KEY  (event_id, reservation_id)  REFERENCES customer_event (event_id, reservation_id),
  PRIMARY KEY  (event_id, reservation_id)
);

/* Entity: Customer Order
 * Purpose: Associates the customer's order with a reservation.
 *
 * Note: On the ERD this is listed as 'Order', however, this is a reserved
 *       keyword in postgresql.
 */
CREATE TABLE customer_order (
  customer_order_id   serial        PRIMARY KEY,
  order_dt            timestamptz   NOT NULL DEFAULT now(),
  reservation_id      integer       NOT NULL UNIQUE REFERENCES reservation (reservation_id)
);

/* Entity: Menu Item
 * Purpose: Stores the knowledge of a dish on the resturant's menu.
 */
CREATE TABLE menu_item (
  menu_item_id        serial        PRIMARY KEY,
  name                text          NOT NULL UNIQUE,
  description         text          NOT NULL
);

/* Entity: Order Item
 * Purpose: Lists the menu item and quantity a customer has ordered for their meal.
 */
CREATE TABLE order_item (
  customer_order_id   integer       NOT NULL,
  menu_item_id        integer       NOT NULL,
  quantity            numeric       NOT NULL CHECK (quantity > 0),
  -- Key definitions
  FOREIGN KEY  (customer_order_id)  REFERENCES customer_order (customer_order_id),
  FOREIGN KEY  (menu_item_id)       REFERENCES menu_item (menu_item_id),
  PRIMARY KEY  (customer_order_id, menu_item_id)
);

/*** Definition of trigger functions. ***/

/* Function: Check event exists
 * Purpose: Called by the 'restaurant table has event' trigger, this function checks
 *          if a newly created restaurant table has an associated event.
 * Returns: NULL if the event exists. Otherwise, an exception will be raised.
 */
CREATE OR REPLACE FUNCTION check_event_exists()
RETURNS TRIGGER AS
$$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM event WHERE event.restaurant_table_id = NEW.restaurant_table_id) THEN
    RAISE EXCEPTION 'a restaurant table needs at least one associated event';
  END IF;
  RETURN NULL;
END;
$$
LANGUAGE plpgsql;

/* Function: Check customer event exists
 * Purpose: Called by the 'Reservation has customer event' trigger, this function checks
 *          if a newly created reservation has an associated customer event.
 * Returns: NULL if the customer event exists. Otherwise, an exception will be raised.
 */
CREATE OR REPLACE FUNCTION check_customer_event_exists()
RETURNS TRIGGER AS
$$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM customer_event WHERE customer_event.reservation_id = NEW.reservation_id) THEN
    RAISE EXCEPTION 'a reservation needs at least one associated customer event';
  END IF;
  RETURN NULL;
END;
$$
LANGUAGE plpgsql;

/* Function: Validates that a customer event is of the right type.
 * Purpose: Called by the 'Customer event is valid' trigger, this function checks
 *          if a newly created customer event is valid as defined by the buisness rules.
 * Returns: NEW if the customer event is valid. Otherwise, an exception will be raised.
 */
CREATE OR REPLACE FUNCTION validate_customer_event()
RETURNS TRIGGER AS
$$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM event WHERE event.event_id = NEW.event_id AND description IN ('seated', 'attending', 'paid')) THEN
    RAISE EXCEPTION 'a customer event can only be of types: seated, attended or paid';
  END IF;
  RETURN NEW;
END;
$$
LANGUAGE plpgsql;

/* Function: Validates the state change on a resturant table.
 * Purpose: Called by the 'State change is valid' trigger, this function checks
 *          if a newly created event is valid as defined by the buisness rules.
 * Returns: NEW if the new event is valid. Otherwise, an exception will be raised.
 */
CREATE OR REPLACE FUNCTION validate_state_change()
RETURNS TRIGGER AS
$$
DECLARE
  latest_event event_e;
BEGIN
  IF NOT EXISTS (SELECT 1 from event where event.restaurant_table_id = NEW.restaurant_table_id) THEN
    RETURN NEW; -- A state for this resturant table has yet to be specified
  END IF;

  latest_event = (SELECT description from event
    WHERE event.restaurant_table_id = NEW.restaurant_table_id
    ORDER BY event_dt desc LIMIT 1
  );

  CASE NEW.description
    WHEN 'ready' THEN
      IF latest_event NOT IN ('maintaining', 'paid') THEN
        RAISE EXCEPTION 'a table can only become ready after being paid or maintained';
      END IF;
    WHEN 'maintaining' THEN
      IF latest_event NOT IN ('ready') THEN
        RAISE EXCEPTION 'a table can only be maintained if it was initially ready';
      END IF;
    WHEN 'seated' THEN
      IF latest_event NOT IN ('ready') THEN
        RAISE EXCEPTION 'a customer cannot be seated at a table if it was not available';
      END IF;
    WHEN 'attending' THEN
      IF latest_event NOT IN ('seated', 'attending') THEN
        RAISE EXCEPTION 'a table cannot be attended if not currently occupied by customers';
      END IF;
    WHEN 'paid' THEN
      IF latest_event NOT IN ('seated', 'attending') THEN
        RAISE EXCEPTION 'only an occupied table can be paid for';
      END IF;
    ELSE
      RAISE EXCEPTION 'unhandled state change';
  END CASE;
  RETURN NEW;
END;
$$
LANGUAGE plpgsql;

/*** Definition of trigger constraints. ***/

/* Constraint Trigger: restaurant table has event
 * Purpose: This trigger will check that at a restaurant table has at least one associated event
 *          prior to the end of the transaction. This is to enforce a begining state upon
 *          the restaurant table.
 */
CREATE CONSTRAINT TRIGGER restaurant_table_has_event
  AFTER INSERT ON restaurant_table
  DEFERRABLE INITIALLY DEFERRED
  FOR EACH ROW
  EXECUTE PROCEDURE check_event_exists();

/* Constraint Trigger: Reservation has customer event
 * Purpose: This trigger will check that at a reservation has at least one associated
 *          customer event prior to the end of the transaction. This is to enforce a
 *          begining state upon the reservation.
 */
CREATE CONSTRAINT TRIGGER reservation_has_customer_event
  AFTER INSERT ON reservation
  DEFERRABLE INITIALLY DEFERRED
  FOR EACH ROW
  EXECUTE PROCEDURE check_customer_event_exists();

/* Constraint Trigger: Customer event is valid
 * Purpose: This trigger will check that at a newly created customer event
 *          correctly references a subset of event types (as defined by the
 *          buisness rules) in the events table.
 *          Valid events include seated, attended, and paid.
 */
CREATE TRIGGER customer_event_is_valid
  BEFORE INSERT ON customer_event
  FOR EACH ROW
  EXECUTE PROCEDURE validate_customer_event();

/* Constraint Trigger: State change is valid
 * Purpose: This trigger will check that at a newly created event
 *          is correctly transitioning the resturant table to a new state (as
 *          defined by the buisness rules).
 */
CREATE TRIGGER state_change_is_valid
  BEFORE INSERT ON event
  FOR EACH ROW
  EXECUTE PROCEDURE validate_state_change();
