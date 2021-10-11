import wikipedia
import urllib
import wikipediaapi

wiki_wiki = wikipediaapi.Wikipedia('en')

page_py = wiki_wiki.page("Berbérati")
print(page_py.canonicalurl)

s = wikipedia.summary("West_Loch_Estate,_Hawaii")
print(s.url)
print(s)