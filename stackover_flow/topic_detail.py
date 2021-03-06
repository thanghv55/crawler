__author__ = 'Hoangthang'

from bs4 import BeautifulSoup
import requests
import json
import re
import traceback

BASE_LINK = "https://stackoverflow.com"


def get_topic_detail(url):
    result = {}
    data = get_object_html(url)
    answers = get_answers(data)
    title_question = get_title_question(data)
    content_question = get_content_question(data)
    question_vote_count = get_vote_count_post(data)
    tags = get_tag(data)
    if answers is not None and len(answers) != 0:
        result['answers'] = answers
        result['title_question'] = title_question
        result['content_question'] = content_question
        result['question_vote_count'] = question_vote_count
        result['tags'] = tags
        result['url'] = url
        result['url_id'] = get_id_url(url)
    return result

def get_object_html(url):
    response = requests.get(url=url)
    data = BeautifulSoup(response.text)
    return data

def get_title_question(data):
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
            if elm.name == 'a':
                content.append({'tag_name': elm.name, "content": elm.text, "link": BASE_LINK + elm['href']})
            else:
                content.append({'tag_name': elm.name, "content": elm.text})
    return content

def get_answers(data):
    answer_result = []
    content = data.find('div', {'id': 'answers'})
    answers = content.find_all('div', {'class': 'answer'})
    for answer in answers:
        temp = get_answer(answer)
        if temp is not None:
            answer_result.append(temp)
    return answer_result


def get_answer(answer_content):
    if check_accepted_answer(answer_content) is True:
        username = get_username_comment(answer_content)
        _time = get_time_comment(answer_content)
        content = []
        temp = answer_content.find("div", {'class': 'post-text'}).findChildren()
        for elm in temp:
            if len(elm.findChildren()) == 0:
                if elm.name == 'a':
                    content.append({'tag_name': elm.name, "content": elm.text, "link": BASE_LINK + elm['href']})
                else:
                    content.append({'tag_name': elm.name, "content": elm.text})
        return {'user_comment': username, 'data': content, 'answered_time': _time}
    return None

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

def get_tag(data):
    tags_result = []
    tags = data.find_all('a', {'class': 'post-tag'})
    if tags is not None:
        for tag in tags:
            tags_result.append({'tag': tag.text, 'link': BASE_LINK + tag['href']})
    return tags_result

def get_id_url(url):
    try:
        temp = re.findall('\d+', url)
        if temp:
            return int(temp[0])
    except:
        traceback.print_exc()
    return -1

url = 'https://stackoverflow.com/questions/49114011/how-to-check-out-a-pull-request-with-jenkins-pipeline'
#data = get_object_html(url)
#print get_answers(data)
#print get_topic_detail(url)
print(get_id_url(url))
#get_tag(data)
