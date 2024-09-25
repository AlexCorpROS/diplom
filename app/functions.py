import os.path
import secrets
from PIL import Image
from flask import current_app

import spacy
from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel
import fasttext

fasttext.FastText.eprint = lambda x: None


def save_picture(picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.config['SERVER_PATH'], picture_fn)
    output_size = (125, 125)
    img = Image.open(picture)
    img.thumbnail(output_size)
    img.save(picture_path)
    return picture_fn

def review(text):
    lemma = []    
    
    nlp2 = spacy.load("ru_core_news_sm")
    text = text
    doc = nlp2(text)
    
    # Удаляем стопслова
    filtered_words = [token.text for token in doc if not token.is_stop]
    
    # Получим очищенную строку слов
    clean_text = ' '.join(filtered_words)
    
    # Проведем лематизацию слов
    for doc in nlp2.pipe([clean_text]):
        lemma.append([n.lemma_ for n in doc])
        
    # Получим очищенную строку слов приведенных к нормальной форме.
    text_lemma = ' '.join(lemma[0])
            
    tokenizer = RegexTokenizer()
    model = FastTextSocialNetworkModel(tokenizer=tokenizer)

    # Посмотрим на результаты работы модели для оригинального и обработанного текста
    results = model.predict([text])
    results_lem = model.predict([text_lemma])
       
    for items in results:
            res = items.get('positive') - items.get('negative')

    for items in results_lem:
            res_lemm = items.get('positive') - items.get('negative')       
    
    # В итоговый вывод отдаем усредyенный результат обеих подходов        
    return round((res + res_lemm)/2, 2)



def overall_rating(list):
    ''' Функция для оценки общего настроения отзывов. Так как используемая модель не очень точна, то мы будем учитывать 
    только полярные значения, без значения веса предсказания'''
    tmp = 0

    for i in list:
        if i > 0:
            tmp += 1
        elif i < 0:
            tmp -= 1
    
    tmp = tmp/len(list)
    if tmp > 0.2:
        res = 'Хороший'
    elif tmp < -0.2:
        res = 'Плохой'
    else:
        res = 'Нейтральный'
    return res 

