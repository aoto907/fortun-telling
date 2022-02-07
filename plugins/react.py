from slackbot.bot import respond_to  #@メッセージへの応答
from slackbot.bot import listen_to      #チャンネル内発言への応答
from slackbot.bot import default_reply    # デフォルトの応答
from collections import defaultdict
import datetime
import math
import random
import datetime
import re
import slackbot_settings

######### この下にクラスや関数を貼りつける ###########

from janome.tokenizer import Tokenizer

# 単語のクラス
class Word:
    def __init__(self, token):
        # 表層形
        self.text = token.surface

        # 原型
        self.basicForm = token.base_form

        # 品詞
        self.pos = token.part_of_speech
        
    # 単語の情報を「表層系\t原型\t品詞」で返す
    def wordInfo(self):
        return self.text + "\t" + self.basicForm + "\t" + self.pos

# 引数のtextをJanomeで解析して単語リストを返す関数
def janomeAnalyzer(text):
    
    # 形態素解析
    t = Tokenizer()
    tokens = t.tokenize(text) 

    # 解析結果を1行ずつ取得してリストに追加
    wordlist = []
    for token in tokens:
        word = Word(token)
        wordlist.append(word)
    return wordlist

# 星座判定
def Hroscope(Wordlist):
    import numpy as np
    import pprint
    my_bth = defaultdict(list)
    # 各月と日数が辞書型に格納される
    for i in range(12):
        if i == 1:
            for j in range(29):
                my_bth[i+1].append((i+1)*100+j+1)
        elif i == 3 or i == 5 or i == 10:
            for k in range(30):
                my_bth[i+1].append((i+1)*100+k+1)
        else:
            for p in range(31):
                my_bth[i+1].append((i+1)*100+p+1)
    
    number = []
    for w in Wordlist:
        pos2 = w.pos.split(",")
        if pos2[0]=='名詞' and pos2[1]=="数":
            number.append(int(w.basicForm))

    while(True):
        # 該当する星座を返答
        answer = "" 
        
        if (number[0] > 12):
            answer = "そんな日にちは存在しない"
            break
        elif (number[0] <= 12) and (number[1] > 31):
            answer = "そんな日にちは存在しない"
            break
        else:
            my_b = my_bth[number[0]][number[1]]

        # 入力された値から、星座を判定
        if (my_b in my_bth[3][21:]) or (my_b in my_bth[4][:20]):
            answer = "牡羊座"
        elif (my_b in my_bth[4][20:]) or (my_b in my_bth[5][:21]):
            answer = "牡牛座"
        elif (my_b in my_bth[5][21:]) or (my_b in my_bth[6][:22]):
            answer = "双子座"
        elif (my_b in my_bth[6][22:]) or (my_b in my_bth[7][:22]):
            answer = "蟹座"
        elif (my_b in my_bth[7][22:]) or (my_b in my_bth[8][:23]):
            answer = "獅子座"
        elif (my_b in my_bth[8][23:]) or (my_b in my_bth[9][:23]):
            answer = "乙女座"
        elif (my_b in my_bth[9][23:]) or (my_b in my_bth[10][:24]):
            answer = "天秤座"
        elif (my_b in my_bth[10][24:]) or (my_b in my_bth[11][:23]):
            answer = "蠍座"
        elif (my_b in my_bth[11][23:]) or (my_b in my_bth[12][:22]):
            answer = "射手座"
        elif (my_b in my_bth[12][22:]) or (my_b in my_bth[1][:21]):
            answer = "山羊座"
        elif (my_b in my_bth[1][21:]) or (my_b in my_bth[2][:19]):
            answer = "水瓶座"
        elif (my_b in my_bth[2][19:]) or (my_b in my_bth[3][:21]):
            answer = "魚座"
        break
        
    return answer

def GregorianCalendar(wordlist):
    number = []
    for w in wordlist:
        pos2 = w.pos.split(",")
        if pos2[0]=='名詞' and pos2[1]=="数":
            number.append(int(w.basicForm))
    year = number[0]
    month = number[1]
    day = number[2]
    
  # h = math.floor((day + ((26*(month+1))/10) + year + (year/4) - 2*(year/100) + (year/400)) % 7)
    h = math.floor((year + (year/4) - (year/100) + (year/400) + ((13*month+8)/5) + day) % 7)  # ツェリーの公式
    dtow = ["日", "月", "火", "水", "木", "金", "土"]
    
    return dtow[h]
###################################################

# 特定の文字列に対して返答
@respond_to('こんにちは')
def respond(message):
    message.reply('こんにちは！')

@respond_to('あなたは誰？')
def respond(message):
    input = message.user['real_name']
    message.reply('私は、' + input + "のお手伝いをします")

@respond_to('何が出来るの？')
def respond(message):
    with open("answer.txt", "r", encoding="utf-8") as fileobj:
        text = fileobj.read()
        message.reply(text)
    message.reply("以上です。")

@respond_to("今日の運勢、")
def respond(message):
    text = message.body['text']
    wordlist = janomeAnalyzer(text)
    answer = Hroscope(wordlist)
    # ラッキーアイテム
    with open("comment.txt", "r", encoding="utf_8") as fileobje1:
        lucky_items = fileobje1.read()
        items_list = lucky_items.split("\n")
    # 今日の格言
    with open("today_maxim.txt", "r", encoding="utf_8") as fileobje2:
        maxim_comment = fileobje2.read()
        maxim_list = maxim_comment.split("\n")
        
    # 仕事運、恋愛運、金運
    if answer == "そんな日にちは存在しない":
        message.reply(answer)
    else:
        message.reply("今日の" + answer + "の運勢は" + str(random.randint(1,12)) + "位 \n")
        message.reply("仕事運" + random.randint(1,6)*"★")
        message.reply("恋愛運" + random.randint(1,6)*"★")
        message.reply("金運" + random.randint(1,6)*"★")
        message.reply("ラッキーアイテムは「" + random.choice(items_list) + "」\n" + "今日の格言「" + random.choice(maxim_list) + "」")
    
@respond_to("私の生年月日、")
def respond(message):
    text = message.body['text']
    text = text.replace("私の生年月日、", "")
    wordlist = janomeAnalyzer(text)
    dotw = GregorianCalendar(wordlist)
    message.reply("貴方の生年月日" + text + "は、" + dotw + "曜日です。")

@respond_to('時間を教えて')
def react(message):
    dt_now = datetime.datetime.now()
    dt_now_str = dt_now.strftime('%Y/%m/%d %H:%M')
    message.reply("今の時間は、" + dt_now_str)
    
    
# スタンプの追加
@respond_to('かっこいい')
def react(message):
    message.reply('ありがとう！')
    message.react('hearts')
    message.react('+1')

# デフォルトの返答
@default_reply()
def default(message):
    # Slackの入力を取得
    text = message.body['text']

    # Slackで返答
    message.reply(text)