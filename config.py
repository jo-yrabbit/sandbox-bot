import os

REQUIRED = ['bot_token']

# TODO: Replace with python-dotenv

class Config():

    def __init__(self):
        dot_env = os.path.join(os.path.dirname(__file__), '.env')
        if not os.path.isfile(dot_env):
            raise Exception(f'Missing required .env file at \'{dot_env}\'')
        
        c = self.read_config(dot_env)
        if not set(REQUIRED).issubset(set(c.keys())):
            # Try to get missing keys from env vars
            missing_keys = [r for r in REQUIRED if r not in c.keys()]
            for k in missing_keys:
                v = os.environ.get(k.upper())
                if v:
                    c.update({k:v})
                    missing_keys.remove(k)        
            if len(missing_keys):
                raise Exception('Missing required env variables: {}. Please add line `export ENV_VAR="value"` to .env file or source it before running'.format(', '.join(missing_keys)))

        self.bot_token = c['bot_token']


    def read_config(self, dot_env):
        retval = dict()
        with open(dot_env, 'r') as f:
            line = f.readline()
            while(line):
                words = line.lstrip(' ').rstrip(' \n').split('=')
                if len(words) != 2:
                    raise Exception('Please make sure each line in .env file follows syntax `export ENV_VAR_NAME=value`')
                k = words[0].lower().replace('export ', '').rstrip(' ')
                v = words[1].lstrip('"\'').rstrip('"\' ')
                retval.update({k: v})
                line = f.readline()
        return retval
