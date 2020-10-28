import codecs
import re
from bs4 import BeautifulSoup

f = codecs.open("eastenders_split_html.html", 'r')
lines = f.read()
soup = BeautifulSoup(lines, 'html.parser')

mixed_output = []


def contains_lowercase(input_string):
    for c in input_string:
        if c.islower():
            return True
    return False


def remove_square_bracket_text(input_string):
    return re.sub("[\(\[].*?[\)\]]", "", input_string)


def remove_pipes(input_string):
    return input_string.replace('|', '')


def remove_brackets(input_string):
    return input_string.replace('[', '').replace(']', '')


for line in soup.findAll('tr'):
    for l in line.findAll('td'):
        if l.find('sup'):
            l.find('sup').extract()
        mixed_output.append(l.getText()+'|')

mixed_output_with_lowercase_only = []

for line in mixed_output:
    if contains_lowercase(line):
        mixed_output_with_lowercase_only.append(line)

likely_speech = []

for line in mixed_output_with_lowercase_only:
    if ':' in line:
        likely_speech.append(line.split(":", 1)[1])

cleaned_text = []

for line in likely_speech:
    cleaned_text.append(remove_brackets(remove_pipes(
        remove_square_bracket_text(line)).strip()))

final_filter = []

for line in cleaned_text:
    if contains_lowercase(line):
        final_filter.append(line)

# import ipdb; ipdb.set_trace()

with open('script_sentences.txt', 'w') as f:
    for item in final_filter:
        f.write("%s\n" % item)
