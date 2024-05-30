from pickle import TRUE
from unittest import result
from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable

from datetime import datetime


class Twitter:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Close the driver connection when finished
        self.driver.close() 

    # Tìm những link thú dị được retweet
    def findLinksFromInterestingRetweets(self, screen_name):
        with self.driver.session() as session:
            result = session.read_transaction(self.__findLinksFromInterestingRetweets, screen_name)
            return {"result": result}
        
    @staticmethod
    def __findLinksFromInterestingRetweets(tx, screen_name):
        query = (
            """MATCH (:User {screen_name: $screen_name})-[:POSTS]->
            (t:Tweet)-[:RETWEETS]->(rt)-[:CONTAINS]->(link:Link)
            RETURN t.id_str AS tweet, link.url AS url, rt.favorites AS favorites
            ORDER BY favorites DESC LIMIT 10"""
        )
        try:
            result = tx.run(query,  screen_name=screen_name)
            return [ {"tweet": record["tweet"], "url": record["url"], "favorites": record["favorites"]} for record in result]
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(query=query, exception=exception))
            raise
    
    #Tìm những đề xuất hàng đầu của bạn
    def findTopMentionsOfYou(self, screen_name):
        with self.driver.session() as session:
            result = session.read_transaction(self.__findTopMentionsOfYou, screen_name)
            return {"result": result}    

    @staticmethod
    def __findTopMentionsOfYou(tx, screen_name):
        query = (
            """MATCH
                (u:User)-[:POSTS]->(t:Tweet)-[:MENTIONS]->(m:User {screen_name: $screen_name})
                WHERE u.screen_name <> ''
                RETURN u.screen_name AS screen_name, COUNT(u.screen_name) AS count 
                ORDER BY count 
                DESC LIMIT 10 """
        )
        try:
            result = tx.run(query,  screen_name=screen_name)
            return [ {"screen_name": record["screen_name"], "count": record["count"]} for record in result]
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(query=query, exception=exception))
            raise 

    # Xóa 1 User
    def deleteUser(self, screen_name):
        with self.driver.session() as session:
            result = session.write_transaction(self.__deleteUser, screen_name)
            return {"result": "DELETED"}
        
    @staticmethod
    def __deleteUser(tx, screen_name):
        query = ("""MATCH (n:User) WHERE n.screen_name= $screen_name DETACH DELETE n """)
        try:
            result = tx.run(query, screen_name=screen_name)
            return [record for record in result]
        except ServiceUnavailable as exception:
            logging.error("delete rating: {query} raised an error: \n {exception}".format(query=query, exception=exception))
            raise 

 


   