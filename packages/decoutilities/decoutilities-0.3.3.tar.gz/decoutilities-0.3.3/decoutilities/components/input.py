import msvcrt
import os
from ..textUtils import textUtils
import re
import json

class Input():
    def __init__(self, name, value, rules, placeholder):
        self.name = name
        self.value = value
        self.rules = rules
        self.placeholder = placeholder

    def __action(self, action, value=None):
        match action:
            case 'write':
                self.value += value
            case 'delete':
                self.value = self.value[:-1]
            case 'clear':
                self.value = ''
            case 'submit':
                return self.value

    def display(self):
        last_error = ''
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console
            suffix = ''
            if 'REQUIRED' in self.rules.split('|'):
                suffix = textUtils.format("{red}*")
            print(textUtils.format("{bold}" + self.name)+suffix)
            spacing = 30
            if self.value and len(self.value) > 28:
                spacing = len(self.value) + 2

            print("┌" + "─" * spacing + "┐")
            if self.value:
                if 'PASSWORD' in self.rules.split('|'):
                    value_to_display = '*' * len(self.value)
                else:
                    value_to_display = self.value
            else:
                value_to_display = textUtils.format("{dark_gray}" + self.placeholder)
            print("│ " + value_to_display + " " * (28 - len(self.value or self.placeholder)) + " │")
            print("└" + "─" * spacing + "┘")
            if last_error:
                print(textUtils.format("{red}ERROR: " + last_error))
            key = msvcrt.getch()
            if key == b'\r':  # Enter key
                status = self.__validate(self.value)
                if  status[0]:
                    return self.__action('submit')
                else:
                    last_error = status[1]
            elif key == b'\x08':  # Backspace key
                self.__action('delete')
            else:
                self.__action('write', key.decode("utf-8"))
    
    def __validate(self, value):
        rulelist = self.rules.split('|')
        for rule in rulelist:
            if rule == 'EMAIL':
                if '@' not in value:
                    return [False, 'Must be a valid email address']
            if rule == 'NUMBER':
                if not value.isnumeric():
                    return [False, 'Must be a number']
            if rule == 'STRING':
                if not value.isalpha():
                    return [False, 'Must be a string']
            if rule.startswith('MIN:'):
                if len(value) < int(rule.split(':')[1]):
                    return [False, f'Must be at least {rule.split(":")[1]} characters long']
            if rule.startswith('MAX:'):
                if len(value) > int(rule.split(':')[1]):
                    return [False, f'Must be at most {rule.split(":")[1]} characters long']
            if rule.startswith('LENGTH:'):
                if len(value) != int(rule.split(':')[1]):
                    return [False, f'Must be exactly {rule.split(":")[1]} characters long']
            if rule.startswith('REGEX:'):
                if not re.match(rule.split(':')[1], value):
                    return [False, 'Must match the regex pattern']
            if rule.startswith('CONTAINS:'):
                if rule.split(':')[1] not in value:
                    return [False, 'Must contain the specified value']
            if rule.startswith('NOT_CONTAINS:'):
                if rule.split(':')[1] in value:
                    return [False, 'Must not contain the specified value']
            if rule.startswith('IN:'):
                if value not in rule.split(':')[1].split(','):
                    return [False, 'Must be one of the specified values']
            if rule.startswith('NOT_IN:'):
                if value in rule.split(':')[1].split(','):
                    return [False, 'Must not be one of the specified values']
            if rule.startswith('EQUALS:'):
                if value != rule.split(':')[1]:
                    return [False, 'Must be equal to the specified value']
            if rule.startswith('NOT_EQUALS:'):
                if value == rule.split(':')[1]:
                    return [False, 'Must not be equal to the specified value']
            if rule.startswith('HIGHER:'):
                if float(value) < int(rule.split(':')[1]):
                    return [False, f'Must be higher than {rule.split(":")[1]}']
            if rule.startswith('LOWER:'):
                if float(value) > int(rule.split(':')[1]):
                    return [False, f'Must be lower than {rule.split(":")[1]}']
            if rule.startswith('HIGHER_OR_EQUAL:'):
                if float(value) <= int(rule.split(':')[1]):
                    return [False, f'Must be higher or equal to {rule.split(":")[1]}']
            if rule.startswith('LOWER_OR_EQUAL:'):
                if float(value) >= int(rule.split(':')[1]):
                    return [False, f'Must be lower or equal to {rule.split(":")[1]}']
            if rule == 'REQUIRED':
                if value is None or value == '':
                    return [False, 'This field is required']
            if rule == 'FLOAT':
                try:
                    float(value)
                except ValueError:
                    return [False, 'Must be a float']
            if rule == 'BOOLEAN':
                if value.lower() not in ['true', 'false']:
                    return [False, 'Must be a boolean']
            if rule == 'JSON':
                try:
                    json.loads(value)
                except ValueError:
                    return [False, 'Must be a valid JSON string']
            if rule == 'IP':
                if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', value):
                    return [False, 'Must be a valid IP address']
            if rule == 'URL':
                if not re.match(r'^(http|https)://', value):
                    return [False, 'Must be a valid URL']
            if rule == 'DATE':
                if not re.match(r'\d{4}-\d{2}-\d{2}', value):
                    return [False, 'Must be a valid date']
            if rule == 'TIME':
                if not re.match(r'\d{2}:\d{2}:\d{2}', value):
                    return [False, 'Must be a valid time']
            if rule == 'DATETIME':
                if not re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', value):
                    return [False, 'Must be a valid datetime']
            if rule == 'PHONE':
                if not re.match(r'^\d{10}$', value):
                    return [False, 'Must be a valid phone number']
            if rule == 'PASSWORD':
                if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', value):
                    return [False, 'Must be a valid password: Minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character']
        return [True, '']
    
name = Input('Password', '', 'REQUIRED|PASSWORD', 'The text is hidden')
name.display()