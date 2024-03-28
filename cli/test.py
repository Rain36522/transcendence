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
