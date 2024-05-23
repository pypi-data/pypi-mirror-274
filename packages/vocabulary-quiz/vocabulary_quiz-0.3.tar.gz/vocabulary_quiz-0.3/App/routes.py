from flask import Blueprint, render_template, request, redirect, url_for
import os
import csv
import random
from datetime import datetime

main = Blueprint('main', __name__)

# 데이터 파일 경로
csv_filename = os.path.join(os.path.dirname(__file__), '../words.csv')
score_filename = os.path.join(os.path.dirname(__file__), '../scores.csv')

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
    with open(score_filename, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Username', 'Date', 'Correct', 'Total']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

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
    if not os.path.exists(score_filename):
        return []

    with open(score_filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader if row['Username'] == username]

# CSV 파일 데이터 로드
loaded_words_dict = read_from_csv(csv_filename)

# 매일 30개의 단어를 임의로 추출
def get_random_words(words_dict, num_words=30):
    return random.sample(list(words_dict.items()), num_words)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/quiz', methods=['POST'])
def start_quiz():
    username = request.form.get('username')
    random_words = get_random_words(loaded_words_dict)
    return render_template('quiz.html', username=username, random_words=random_words)

@main.route('/submit', methods=['POST'])
def submit_quiz():
    username = request.form.get('username')
    correct_answers = int(request.form.get('correct_answers'))
    total_questions = int(request.form.get('total_questions'))
    save_score(username, correct_answers, total_questions)
    return redirect(url_for('main.view_scores_route', username=username))

@main.route('/scores', methods=['POST'])
def view_scores_route():
    username = request.form.get('username')
    scores = view_scores(username)
    return render_template('scores.html', username=username, scores=scores)
