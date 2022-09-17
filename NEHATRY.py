import io
import random
import string # to process standard python strings
import warnings
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')

import nltk
from nltk.stem import WordNetLemmatizer
#nltk.download('popular', quiet=True)
#for downloading packages

# uncomment the following only the first time
#nltk.download('punkt') # first-time use only
#nltk.download('wordnet') # first-time use only


#Reading in the corpus
with open('chatbot.txt','r+', encoding='utf8', errors ='ignore') as fin:
    raw = fin.read().lower()

#TOkenisation
sent_tokens = nltk.sent_tokenize(raw)# converts to list of sentences 
word_tokens = nltk.word_tokenize(raw)# converts to list of words

# Preprocessing
lemmer = WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


# Keyword Matching
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]

GEN_INPUT = ["im lost", "im in a bad mood","today was a bad day"]
GEN_RESPONSE = ["what makes you feel that way", "what caused that","what happened"]

IDK_INPUT = ["idk", "i dont know","im not sure","dunno"]
IDK_RESPONSE = ["when did you start feeling this way","when did that start"]

ACTIVE_INPUT = ["something at school", "something at work", "i had a fight","i had an argument"]
ACTIVE_RESPONSE = ["how did that make you feel","how did you feel when that hapened","what effect did that have on you"]

FEEL_ANXIOUS_INPUT = ["i cant sleep","im anxious","i cant function","i experience stage fright","i feel anxious","i feel nervous","anxiety"]
FEEL_DEPRESSED_INPUT = ["ive lost my appetite","i cant function","ive lost interest","i feel worthless"]
CONTINUE_RESPONSE = ["anything else?","any other noticeable changes?","any other symptoms?"]

TIME_INPUT = ["few days ago","few days back","a week back","a week ago","couple of months ago","few months back"]
TIME_RESPONSE = ["Ok did you feel anything then?","any noticeable changes?","any symptoms?"]

ANX_COUNTER=0
DEP_COUNTER=0

def idk(sentence):
    """If user's input is vague, return an additional check response"""
    if sentence.lower() in IDK_INPUT:
        return random.choice(IDK_RESPONSE)

def active(sentence):
    """If user's input is an active response tothe question, return a continuation response"""
    if sentence.lower() in ACTIVE_INPUT:
        return random.choice(ACTIVE_RESPONSE)

def gen_response(sentence):
    """If user's input is a general statement, return a general response"""
    if sentence.lower() in GEN_INPUT:
        return random.choice(GEN_RESPONSE) 
    
def anxious(sentence):
    """If user's input is a general statement, return a general response"""
    if sentence.lower() in FEEL_ANXIOUS_INPUT:
        return random.choice(CONTINUE_RESPONSE)

def depression(sentence):
    """If user's input is a general statement, return a general response"""
    if sentence.lower() in FEEL_DEPRESSED_INPUT:
        return random.choice(CONTINUE_RESPONSE)

def greeting(sentence):
    """If user's input is a greeting, return a greeting response"""
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)


def time(sentence):
    """If user's input is a general statement, return a general response"""
    if sentence.lower() in TIME_INPUT:
        return random.choice(TIME_RESPONSE)



# Generating response

def response(user_response):
    try:
        robo_response=''
        sent_tokens.append(user_response)
        TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
        tfidf = TfidfVec.fit_transform(sent_tokens)
        vals = cosine_similarity(tfidf[-1], tfidf)
        idx=vals.argsort()[0][-2]
        flat = vals.flatten()
        flat.sort()
        req_tfidf = flat[-2]
        if(req_tfidf==0):
            robo_response=robo_response+"I am sorry! I don't understand you"
            return robo_response
        else:
            robo_response = robo_response+sent_tokens[idx]
            return robo_response
    except:
        
        robo_response=robo_response+""
        return robo_response
        


flag=True
print("WEvolve Bot: My name is WEvolve Bot. I'm here to help!")
while(flag==True):
    user_response = input()
    user_response=user_response.lower()
    if(user_response!='bye'):
        if(user_response=='thanks' or user_response=='thank you' ):
            flag=False
            print("WEvolve Bot: You are welcome..")
        else:
            if(greeting(user_response)!=None):
                print("WEvolve Bot: "+greeting(user_response))
            if(idk(user_response)!=None):
                print("WEvolve Bot: "+idk(user_response))
            if(gen_response(user_response)!=None):
                print("WEvolve Bot: "+gen_response(user_response))
            if(time(user_response)!=None):
                print("WEvolve Bot: "+time(user_response))    
            if(active(user_response)!=None):
                print("WEvolve Bot: "+active(user_response))
            if(anxious(user_response)!=None):
                ANX_COUNTER+=1
                if (ANX_COUNTER>3):
                    print("conversation shifts to anxiety help theme")
                    continue
                print("WEvolve Bot: "+anxious(user_response))
                
            if(depression(user_response)!=None):
                DEP_COUNTER+=1
                if(DEP_COUNTER>3):
                    print("conversation shifts to depression help theme")
                    continue
                print("WEvolve Bot: "+depression(user_response))
                

            else:
                print("WEvolve Bot: ",end="")
                print(response(user_response))
                sent_tokens.remove(user_response)
    else:
        flag=False
        print("WEvolve Bot: Bye! take care..")    