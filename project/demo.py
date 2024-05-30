from unittest import result
from neo4j import GraphDatabase
from fastapi import FastAPI
import twitter
import atexit

#global variables
uri = "bolt://localhost:7687"
user = "neo4j"
password = "neo4jneo4j" # modify this accordingly based on your own password

neo_db = twitter.Twitter(uri, user, password)

app = FastAPI(title="Nhóm 13",
                description="Demo Project sử dụng cơ sở dữ liệu Neo4j")

# Links From Interesting Retweets
@app.get("/followlinksfrominterestingretweets", tags=["Chức năng"])
async def find_links_from_interesting_retweets(screen_name):
    result = neo_db.findLinksFromInterestingRetweets(screen_name)
    return result

# Tìm những đề xuất hàng đầu của bạn
@app.get("/topmentionsofyou", tags=["Chức năng"])
async def find_top_mentions_of_you(screen_name):
    result = neo_db.findTopMentionsOfYou(screen_name)
    return result

# Delete User (Node)
@app.delete("/deleteUser", tags=["Chức năng"])
async def delete_User(screen_name):
    result = neo_db.deleteUser(screen_name)
    return result







