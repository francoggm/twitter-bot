import openai, random
from credentials import gpt_key

class Gpt3():
    def __init__(self):
        self.phrases = [
            'say something cool\n',
            'tells about today news\n',
            'how is the stock market today?',
            'tell a conspiracy theory\n',
            'talks about python\n',
            'talks about javascript\n',
            'what is the best movie?',
            'indicate a movie\n',
            'indicate a serie\n',
            'how is it to love?',
            'talks about tech careers\n',
            'talks about the war\n',
            'how is the weather today?',
            'tell a joke\n',
            'talks about science\n',
            'talks about black holes\n',
            'talks about quantic cryptography\n',
            'how is it to have a girlfriend\n',
            'what is the best country to live?',
            'talks about james webb in nasa\n',
            'talks about quantum computer\n',
            'says a nice hashtag to twitter\n',
            'make a tweet\n',
            'make a angry tweet\n',
            'make a happy tweet\n',
            'make a sarcastic tweet\n',
            'popular books\n',
            'talks about stolen data on social media\n',
            'talks about tesla\n',
            'talks about spacex\n',
            'talks about outer space\n',
            'talks about white roles\n',
            'talks about nuclear bomb\n',
            'talks about frameworks\n',
            'talks about data science\n',
            'says something sarcastic\n',
            'says something good'
        ]
        self.connect()

    def get_key(self):
        return gpt_key

    def connect(self):
        openai.api_key = self.get_key()

    def specific_text(self, text):
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt= 'uma pergunta: '+text,
            temperature=0.7,
            max_tokens=64
        )
        data = response['choices'][0]['text']
        return data

    def random_text(self):
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt= random.choice(self.phrases),
            temperature=0.7,
            max_tokens=64
        )
        data = response['choices'][0]['text']
        return data

