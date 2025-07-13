{{ config(materialized='table') }}

with base as (
    select
        m.message_id,
        m.channel_username,
        m.text,
        m.posted_at,
        m.views,
        m.media_type,
        m.message_length,
        m.has_image
    from {{ ref('stg_telegram_messages') }} m
)

select
    b.message_id,
    d.channel_id,
    dt.date_day,
    b.text,
    b.views,
    b.media_type,
    b.message_length,
    b.has_image
from base b
left join {{ ref('dim_channels') }} d
    on b.channel_username = d.channel_username
left join {{ ref('dim_dates') }} dt
    on date_trunc('day', b.posted_at)::date = dt.date_day
