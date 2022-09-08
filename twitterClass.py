import requests
from requests_oauthlib import OAuth1
from gpt3Class import Gpt3
from credentials import consumerKey, consumerSecret, acessSecret, acessToken


class Bot():
    def __init__(self):
        self.gpt3 = Gpt3()
        self.createds_tt = []
        self.reply_tt = []
        self.url = 'https://api.twitter.com'
        self.consumerKey = consumerKey
        self.consumerSecret = consumerSecret
        self.acessToken = acessToken
        self.acessSecret = acessSecret
        self.auth = self.oauth1()
        m_id = self.get_user_by_username('wilson_human')
        self.my_id = m_id[0]['id'] if not m_id is False else print('Exception get own id')

    def get_keys(self):
        return

    def get_bearer_token(self):
        command = '/oauth2/token'
        params = {'grant_type':'client_credentials'}
        response = requests.request('POST',self.url+command,params=params,auth=(self.consumerKey,self.consumerSecret))
        data = response.json()
        return data['access_token']

    def get_user_by_username(self, username):
        command = '/2/users/by?usernames=' + ''.join(username)
        method = 'GET'
        data = self.make_request(method=method,command=command, bearer=True)
        if not data:
            return False
        elif not 'data' in data:
            print('Exception get user by username')
            return False
        else:
            return data['data']
    
    def get_user_by_id(self, id):
        command = '/2/users/' + ''.join(str(id))
        method = 'GET'
        data = self.make_request(method=method,command=command,bearer=True)
        if not data:
            return False
        elif not 'data' in data:
            print('Exception get user by id')
            return False
        else:
            return data['data']
    
    def make_request(self, method, command, json=None, auth=None, headers=None, bearer=False, params=None):
        if bearer and headers is not None:
            headers["Authorization"] = "Bearer {}".format(self.get_bearer_token())
        elif bearer and headers is None:
            headers = {}
            headers["Authorization"] = "Bearer {}".format(self.get_bearer_token())
        response = requests.request(method=method, url=self.url+command, auth=auth, json=json,headers=headers,params=params)
        data = response.json() 
        if response.status_code == 200 or 201:  
                return data
        print('Exception in request', data)
        return False

    def oauth1(self):
        return OAuth1(self.consumerKey, self.consumerSecret, self.acessToken, self.acessSecret)

    def get_tweet_by_id(self, id):
        command = '/2/tweets/' + ''.join(str(id))
        method = 'GET'
        data = self.make_request(method=method, command=command, auth=self.auth)
        if not data:
            return False
        elif not 'data' in data:
            print('Exception get tweet by id')
            return False
        else:
            return data['data']
    
    def get_tweets_by_ids(self, ids):
        command = '/2/tweets?ids=' + ','.join(id for id in ids)
        method = 'GET'
        data = self.make_request(method=method, command=command, auth=self.auth)
        if not data:
            return False
        elif not 'data' in data:
            print('Exception get tweet by id')
            return False
        else:
            return data['data']
        
    def get_tweet_by_query(self, query, max_results=10):
        if max_results < 10: max_results = 10
        if max_results > 100: max_results = 100
        querys = ' '.join(query)
        command = '/2/tweets/search/recent'
        method = 'GET'
        params = {'query': querys, 'max_results':max_results}
        data = self.make_request(method=method, command = command,params=params, bearer=True)
        if not data:
            return False
        elif not 'data' in data:
            print('Exception get tweet by querys')
            return False
        else:
            return data['data']

    def get_mentions_by_userid(self, id=1, max_results = 5, himself = False):
        if max_results < 5: max_results = 5
        if max_results > 100: max_results = 100
        if himself: id = self.my_id
        command = '/2/users/{}/mentions'.format(str(id))
        method = 'GET'
        params = {"max_results":max_results}
        data = self.make_request(method=method,command=command,params=params,bearer=True)
        if not data:
            return False
        elif not 'data' in data:
            print('Exception get quote tweets')
            return False
        else:
            return data['data']

    def create_tweet(self, text=None, for_super_followers_only=None, reply_settings=None, in_reply_to_tweet_id=None):
        command = '/2/tweets'
        method =  'POST'
        params = {}
        if not for_super_followers_only is None:    
            params['for_super_followers_only'] = for_super_followers_only
        if not reply_settings is None:    
            params['reply_settings'] = reply_settings
        if not text is None:    
            params['text'] = text
        if not in_reply_to_tweet_id is None:
            params['reply'] = {'in_reply_to_tweet_id':str(in_reply_to_tweet_id)}
        data = self.make_request(method=method,command=command,json=params,auth=self.auth)
        if not data: 
            return False
        elif not 'data' in data:
            print('Exception in create_tweet', data)
            return False
        else:
            self.createds_tt += [{'id':data['data']['id'],'text':data['data']['text']}]
            return True

    def user_mention_timeline_byid(self, id):
        command = '/2/users/{}/mentions'.format(str(id))
        method = 'GET'
        params = {}
        data = self.make_request(method=method,command=command,json=params,auth=self.auth,bearer=True)
        if not data: 
            return False
        elif not 'data' in data:
            print('Exception in get mentions timeline user', data)
            return False
        else:
            return data

    def get_quote_tweets(self, id):
        command = '/2/tweets/{}/quote_tweets'.format(str(id))
        method = 'GET'
        params = {}
        data = self.make_request(method=method,command=command,json=params,auth=self.auth,bearer=True)
        if not data: 
            return False
        elif not 'data' in data:
            print('Exception in get quote tweets user', data)
            return False
        else:
            return data

    def list_tweets_lockup_byid(self, id):
        command = 'https://api.twitter.com/2/lists/{}/tweets'.format(str(id))
        method = 'GET'
        params = {}
        data = self.make_request(method=method,command=command,json=params,auth=self.auth,bearer=False)
        if not data: 
            return False
        elif not 'data' in data:
            print('Exception in list_tweets_lockup_byid', data)
            return False
        else:
            return data

    def create_rotine_tt(self):
        if self.create_tweet(text=self.gpt3.random_text()):
            return True
        return False
    
    def answer_quote_tts(self):
        mentions = self.get_mentions_by_userid(self.my_id)
        if mentions is not False:
            for mention in mentions:
                if not any(id['id'] == mention['id'] for id in self.reply_tt):
                    text = mention['text']
                    id = mention['id']
                    text = text.replace('@wilson_human','')
                    self.create_tweet(text=self.gpt3.specific_text(text),in_reply_to_tweet_id=str(id))
                    self.reply_tt += [{'id':id,'text':text}]
                else:
                    pass
        else:
            return False
                      
    

if __name__ == '__main__':
    tt = Bot()
    tt.list_tweets_lockup_byid(tt.d_user_id)
    tt.get_mentions_by_userid(tt.my_id)
    

   

    

