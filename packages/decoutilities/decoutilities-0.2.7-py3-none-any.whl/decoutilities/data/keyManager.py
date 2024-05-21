import re
from random import randint, choice, shuffle
import base64
import string

class keyManager():
    def __init__(self):
        cache = str(randint(0, 2550))+str(randint(0, 2550))+str(randint(0, 2550))
        self.encryptBase = base64.b64encode(cache.encode())
        self.key = self.shuffle_string(self.replace_non_alnum(self.__keyGen())).encode()
    
    def __keyGen(self):
        cache = 0
        for char in self.encryptBase:
            for i in range(0, 255):
                cache += int(char) ^ i
        
        cache = str(int(cache)/2).replace(".", "").replace(",", "")

        for char in cache:
            if randint(0, 10) == 5:
                cache = cache.replace(char, str(randint(0, 9)))

        for char in cache:
            if int(char) > 2:
                lower_bound = int(str(int(char)/2).replace('.', ''))
                upper_bound = int(char)
                if lower_bound > upper_bound:
                    lower_bound, upper_bound = upper_bound, lower_bound
                cache += str(randint(lower_bound, upper_bound))
        
        return cache

    def shift_char(self, c):
        return chr((ord(c) + 10) % 256)

    def shift_string(self, s):
        return ''.join(self.shift_char(c) for c in s)

    def replace_non_alnum(self, s):
        s = self.shift_string(s)
        s = re.sub(r'\W', ''.join(choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(10)), s)
        return s

    def shuffle_string(self, s):
        s_list = list(s)
        shuffle(s_list)
        return ''.join(s_list)
    
key = keyManager().key
print(key)