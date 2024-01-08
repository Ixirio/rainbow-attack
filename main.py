import random
from datetime import datetime

from json_storer import JsonStorer
from string_hasher import StringHasher

class RainbowAttack:

    hash_challenges = []
    words = []
    data = {}

    attack_start_date : datetime
    attack_end_date : datetime

    def __init__(self, iteration = 1000000) -> None:
        self.hash_challenges = self.read_file_data('hash_challenges.txt')
        self.words = self.read_file_data('words_ccm_2023.txt')

        self.attack_start_date = datetime.now()
        self.attack(iteration)
        
        print(datetime.now() - self.attack_start_date)


    def read_file_data(self, fileName):
        with open(fileName) as file:
            return [line.strip('\n') for line in file.readlines()]

    def interlace(self, word, numbers = None, numbers_count = 4):
        if numbers is None:
            numbers = ''.join(str(random.randint(0, 9)) for _ in range(numbers_count))

        return ''.join(map(next, random.sample(
            [iter(word)] * len(word) + [iter(numbers)] * numbers_count, len(word) + numbers_count
        )))

    def create_word(self, word = None, numbers = None):
        return self.interlace(random.choice(self.words) if word is None else word, numbers)


    def first_reduce(self, hash):
        return StringHasher.hash(
            self.create_word(self.words[int(''.join(filter(str.isdigit, hash))) % len(self.words)])
        )

    def second_reduce(self, hash):
        hash_digits = ''.join(filter(str.isdigit, hash))

        number = int(hash_digits[0:len(hash_digits):3])

        while number > len(self.words):
            number %= len(self.words)

        return StringHasher.hash(self.create_word(self.words[number]))

    def third_reduce(self, hash):
        return StringHasher.hash(self.create_word(None, str("%04d" % int(''.join(filter(str.isdigit, hash))[:4]))))

    def attack(self, iteration):
        for _ in range(iteration):
            word = self.create_word()

            hash = self.third_reduce(self.second_reduce(self.first_reduce(StringHasher.hash(word))))

            if hash in self.hash_challenges:
                self.data['success'][word] = hash

            self.data[word] = hash

        JsonStorer.store(self.data)


if __name__ == '__main__':
    rainbowAttack = RainbowAttack()
