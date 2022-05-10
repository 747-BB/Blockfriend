import ctypes
import os
import platform
import sys
from enum import Enum
from typing import Callable, Dict, List, Optional, Tuple, Union
from colorama import init
from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.styles import Style
from PyInquirer import Separator
from PyInquirer.prompt import prompt
init()

class WindowAlign(Enum):
    '''Patch WindowAlign lol.'''
    LEFT = 'LEFT'
    RIGHT = 'LEFT'
    CENTER = 'LEFT'

from PyInquirer.prompts import checkbox
checkbox.WindowAlign = WindowAlign
HEADER_COLOR = 'ansibrightmagenta'
DEFAULT_HEADER = [
    '\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x95\x97 \xe2\x96\x88\xe2\x96\x88\xe2\x95\x97      \xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x95\x97  \xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x95\x97\xe2\x96\x88\xe2\x96\x88\xe2\x95\x97  \xe2\x96\x88\xe2\x96\x88\xe2\x95\x97\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x95\x97\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x95\x97 \xe2\x96\x88\xe2\x96\x88\xe2\x95\x97\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x95\x97\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x95\x97   \xe2\x96\x88\xe2\x96\x88\xe2\x95\x97\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x95\x97 ',
    '\xe2\x96\x88\xe2\x96\x88\xe2\x95\x94\xe2\x95\x90\xe2\x95\x90\xe2\x96\x88\xe2\x96\x88\xe2\x95\x97\xe2\x96\x88\xe2\x96\x88\xe2\x95\x91     \xe2\x96\x88\xe2\x96\x88\xe2\x95\x94\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x96\x88\xe2\x96\x88\xe2\x95\x97\xe2\x96\x88\xe2\x96\x88\xe2\x95\x94\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x9d\xe2\x96\x88\xe2\x96\x88\xe2\x95\x91 \xe2\x96\x88\xe2\x96\x88\xe2\x95\x94\xe2\x95\x9d\xe2\x96\x88\xe2\x96\x88\xe2\x95\x94\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x9d\xe2\x96\x88\xe2\x96\x88\xe2\x95\x94\xe2\x95\x90\xe2\x95\x90\xe2\x96\x88\xe2\x96\x88\xe2\x95\x97\xe2\x96\x88\xe2\x96\x88\xe2\x95\x91\xe2\x96\x88\xe2\x96\x88\xe2\x95\x94\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x9d\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x95\x97  \xe2\x96\x88\xe2\x96\x88\xe2\x95\x91\xe2\x96\x88\xe2\x96\x88\xe2\x95\x94\xe2\x95\x90\xe2\x95\x90\xe2\x96\x88\xe2\x96\x88\xe2\x95\x97',
    '\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x95\x94\xe2\x95\x9d\xe2\x96\x88\xe2\x96\x88\xe2\x95\x91     \xe2\x96\x88\xe2\x96\x88\xe2\x95\x91   \xe2\x96\x88\xe2\x96\x88\xe2\x95\x91\xe2\x96\x88\xe2\x96\x88\xe2\x95\x91     \xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x95\x94\xe2\x95\x9d \xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x95\x97  \xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x95\x94\xe2\x95\x9d\xe2\x96\x88\xe2\x96\x88\xe2\x95\x91\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x95\x97  \xe2\x96\x88\xe2\x96\x88\xe2\x95\x94\xe2\x96\x88\xe2\x96\x88\xe2\x95\x97 \xe2\x96\x88\xe2\x96\x88\xe2\x95\x91\xe2\x96\x88\xe2\x96\x88\xe2\x95\x91  \xe2\x96\x88\xe2\x96\x88\xe2\x95\x91',
    '\xe2\x96\x88\xe2\x96\x88\xe2\x95\x94\xe2\x95\x90\xe2\x95\x90\xe2\x96\x88\xe2\x96\x88\xe2\x95\x97\xe2\x96\x88\xe2\x96\x88\xe2\x95\x91     \xe2\x96\x88\xe2\x96\x88\xe2\x95\x91   \xe2\x96\x88\xe2\x96\x88\xe2\x95\x91\xe2\x96\x88\xe2\x96\x88\xe2\x95\x91     \xe2\x96\x88\xe2\x96\x88\xe2\x95\x94\xe2\x95\x90\xe2\x96\x88\xe2\x96\x88\xe2\x95\x97 \xe2\x96\x88\xe2\x96\x88\xe2\x95\x94\xe2\x95\x90\xe2\x95\x90\xe2\x95\x9d  \xe2\x96\x88\xe2\x96\x88\xe2\x95\x94\xe2\x95\x90\xe2\x95\x90\xe2\x96\x88\xe2\x96\x88\xe2\x95\x97\xe2\x96\x88\xe2\x96\x88\xe2\x95\x91\xe2\x96\x88\xe2\x96\x88\xe2\x95\x94\xe2\x95\x90\xe2\x95\x90\xe2\x95\x9d  \xe2\x96\x88\xe2\x96\x88\xe2\x95\x91\xe2\x95\x9a\xe2\x96\x88\xe2\x96\x88\xe2\x95\x97\xe2\x96\x88\xe2\x96\x88\xe2\x95\x91\xe2\x96\x88\xe2\x96\x88\xe2\x95\x91  \xe2\x96\x88\xe2\x96\x88\xe2\x95\x91',
    '\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x95\x94\xe2\x95\x9d\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x95\x97\xe2\x95\x9a\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x95\x94\xe2\x95\x9d\xe2\x95\x9a\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x95\x97\xe2\x96\x88\xe2\x96\x88\xe2\x95\x91  \xe2\x96\x88\xe2\x96\x88\xe2\x95\x97\xe2\x96\x88\xe2\x96\x88\xe2\x95\x91     \xe2\x96\x88\xe2\x96\x88\xe2\x95\x91  \xe2\x96\x88\xe2\x96\x88\xe2\x95\x91\xe2\x96\x88\xe2\x96\x88\xe2\x95\x91\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x95\x97\xe2\x96\x88\xe2\x96\x88\xe2\x95\x91 \xe2\x95\x9a\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x95\x91\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x95\x94\xe2\x95\x9d',
    '\xe2\x95\x9a\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x9d \xe2\x95\x9a\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x9d \xe2\x95\x9a\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x9d  \xe2\x95\x9a\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x9d\xe2\x95\x9a\xe2\x95\x90\xe2\x95\x9d  \xe2\x95\x9a\xe2\x95\x90\xe2\x95\x9d\xe2\x95\x9a\xe2\x95\x90\xe2\x95\x9d     \xe2\x95\x9a\xe2\x95\x90\xe2\x95\x9d  \xe2\x95\x9a\xe2\x95\x90\xe2\x95\x9d\xe2\x95\x9a\xe2\x95\x90\xe2\x95\x9d\xe2\x95\x9a\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x9d\xe2\x95\x9a\xe2\x95\x90\xe2\x95\x9d  \xe2\x95\x9a\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x9d\xe2\x95\x9a\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x9d ']
stylesheet = Style.from_dict({
    'separator': 'ansired',
    'questionmark': 'ansired',
    'selected': 'fg:ansibrightred noreverse',
    'pointer': 'ansired',
    'instruction': '',
    'answer': 'ansibrightred',
    'question': 'bold',
    'header': HEADER_COLOR,
    'validation-toolbar': 'bg:ansired ansiwhite' })

def clear_screen():
    '''Clears the screen.'''
    system = platform.system()
    if system == 'Windows':
        command = 'cls'
    else:
        command = 'clear'
    print('\x1b[2J')
    os.system(command)


def update_title(title):
    '''Updates title of cmd window.'''
    system = platform.system()
    if system == 'Windows' and getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        ctypes.windll.kernel32.SetConsoleTitleW(title)


class Form:
    '''Represents a `Form` for a `Menu`.'''

    def __init__(self = None, questions = None):
        '''Initializes a Form object.

        questions: List of question-dictionaries:
            {
                "prompt": "Question for input",
                "prompt_type": "",
                "key": "What to save input as",
                "choices": [] # (OPTIONAL)
            }

        '''
        self.questions = questions
        self.answers = { }


    def history(self = None):
        '''Returns the answer history for this Form.'''
        history = { }
        return history

    history = None(history)

    def format_choices(self = None, choices = None):
        '''Properly formats the choices into PyInquirer format.'''
        if not isinstance(choices, list):
            return []
        formatted = None
        if hasattr(choice, 'get') and callable(choice.get):
            data = {
                'name': choice.get('name'),
                'value': choice.get('value') }
            formatted.append(data)
        formatted.append({
            'name': choice })
        return formatted


    def choice_callable(self = None, func = None, prev_answers = None):
        '''Bandaid patch for callable `choices`.'''

        def patch(answers = None):
            answers.update(prev_answers)
            choices = func(answers)
            return self.format_choices(choices)

        return patch


    def parse_questions(self = None, prev_answers = None):
        '''Parses the questions to a PyInquirer compatible format.'''
        res = []
        for question in self.questions:
            payload = {
                'type': question.get('prompt_type'),
                'name': question.get('key'),
                'message': question.get('prompt') }
            choices = question.get('choices')
            formatted = self.format_choices(choices)
            payload['choices'] = formatted
        if callable(choices):
            payload['choices'] = self.choice_callable(choices, prev_answers)
        when = question.get('when')
        if when:
            payload['when'] = when
        validator = question.get('validate')
        if validator:
            payload['validate'] = validator
        res.append(payload)
        return res


    def execute(self = None, prev_answers = None):
        '''Asks all questions and returns the formatted answers.'''
        questions = self.parse_questions(prev_answers)



class Option:
    '''Represents an `Option` for a `Menu`.'''

    def __init__(self = None, name = None, menu = None, form = (None, None)):
        '''Initializes an Option object.

        name: The name of the option, displayed on the CLI.
        menu: The `Menu` that follows this option.
        form: The `Form` that follows this option.

        If both Menu and Form are specified, the Form will be executed first,
        before proceeding to the Menu.
        '''
        self.name = name
        self.menu = menu
        self.form = form
        if not menu and isinstance(menu, Menu):
            raise ValueError(f'''Expected `Menu`, got: `{type(menu)}`''')
        if not None and isinstance(form, Form):
            raise ValueError(f'''Expected `Form`, got: `{type(form)}`''')



class Menu:

    def __init__(self, prompt, prompt_type, key = None, options = None, header = None, has_back = (None, DEFAULT_HEADER, True, None), validation = {
        'prompt': str,
        'prompt_type': str,
        'key': str,
        'options': Optional[List[Option]],
        'header': Union[(str, list)],
        'has_back': bool,
        'validation': Optional[Callable[(..., bool)]] }):
        '''Initializer for Menu objects.

        prompt: The prompt message when this Menu asks for input.
        prompt_type: The PyInquirer prompt type.
        key: The dict key to store the Menu answer as: {self.key: value}.
        options: A list of Option objects to be displayed.
        header: The message to be displayed at the top of the menu.
        has_back: If this Menu has the "Go Back" option.
        validation: A function to validate the option selected.
            Returns is_valid, error_message: Tuple[bool, Optional[str]]
        '''
        self.prompt = prompt
        self.prompt_type = prompt_type
        self.key = key
        self.options = []
        self.header = header
        self.has_back = has_back
        self.validation = validation
        self.answers = { }
        self.history = { }
        if not options:
            pass
        options = []
        self.active_menu = self
        self.prev_menu = None
        self.error_message = ''


    def set_current_error(self = None, error = None):
        '''Sets the error message for the Menu currently in view.'''
        if error is None:
            self.active_menu.error_message = None
        elif not error and self.active_menu.error_message:
            self.active_menu.error_message = error


    def print_header(self):
        """Prints the current Menu's header."""
        if isinstance(self.active_menu.header, str):
            fragments = [
                self.active_menu.header]
        elif isinstance(self.active_menu.header, list):
            fragments = self.active_menu.header
        else:
            return None
        tokens = None
        print('\n')
        if self.active_menu.error_message:
            msg = self.active_menu.error_message
            token = ('class:validation-toolbar', '\n' + msg)
            tokens.append(token)
        print_formatted_text(FormattedText(tokens), stylesheet, **('style',))
        print('\n')


    def refresh_screen(self):
        '''Refreshes the screen.'''
        clear_screen()
        self.print_header()
        if self.history:
            for question, value in self.history.items():
                answer = list(value.values())[0]
                answer = answer[0]
            answer = f'''done ({len(answer)} selections)'''
            tokens = FormattedText([
                ('class:questionmark', '? '),
                ('class:question', f'''{question} '''),
                ('class:answer', f'''{answer}''')])
            print_formatted_text(tokens, stylesheet, **('style',))


    def validate_choice(self = None, choice = None):
        '''Validates the option with the validation function of this Menu.'''
        if not self.active_menu.validation:
            (valid, error_message) = (True, None)
        else:
            (valid, error_message) = self.active_menu.validation(choice)
        if not valid:
            self.set_current_error(error_message)
        else:
            self.set_current_error(None)
        return valid


    def get_choice(self = None):
        '''Gets a single choice from the user.'''
        options = (lambda .0: [ o.name for o in .0 ])(self.active_menu.options)
        if self.active_menu.has_back:
            options.append('Go Back')
        questions = [
            {
                'type': self.active_menu.prompt_type,
                'name': self.active_menu.key,
                'message': self.active_menu.prompt,
                'choices': options }]
        answers = prompt(questions, stylesheet, **('style',))
        choice = list(answers.values())[0]
        idx = options.index(choice)
        return (answers, idx)


    #def set_current_chain(self = None, name = None):