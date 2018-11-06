__author__ = 'Hoangthang'

import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import topic_detail as top_de
from pymongo import MongoClient
import traceback

BASE_DOMAIN = 'https://stackoverflow.com'

def run():
    url = "https://stackoverflow.com/questions"
    while(True):
        print url
        data = get_object_html(url)
        get_questions(data)
        next_pages = get_next_page(data)
        print next_pages
        if next_pages == -1:
            return
        url = 'https://stackoverflow.com/questions?page=' + str(next_pages) + '&sort=votes'


def get_questions(data):
    questions_object = data.find('div', {'id': 'questions'})
    questions = questions_object.find_all('div', {'class': 'question-summary'})
    if questions is not None:
        print len(questions)
        pool = ThreadPoolExecutor(max_workers=20)
        for question in questions:
            pool.submit(get_question_detail, question)
        pool.shutdown(wait=True)

def get_question_detail(question):
    if check_question(question):
        url = get_question_link(question)
        temp = top_de.get_topic_detail(url)
        if temp is not None:
            insert_mongodb(temp)

def get_question_link(question):
    a = question.find('a', {'class': 'question-hyperlink'})
    return  BASE_DOMAIN + a['href']

def check_question(question):
    #print question
    answered_accepted = question.find('div', {'class': 'answered-accepted'})
    if answered_accepted is None:
        return False
    votes = question.find('div', {'class': 'votes'})
    if votes is None:
        return False
    vote_count = votes.text
    vote_count = vote_count.replace('votes', "").replace(' ', '')
    if int(vote_count) == 0:
        return False
    return True

def get_next_page(data):
    pages = data.find('div', {'class': 'pager'})
    if pages is None:
        return -1
    current_pages = pages.find('span', {'class': 'current'})
    print current_pages.text
    if current_pages is None or int(current_pages.text) <= 0:
        return -1
    return int(current_pages.text) + 1


def get_object_html(url):
    response = requests.get(url=url)
    data = BeautifulSoup(response.text)
    return data

def insert_mongodb(data):
    mongo_client = MongoClient("localhost", 27017)
    try:
        db = mongo_client.get_database("stackover_flow")
        collection = db.get_collection("questions")
        collection.insert(data)
    except:
        traceback.print_exc()

#url = "https://stackoverflow.com/questions"
#data = get_object_html(url)
run()
