-- dim_channels: A dimension table with information about each Telegram channel.
-- One row per unique channel (Metadata and grouping)

{{ config(materialized='table') }}

with source as (
    select distinct
        channel_username,
        channel_title
    from {{ ref('stg_telegram_messages') }}
    where channel_username is not null
)

select
    row_number() over (order by channel_username) as channel_id,
    channel_username,
    channel_title
from source
