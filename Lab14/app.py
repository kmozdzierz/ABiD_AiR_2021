from textblob import TextBlob
import numpy as np

def hello(name):
    output = f'Hello {name}'
    return output


def extract_sentiment(text):
    text = TextBlob(text)

    return text.sentiment.polarity

def text_contain_word(word: str, text: str):
    return word in text


 
def Frobenius_mtx(coeff: np.ndarray):

    if not isinstance(coeff, np.ndarray):
        return None
    else:

        n = coeff.shape[0]- 1  
        frob_mtx = np.zeros(shape=(n, n))
        
        for i in range(n - 1):
            frob_mtx[i][i+1] = 1
            frob_mtx[-1] = -1*coeff[::-1][:-1]

        return frob_mtx