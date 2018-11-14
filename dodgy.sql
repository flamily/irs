select * from reservation r limit 10;

select * from satisfaction limit 10;

select * from event limit 10;

--- STAFF ID AND "reservation"
select all_e.staff_id, all_c_e.reservation_id
    from event all_e
    join customer_event all_c_e
        on all_c_e.event_id = all_e.event_id

select array_agg(DISTINCT group_size) from reservation r limit 10;

select e_start.event_id, s_start.reservation_id, s_start.score from satisfaction s_start
join event e_start on s_start.event_id = e_start.event_id
where e_start.description = 'seated';

select e_start.event_id, s_start.reservation_id, s_start.score from satisfaction s_start
join event e_start on s_start.event_id = e_start.event_id
where e_start.description = 'paid';

--- wew lad ^^^^^


---- GENERIC

select
    r.reservation_id,
    r.reservation_dt as r_date,
    (sat_end.score - sat_start.score) as delta,
    sat_start.event_id as e_start,
    sat_start.score as score_start,
    sat_end.event_id as e_end,
    sat_end.score as score_end
from reservation r
join
(
    select e_start.event_id, s_start.reservation_id, s_start.score, e_start.description from satisfaction s_start
    join event e_start on s_start.event_id = e_start.event_id
    where e_start.description = 'seated'
) as sat_start on sat_start.reservation_id = r.reservation_id
join
(
    select e_end.event_id, s_end.reservation_id, s_end.score, e_end.description from satisfaction s_end
    join event e_end on s_end.event_id = e_end.event_id
    where e_end.description = 'paid'
) as sat_end on sat_end.reservation_id = r.reservation_id
limit 10;



---- Per Reservation
CREATE VIEW SPAGHET AS
WITH staff_per_res as (
    select
        distinct all_e.staff_id as staff_id,
        all_c_e.reservation_id as res_id
    from event all_e
    join customer_event all_c_e
        on all_c_e.event_id = all_e.event_id
), connect_css as (
    select
        e_start.event_id,
        s_start.reservation_id,
        s_start.score,
        e_start.description
    from
        satisfaction s_start
    join event e_start
        on s_start.event_id = e_start.event_id
), menu_item_per_res as (
    select
        distinct oi.menu_item_id,
        co.reservation_id as res_id
    from order_item oi
    join customer_order co
        on co.customer_order_id = oi.customer_order_id
)
select
    r.reservation_id,
    r.reservation_dt as r_date,
    sat_start.event_id as e_start,
    sat_end.event_id as e_end,
    staff_per_res.staff_id,
    menu_item_per_res.menu_item_id,
    (sat_end.score - sat_start.score) as delta,
    sat_start.score as score_start,
    sat_end.score as score_end
from reservation r
join connect_css as sat_start
    on sat_start.reservation_id = r.reservation_id
    and sat_start.description = 'seated'
join connect_css as sat_end
    on sat_end.reservation_id = r.reservation_id
    and sat_end.description = 'paid'
join staff_per_res on staff_per_res.res_id = r.reservation_id
join menu_item_per_res on menu_item_per_res.res_id = r.reservation_id
order by reservation_id