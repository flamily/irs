"""
These tests check the constraints of the event relation.

Author: Andrew Pope
Date: 06/10/2018
"""
import pytest
import psycopg2
from irs.test.database.util import (
    insert_staff, insert_restaurant_table, insert_event,
    insert_customer_event, insert_reservation
)

from irs.app.manage_restaurant_table import (
    ManageRestaurantTable
)


def test_valid(database_snapshot):
    """Enter a valid record."""
    with database_snapshot.getconn() as conn:
        with conn.cursor() as curs:
            id1 = insert_restaurant_table(curs, 1, 1, 1, 'ellipse')
            id2 = insert_restaurant_table(curs, 2, 3, 4, 'ellipse')
            s_id = insert_staff(curs, 'gcostanza', 'management')
            insert_event(curs, 'ready', id1, s_id)
            insert_event(curs, 'ready', id2, s_id)
            conn.commit()
            insert_event(curs, 'seated', id1, s_id)
            insert_event(curs, 'seated', id2, s_id)
            conn.commit()
            insert_event(curs, 'attending', id2, s_id)
            conn.commit()

        with conn.cursor() as curs:
            curs.execute("SELECT * from restaurant_table")
            print(curs.fetchall())
            curs.execute("SELECT event_id, restaurant_table_id, description from event")
            print(curs.fetchall())

            curs.execute(
                "SELECT rt.*, et.description "
                "FROM restaurant_table rt "
                "JOIN event et on et.restaurant_table_id=rt.restaurant_table_id "
                "WHERE et.event_id = ("
                " SELECT e.event_id FROM event e "
                " WHERE e.restaurant_table_id = rt.restaurant_table_id "
                " ORDER BY event_dt desc LIMIT 1"
                ")"
            )
            print(curs.fetchall())

        #mgt = ManageRestaurantTable(db_connection)
        #mgt.list()
        assert False
