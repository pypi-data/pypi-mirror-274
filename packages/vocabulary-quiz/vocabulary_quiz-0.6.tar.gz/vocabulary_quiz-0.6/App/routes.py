from flask import Blueprint, render_template, request, redirect, url_for, flash
import random
import csv
import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup

main = Blueprint('main', __name__)

# 웹 페이지 URL
url = 'https://studytogether.tistory.com/entry/토익단어첫번째'

# 웹 페이지로부터 HTML을 가져옵니다
response = requests.get(url)
response.encoding = 'utf-8'  # 한글 인코딩 문제 해결을 위해 필요

# BeautifulSoup 객체 생성, HTML을 파싱
soup = BeautifulSoup(response.text, 'html.parser')

# <tr> 태그로 각 단어 항목을 찾습니다
rows = soup.find_all('tr')

# 중복을 제거하기 위한 사전 생성
words_dict = {}

# 각 행에서 단어, 발음, 뜻을 추출
for row in rows:
    cells = row.find_all('td')
    if len(cells) >= 2:  # 적어도 두 개의 <td> 태그가 있는 행만 처리
        word = cells[0].text.strip().replace('\xa0', '').split()[0]  # 첫 번째 단어만 사용
        meanings = set(cells[1].text.strip().replace('\xa0', '').split(", "))

        if word in words_dict:
            words_dict[word].update(meanings)
        else:
            words_dict[word] = meanings

# 결과 출력
for word, meanings in words_dict.items():
    combined_meanings = ", ".join(sorted(meanings))
    print(f"Word: {word}, Meaning: {combined_meanings}")

# 총 단어 수 출력
print(f"Total number of unique words: {len(words_dict)}")

# 사전 데이터 저장하기
def save_to_csv(filename, words_dict):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Word', 'Meanings']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for word, meanings in words_dict.items():
            combined_meanings = ", ".join(sorted(meanings))
            writer.writerow({'Word': word, 'Meanings': combined_meanings})

# CSV 파일에서 데이터 읽기
def read_from_csv(filename):
    loaded_words_dict = {}
    with open(filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            word = row['Word']
            meanings = set(row['Meanings'].split(', '))
            loaded_words_dict[word] = meanings
    return loaded_words_dict

# 성적 저장하기
def save_score(username, correct_answers, total_questions):
    score_filename = 'scores.csv'
    with open(score_filename, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Username', 'Date', 'Correct', 'Total']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # 파일이 비어있는 경우 헤더 추가
        if csvfile.tell() == 0:
            writer.writeheader()

        writer.writerow({
            'Username': username,
            'Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Correct': correct_answers,
            'Total': total_questions
        })

# 성적 조회하기
def view_scores(username):
    score_filename = 'scores.csv'
    if not os.path.exists(score_filename):
        return []

    with open(score_filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader if row['Username'] == username]

# 데이터 저장
csv_filename = 'words.csv'
save_to_csv(csv_filename, words_dict)

# CSV 파일 내용 출력
with open(csv_filename, 'r', encoding='utf-8') as file:
    contents = file.read()
    print("CSV File Contents:")
    print(contents)

# 데이터 확인
loaded_words_dict = read_from_csv(csv_filename)
print("Loaded words from CSV:")
for word, meanings in loaded_words_dict.items():
    combined_meanings = ", ".join(sorted(meanings))
    print(f"Word: {word}, Meaning: {combined_meanings}")

# 매일 30개의 단어를 임의로 추출
def get_random_words(words_dict, num_words=30):
    return random.sample(list(words_dict.items()), num_words)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/start_quiz', methods=['POST'])
def start_quiz():
    username = request.form['username'].strip()
    if not username:
        flash('Username cannot be empty')
        return redirect(url_for('main.index'))
    
    random_words = get_random_words(loaded_words_dict)
    return render_template('quiz.html', username=username, random_words=random_words)

@main.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    username = request.form['username']
    answers = request.form.getlist('answers')
    correct_answers = 0

    for i, (word, meanings) in enumerate(get_random_words(loaded_words_dict)):
        if i < len(answers) and answers[i].strip().lower() == word.lower():
            correct_answers += 1

    save_score(username, correct_answers, len(get_random_words(loaded_words_dict)))
    return render_template('result.html', correct=correct_answers, total=len(get_random_words(loaded_words_dict)))

@main.route('/view_scores', methods=['POST'])
def view_scores_route():
    username = request.form['username'].strip()
    if not username:
        flash('Username cannot be empty')
        return redirect(url_for('main.index'))

    scores = view_scores(username)
    return render_template('scores.html', username=username, scores=scores)
