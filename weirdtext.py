# https://gist.github.com/sargo/e3a4d72fbdace178e1b6
import random
import re


class WeirdtextEncoder:
    """Weirdtext encoder class

    Use encode(message) method to encode a message with Weirdtext.
    """
    def __init__(self):
        self.word_list = None

    @staticmethod
    def shuffle_word(word):
        """Return transformed word with characters at internal positions shuffled."""
        shuffled_word = word
        while shuffled_word == word:  # Until we got a different word from original one
            internal_part = list(word[1:-1])  # Cut out the internal part and save it as mutable list
            random.shuffle(internal_part)  # Shuffle the elements of mutable list
            shuffled_word = word[0] + ''.join(internal_part) + word[-1]  # Concat the word
        return shuffled_word

    def process_word(self, match):
        """Take Match object and return encoded word"""
        word = match.group(0)  # Extract the word from Match object

        # We don't need to encode words shorter than 3 characters as this wont change it
        if len(word) > 3:
            self.word_list.add(word)  # Add word to set of plain words
            shuffled_word = self.shuffle_word(word)  # Encode word by shuffling its internal part
            return shuffled_word
        return word

    def encode(self, plain_text):
        separator = '\n---weird---\n'

        self.word_list = set()  # Initialize an empty word set

        # Encode the text by running self.process_word() method on every word and replacing the plain words
        # with encoded ones.
        encoded_text = re.sub(r'\w+', self.process_word, plain_text)

        used_words = ' '.join(sorted(self.word_list))  # Prepare a list of alphabetically sorted words
        weirdtext_message = f'{separator}{encoded_text}{separator}{used_words}'  # Concat a Weirdtext message
        return weirdtext_message


class WeirdtextDecoder:
    """Weirdtext decoder class

    Use decode(message) method to decode a Weirdtext message.
    """

    def __init__(self):
        self.word_map = None

    @staticmethod
    def _sort_internal_part(word):
        """Return transformed word with characters at internal positions sorted alphabetically."""
        return word[0] + ''.join(sorted(word[1:-1])) + word[-1]

    def _process_word(self, match):
        """Take Match object and return decoded word"""
        encoded_word = match.group(0)  # Extract the encoded word from Match object

        # We don't need to decode words with less than 3 characters since they wont change after that
        if len(encoded_word) > 3:
            sorted_word = self._sort_internal_part(encoded_word)  # Sort its internal part
            decoded_word = self.word_map[sorted_word]  # Use the sorted part as dictionary key to get the plain word
            return decoded_word

        else:
            return encoded_word

    def decode(self, message):
        """Decode 'message' encoded with Weirdtext"""

        separator = '\n---weird---\n'

        # Unpack message
        _, encoded_text, word_set = message.split(separator)

        # Extract plain words into a map/dictionary
        self.word_map = {self._sort_internal_part(word): word for word in word_set.split()}

        # Replace every encoded word with decoded one
        plain_text = re.sub(r'\w+', self._process_word, encoded_text)

        return plain_text


if __name__ == '__main__':
    # Tests...
    encoder = WeirdtextEncoder()
    decoder = WeirdtextDecoder()

    original_message = 'Lorem ipsum! (test)'

    print('ENCODED:')
    encoded_message = encoder.encode(original_message)
    print(encoded_message)
    print()

    print('DECODED:')
    decoded_message = decoder.decode(encoded_message)
    print(decoded_message)
    print()

    assert original_message == decoded_message

    assert decoder.decode(encoder.encode('Ala ma kota, a kot ma ale :-)')) \
           == 'Ala ma kota, a kot ma ale :-)'

    assert decoder.decode(encoder.encode('Alfdasdfa am ffhrtha kohrthrt lelele')) \
           == 'Alfdasdfa am ffhrtha kohrthrt lelele'
