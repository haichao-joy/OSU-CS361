import requests
import nltk
from collections import Counter
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
import string

def main():
    input = "Most biographies and reference works state that West was born on June 8, 1977, in Atlanta, Georgia, although some sources give his birthplace as Douglasville, a small city west of Atlanta.[13][14] After his parents divorced when he was three years old, he moved with his mother to Chicago, Illinois.[15][16] His father, Ray West, is a former Black Panther and was one of the first black photojournalists at The Atlanta Journal-Constitution. Ray later became a Christian counselor,[16] and in 2006, opened the Good Water Store and Café in Lexington Park, Maryland, with startup capital from his son.[17][18] Wests mother, Dr. Donda C. West (neé Williams),[19] was a professor of English at Clark Atlanta University, and the Chair of the English Department at Chicago State University, before retiring to serve as his manager. West was raised in a middle-class environment, attending Polaris School for Individual Education[20] in suburban Oak Lawn, Illinois, after living in Chicago.[21] At the age of 10, West moved with his mother to Nanjing, China, where she was teaching at Nanjing University as part of an exchange program. According to his mother, West was the only foreigner in his class, but settled in well and quickly picked up the language, although he has since forgotten most of it.[22] When asked about his grades in high school, West replied, I got As and Bs. And Im not even frontin.[23]\
    West demonstrated an affinity for the arts at an early age; he began writing poetry when he was five years old.[24] His mother recalled that she first took notice of Wests passion for drawing and music when he was in the third grade.[25] West started rapping in the third grade and began making musical compositions in the seventh grade, eventually selling them to other artists.[26]"

    print(text_summarize(input))



def url_summarize(req_url, length = None):
    print(req_url)
    API_KEY = "1C6618077B"
    API_URL = "https://api.smmry.com"
    if length is None:
        length = 7
    PARAMS = {'SM_API_KEY': API_KEY, "SM_KEYWORD_COUNT":"5", "SM_LENGTH":length, 'SM_URL':req_url}
    req = requests.get(url=API_URL, params=PARAMS)
    json_resp = req.json()
    print(json_resp)
    try:
        text_content = json_resp['sm_api_content']
    except:
        text_content = "Text too short"
    try:
        keywords = json_resp['sm_api_keyword_array']
    except:
        keywords = "Text too short - no keywords"
    return text_content, keywords

def text_summarize(input, length = None):
    parser = PlaintextParser.from_string(input, Tokenizer("english"))
    stemmer = Stemmer("english")
    summary = Summarizer(stemmer)
    ret_string = ""
    if length is None:
        length = 7
    for sentence in summary(parser.document, length):
        ret_string += str(sentence)
        ret_string += "\n"

    stop_words = set(nltk.corpus.stopwords.words('english'))
    punctuations = string.punctuation
    for punc in punctuations:
        input = input.replace(punc, "")
    input = input.split()
    no_stopwords = []

    for word in input:
        if word not in stop_words:
            no_stopwords.append(word)

    common_words = Counter(no_stopwords)
    common_words = common_words.most_common(5)

    common_arr = []

    for tup in common_words:
        common_arr.append(tup[0])

    return (ret_string, common_arr)

if __name__ == "__main__":
    main()