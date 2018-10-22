__author__ = 'Hoangthang'

from bs4 import BeautifulSoup
import requests

def get_object_html(url):
    response = requests.get(url=url)
    data = BeautifulSoup(response.text)
    return data

def get_question(data):
    #print data
    question = data.find('a', {'class': 'question-hyperlink'})
    return question.text

def get_vote_count_post(data):
    vote_counts = data.find('div', {'class': 'vote'})
    vote = vote_counts.find('span', recursive=False)
    return int(vote.text)

def get_content_question(data):
    temp = data.find("div", {'class': 'post-text'}).findChildren()
    content = []
    for elm in temp:
        if len(elm.findChildren()) == 0:
            content.append({'tag name': elm.name, "content": elm.text})
    return content

def get_answers(data):
    content = data.find('div', {'id': 'answers'})
    answers = content.find_all('div', {'class': 'answer'})
    print len(answers)
    for answer in answers:
        get_answer(answer)


def get_answer(answer_content):
    if check_accepted_answer(answer_content) is True:
        username = get_username_comment(answer_content)
        _time = get_time_comment(answer_content)
        content = []
        temp = answer_content.find("div", {'class': 'post-text'}).findChildren()
        for elm in temp:
            if len(elm.findChildren()) == 0:
                content.append({'tag name': elm.name, "content": elm.text})
        return {'user_comment': username, 'data': content, 'answered_time': _time}

def check_accepted_answer(div_content):
    answer_vote = div_content.find('div', {'class': 'vote'})
    accepted = answer_vote.find('span', {'class': 'vote-accepted-on'})
    if accepted is not None and accepted.text == 'accepted':
        return True
    return False


def get_username_comment(answer_content):
    name_element = answer_content.find('div', {'class': 'user-details'})
    name_element = name_element.find_all("a")[0]
    return name_element.text

def get_time_comment(answer_content):
    answered_time = answer_content.find('div', {'class': 'user-action-time'})
    answered_time = answered_time.find('span')
    return answered_time.text
url = 'https://stackoverflow.com/questions/49114011/how-to-check-out-a-pull-request-with-jenkins-pipeline'

data = get_object_html(url)
print get_answers(data)
