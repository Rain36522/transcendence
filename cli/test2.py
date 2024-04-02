from prompt_toolkit import prompt
from prompt_toolkit.key_binding import KeyBindings
import asyncio

# Création des liaisons de touches
kb = KeyBindings()

def create_key_handler(variable):
    def key_handler(event):
        print(f'Variable: {variable}')
        print('Flèche pressée')
    return key_handler

# @kb.add('up')
# def up(event):
#     pass

# @kb.add('down')
# def down(event):
#     pass

# Assigner les fonctions créées avec la variable spécifique
variable = 'example_variable'
kb.add('up')(create_key_handler(variable))
kb.add('down')(create_key_handler(variable))

# Boucle principale
while True:
    user_input = prompt('', key_bindings=kb)
    if user_input == 'q':
        break
