from prompt_toolkit.validation import Validator, ValidationError

class NumberValidator(Validator):

    def validate(self, document):
        valid = True