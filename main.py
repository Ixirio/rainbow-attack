import random
from datetime import datetime, timedelta

from json_storer import JsonStorer
from string_hasher import StringHasher
from txt_file_reader import TxtFileReader

class RainbowAttack:

    hash_challenges : list = []
    words : list = []
    data : dict = {
        'try' : {},
        'success' : {}
    }

    start_date: datetime
    attack_time: timedelta

    def __init__(self, iteration = 1000000) -> None:
        self.hash_challenges = TxtFileReader.read('hash_challenges.txt')
        self.words = TxtFileReader.read('words_ccm_2023.txt')

        self.start_date = datetime.now()
        self.attack(iteration)
        self.attack_time = datetime.now() - self.start_date
        print(self.attack_time)

    def insert_digit(self, source, digit, position):
        return source[:position] + digit + source[position:]

    def interlace(self, word, numbers = None, numbers_count = 4) -> str:
        if numbers is not None:
            for index, number in enumerate(numbers):
                word = self.insert_digit(word, number, index * 2 % len(word))
            return word

        else:
            numbers = ''.join(str(random.randint(0, 9)) for _ in range(numbers_count))

        return ''.join(map(next, random.sample(
            [iter(word)] * len(word) + [iter(numbers)] * numbers_count, len(word) + numbers_count
        )))
    
    def get_digits_from_hash(self, hash) -> str:
        return ''.join(filter(str.isdigit, hash))

    def create_word(self, word = None, numbers = None) -> str:
        return self.interlace(random.choice(self.words) if word is None else word, numbers)

    def first_reduce(self, hash) -> str:
        hash_digits = self.get_digits_from_hash(hash)

        index = int(hash_digits) % len(self.words)

        while index >= len(self.words):
            index %= len(self.words) * 1.5

        return StringHasher.hash(
            self.create_word(
                self.words[index],
                str("%04d" % int(hash_digits[:4]))
            )
        )

    def second_reduce(self, hash) -> str:
        hash_digits = self.get_digits_from_hash(hash)

        index = int(hash_digits[::3])

        while index >= len(self.words):
            index %= len(self.words)

        return StringHasher.hash(
            self.create_word(
                self.words[index],
                str("%04d" % int(hash_digits[::2][:4]))
            )
        )

    def third_reduce(self, hash) -> str:
        hash_digits = self.get_digits_from_hash(hash)

        index = int(hash_digits) % len(self.words)
        
        while index >= len(self.words):
            index %= len(self.words) * 0.75

        return StringHasher.hash(
            self.create_word(
                self.words[index],
                str("%04d" % int(hash_digits[::3][:4]))
            )
        )

    def reduce(self, word) -> str:
        return self.third_reduce(
            self.second_reduce(
                self.first_reduce(
                    StringHasher.hash(word)
                )
            )
        )

    def attack(self, iteration):
        div = iteration / 100
        for index in range(iteration):
            if (index % div == 0):
                print(f'iteration {index}, elapsed time : {datetime.now() - self.start_date}')

            word = self.create_word()
            while word in self.data['try'].keys():
                word = self.create_word()

            hash = self.reduce(word)

            if hash in self.hash_challenges:
                self.data['success'][word] = hash

            self.data['try'][word] = hash

        print('attack ended, storing..')
        JsonStorer.store(self.data['try'], file_name='try.json')
        JsonStorer.store(self.data['success'], file_name='success.json')

if __name__ == '__main__':
    rainbowAttack = RainbowAttack()
