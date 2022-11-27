# English-Dictionary-Database

a CSV of every english word, part of speech, and definition. as well as a web scraping script that generates that data for you

## REQUIREMENTS FOR SCRIPT

```bash
pip install -r requirements.txt
```

## Usaage
```bash
DEV=true python dictionaryScript.py > dev.csv
```

There is a series of web pages hosted by the Australian National University with beautifully formatted HTML containing 176,047 words of the english dictionary. There is a page for each letter of the alphabet. The script will make a request to all the pages based on a string containing all the letters of the alphabet. If you want to modify what pages get requested, modify the string. The script will then run a loop for each entry on the page, parsing out the word, pos (part of speech) and definition of the entry. In this loop you can do whatever it is you need with this data. Example add to a sql database. Or save to some sort of file.


there is a html example included if you want to see what is being parsed (to understantd it)
