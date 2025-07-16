from fastapi import FastAPI
from fastapi import Path
from api.crud import get_top_products, get_channel_activity, search_messages
from api.schemas import ObjectStat, ChannelActivity, MessageSearchResult, ChannelSlug


# ______________ API Endpoints ______________#
app = FastAPI()


# ______________ Get top products ______________#
# This endpoint retrieves the top products based on mentions and confidence scores.
@app.get("/api/reports/top-products", response_model=list[ObjectStat])
def read_top_products(limit: int = 10):
    return get_top_products(limit)


# ______________ Get all channel slugs ______________#
# This endpoint retrieves all distinct channel slugs from the database.
@app.get("/api/channels/{channel_slug}/activity", response_model=list[ChannelActivity])
def read_channel_activity(channel_slug: ChannelSlug = Path(...)):
    return get_channel_activity(channel_slug.value)


# ______________ Search messages ______________#
# This endpoint allows searching for messages containing a specific query string.
@app.get("/api/search/messages", response_model=list[MessageSearchResult])
def read_search_messages(query: str):
    return search_messages(query)
