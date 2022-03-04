MIN_LENGTH = 8

def file_path(instance, filename):
    return "file/{}".format(filename)


class StringShortener(object):
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
	
    def __init__(self, block_size=62):
        if len(self.alphabet) < 2:
            raise AttributeError('Alphabet has to contain at least 2 characters.')

        self.block_size = block_size
        self.mask = (1 << block_size) - 1
        self.mapping = range(block_size)

    def encode_url(self, n, min_length=MIN_LENGTH):
        return self.enbase(self.encode(n), min_length)
        
    def decode_url(self, n):
        return self.decode(self.debase(n))

    def encode(self, n):
        return (n & ~self.mask) | self._encode(n & self.mask)

    def _encode(self, n):
        result = 0
        for i, b in enumerate(reversed(self.mapping)):
            if n & (1 << i):
                result |= (1 << b)
        return result

    def decode(self, n):
        return (n & ~self.mask) | self._decode(n & self.mask)

    def _decode(self, n):
        result = 0
        for i, b in enumerate(reversed(self.mapping)):
            if n & (1 << b):
                result |= (1 << i)
        return result

    def enbase(self, x, min_length=MIN_LENGTH):
        result = self._enbase(x)
        padding = self.alphabet[0] * (min_length - len(result))
        return '%s%s' % (padding, result)

    def _enbase(self, x):
        n = len(self.alphabet)
        if x < n:
            return self.alphabet[x]
        return self._enbase(int(x // n)) + self.alphabet[int(x % n)]

    def debase(self, x):
        n = len(self.alphabet)
        result = 0
        for i, c in enumerate(reversed(x)):
            result += self.alphabet.index(c) * (n ** i)
        return result