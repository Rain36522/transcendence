# from prompt_toolkit.shortcuts import prompt
# from prompt_toolkit.styles import Style

# style = Style.from_dict({
#     # User input (default text).
#     '':          '#ff0066',

#     # Prompt.
#     'username': '#884444',
#     'at':       '#00aa00',
#     'colon':    '#0000aa',
#     'pound':    '#00aa00',
#     'host':     '#00ffff bg:#444400',
#     'path':     'ansicyan underline',
# })

# message = [
#     ('class:username', 'john'),
#     ('class:at',       '@'),
#     ('class:host',     'localhost'),
#     ('class:colon',    ':'),
#     ('class:path',     '/user/john'),
#     ('class:pound',    '# '),
# ]

# text = prompt(message, style=style)

# from prompt_toolkit import prompt
# from prompt_toolkit.styles import Style

# def bottom_toolbar():
#     return [('class:bottom-toolbar', ' This is a toolbar. ')]

# style = Style.from_dict({
#     'bottom-toolbar': '#ffffff bg:#333333',
# })

# text = prompt('> ', bottom_toolbar=bottom_toolbar, style=style)
# print('You said: %s' % text)

# import asyncio

# from prompt_toolkit.input import create_input
# from prompt_toolkit.keys import Keys


# async def main() -> None:
#     done = asyncio.Event()
#     input = create_input()

#     def keys_ready():
#         for key_press in input.read_keys():
#             print(key_press)

#             if key_press.key == Keys.ControlC:
#                 done.set()

#     with input.raw_mode():
#         with input.attach(keys_ready):
#             await done.wait()


# if __name__ == "__main__":
#     asyncio.run(main())

# from prompt_toolkit.formatted_text import HTML
# from prompt_toolkit.shortcuts import message_dialog
# from prompt_toolkit.styles import Style

# example_style = Style.from_dict({
#     'dialog':             'bg:#88ff88',
#     'dialog frame.label': 'bg:#ffffff #000000',
#     'dialog.body':        'bg:#000000 #00ff00',
#     'dialog shadow':      'bg:#00aa00',
# })

# message_dialog(
#     title=HTML('<style bg="blue" fg="white">Styled</style> '
#                '<style fg="ansired">dialog</style> window'),
#     text='Do you want to continue?\nPress ENTER to quit.',
#     style=example_style).run()


# from prompt_toolkit.shortcuts import radiolist_dialog

# result = radiolist_dialog(
#     title="RadioList dialog",
#     text="Which breakfast would you like ?",
#     values=[
#         ("breakfast1", "Eggs and beacon"),
#         ("breakfast2", "French breakfast"),
#         ("breakfast3", "Equestrian breakfast")
#     ]
# ).run()

# import requests
# from bs4 import BeautifulSoup

# # URL de la page de connexion
# url = 'https://127.0.0.1/register/'

# # Envoi d'une requête GET pour récupérer la page de connexion et le token CSRF
# response = requests.get(url, verify=False)

# # Données du formulaire de connexion, incluant le token CSRF
# myobj = {'username': 'test', 'email': 'pudry@42.student.ch', 'password1': '3azah9avuw#9TM!chHu#^$vXppPps', 'password2': '3azah9avuw#9TM!chHu#^$vXppPps'}
# response = requests.get(url, verify=False)


# csrf_token = response.cookies.get('csrftoken')
# print("Token", csrf_token)

# headers = {'Referer': url, 'X-CSRFToken': csrf_token}  # Ajout de l'en-tête Referer
# cookies = {'csrftoken': csrf_token}  # Ajout du cookie CSRF
# # Envoi de la requête POST avec le  dtoken CSRF inclus dans les données du formulaire
# response = requests.post(url, data=myobj, headers=response.headers, cookies=response.cookies, verify=False)


# # Affichage de la réponse
# print(response.text)

# # # Affichage des cookies de la réponse
# print("Cookies : ", response.cookies)


import requests
from color import *
from time import sleep

# URL de la page de connexion
url = 'https://127.0.0.1/register/'
url2 = 'https://127.0.0.1/api/signup/'

# Envoi d'une requête GET pour récupérer la page de connexion et le token CSRF
response = requests.get(url, verify=False)

# Récupération du token CSRF depuis les cookies de la réponse
csrf_token = response.cookies.get('csrftoken')
print(YELLOW, response.text, RESET)


# print(GREEN, response.text)
tokenStart = response.text.find("<input type=\"hidden\" name=\"csrfmiddlewaretoken\" value=\"") + 55
tokenStop = response.text.find("\">", tokenStart)
csrfmiddlewaretoken = response.text[tokenStart:tokenStop]
print(ORANGE, csrfmiddlewaretoken, RESET)

# En-têtes et cookies nécessaires pour la requête POST
headers = {'Referer': url, 'X-CSRFToken': csrf_token}
cookies = {'csrftoken': csrf_token}

myobj = {
    'username': 'test',
    'email': 'pudry@42.student.ch',
    'password': '3azah9avuw#9TM!chHu#^$vXppPps',
    'csrfmiddlewaretoken': csrfmiddlewaretoken
}

# Envoi de la requête POST avec le token CSRF inclus dans les données du formulaire

response = requests.post(url2, data=myobj, headers=headers, cookies=cookies, verify=False)

# Affichage de la réponse
print(MAGENTA, response.text, RESET)

# Affichage des cookies de la réponse
print("Cookies:", response.cookies)


# name="csrfmiddlewaretoken"
# value="zGn8Jg4zlk9jw9uwxGPq0DgTkfT2IMZSzEDBZNggyIXUqtcqkvOKfNKmYgQzWFDz"