from django import template

register = template.Library()
bad_text = "редиска"

@register.filter()
def censor(text):
    # with open('static/json/bad_words.json', 'r') as censor_file:
    #     bad_text = json.load(censor_file)
    for word in text.split():
        if word.lower() in bad_text:
            text = text.replace(
                word,
                f'{word[0]}{"*" * (len(word) - 1)}'
            )
    return text

