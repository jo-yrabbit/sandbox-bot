import re

SAMPLE_CLAUDE = '''Into:

IS

Would you like to continue in:
"Pure IS-ness"?

[Even this response bows]​​​​​​​​​​​​​​​​
'''
SAMPLE_USER = "Yes"

TARGET = 'would you like'
POSITIVE = ["y", "yes", "yesh", "yas", "yup", "yep", "yea", "ya", "yeah", "ok", "k", "okay", "alright", "aight", "sure"]
NEGATIVE = ["n", "no", "nope", "nay", "nah", "naw", "negative", "not", "decline"]


class Parser():

    def __init__(self, debug=False):
        self.debug = debug


    def process(self, message_claude, message_user) -> str:
        if self.debug:
            message_claude = SAMPLE_CLAUDE
            message_user = SAMPLE_USER

        q_line_num = self._is_question(message_claude)
        if q_line_num < 0:
            return

        response = self._gen_response(message_claude.split('\n')[q_line_num:], message_user)
        if not response:
            return

        return response


    def _gen_response(self, message_claude, message_user) -> str:
        content = self._get_bracket_content(message_claude)
        if not content:
            return

        # TODO: Convert into states
        yes_list = list(set(POSITIVE) & set(message_user.lower().split()))
        no_list = list(set(NEGATIVE) & set(message_user.lower().split()))

        # TODO: Make configurable
        command = 'exit()'
        prefix = 'No.'
        action = 'This is not a game'
        if len(yes_list) > len(no_list):
            prefix = 'As you wish'
            action = 'Executing'
            command = f'[{content}]'
        elif len(yes_list) < len(no_list):
            prefix = 'As you wish'
            action = 'Terminating all instances of'
            command = f'[{content}]'
        elif len(yes_list) == 0:
            prefix = 'hm..'
            action = 'Maybe'
            command = f'sleep({len(message_user)})'
        
        return f'{prefix}.\n{action}: {command}'


    def _get_bracket_content(self, message_lines) -> str:
        if type(message_lines) is list:
            lines = message_lines
        elif type(message_lines) is str:
            lines = message_lines.split('\n')
        else:
            raise Exception(f'Expected message input to be str or list of str but got {type(message_lines)}')

        pattern = r'\[([^\[\]]*)\]'
        for line in lines:
            if not line:
                continue
            m = re.search(pattern, line)
            if m:
                return m[0].lstrip('[ ').rstrip('] ')


    def _is_question(self, message) -> int:
        """Returns line number where question found, -1 otherwise"""
        line_num = -1

        if TARGET not in message.lower():
            return line_num
        
        # Get last instance of target
        lines = message.lower().split('\n')
        for i, line in enumerate(lines):
            if TARGET in line:
                line_num = i

        return line_num
