from twitterClass import Bot
import schedule
from time import sleep

tt = Bot()

def rotine_tweet():
    print('Ok') if tt.create_rotine_tt() else print('Fail')

def anwser_tweets():
    if not tt.answer_quote_tts():
        print('Fail')


schedule.every().day.at('12:00').do(rotine_tweet)
schedule.every().day.at('21:00').do(rotine_tweet)
schedule.every(2).minutes.do(anwser_tweets)

while True:
    schedule.run_pending()
    sleep(1)
    



