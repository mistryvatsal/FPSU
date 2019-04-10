import data_calculation
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd

df=data_calculation.save_data()
#df = pd.read_csv(r"new.csv")
comment_words = ' '
stopwords = set(STOPWORDS)


for val in df:
    val = str(val)
    tokens = val.split()

    for i in range(len(tokens)):
        tokens[i] = tokens[i].lower()

    for words in tokens:
      comment_words = comment_words + words + ' '
      print(comment_words)


wordcloud = WordCloud(width = 800, height = 800,
                background_color ='white',
                stopwords = stopwords,
                min_font_size = 10).generate(comment_words)


plt.figure(figsize = (6, 6), facecolor = None,frameon=False)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)
plt.savefig('myfig.png')