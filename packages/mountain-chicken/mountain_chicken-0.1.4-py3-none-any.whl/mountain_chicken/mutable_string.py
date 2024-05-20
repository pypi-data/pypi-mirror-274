from typing import List

class mutable_string:
    def __init__(self, word: str = "") -> None:
        self.word = word
        self.length = len(word)

    def __len__(self) -> int:
        return self.length
    
    def __add__(word1, word2) -> str:
        return mutable_string(word1.word + word2.word)
    
    def __getitem__(self, index: int) -> str:
        return self.word[index]
    
    def __setitem__(self, index: int, characters: str) -> None:
        self.array = [*self.word]
        self.array[index] = characters
        self.word = "".join(self.array)
    
    def __str__(self) -> str:
        return self.word

