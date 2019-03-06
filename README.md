# The Lord of Ice and the Wardrobe

## Purpose
To construct a Markhov Chain twitter bot which generates the titles and descriptions of books in the Fantasy, Sci-Fi and Speculative Fiction genres using data from GoodReads.

### Procedure
In order to recreate the scraping process, go through the Generator Jupyter notebook. The genres I chose can be replaced as long as there is a corresponding page on goodreads (e.g https://www.goodreads.com/shelf/show/speculative). The notebook also walks through the process of coalescing the information into a corpus to build the vocabulary for the Markhov Chain. 

### Twitter Bot
To modify the Twitter Bot add a file named keys.txt with the necessary access tokens listed. Run ScriptWhichMustNotBeNamed.py and it will grab those keys and use the functions in raise_corpus.py to automatically generate a 6 word title and a description up to 60 words (you can change these parameters in the script). It then tweets out these results and if it would constitute more than a single tweet then the script will break up the text in order to reply to its first message and start a thread.

### Sources
More information on the motivation behind and sources used for this project can be found at https://medium.com/@dan.j.izquierdo/seeds-of-chaos-story-prompts-using-markhov-chains-c44e9e124bba
