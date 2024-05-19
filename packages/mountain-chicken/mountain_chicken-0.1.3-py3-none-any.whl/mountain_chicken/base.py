from double_dict import double_dict
from typing import Any, Self, List

class base:
    def __init__(self, base: int, number: str = "") -> None:
        self.number: str = number.lstrip("0")
        self.base: int = base
        self.letters: str = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:self.base]
        
        #check characters are valid
        if not all(l in self.letters for l in self.number): 
            raise ValueError(f"Invalid characters given for base{self.base}")
        
        self.d = double_dict({i : l for i,l in enumerate(self.letters)})
    
    def __add__(self, other) -> Self:
        if self.base != other.base:
            raise TypeError("bases must be the same")
        
        n1: str = self.number[::-1]
        n2: str = other.number[::-1]

        #adds leading 0s to the number
        add_0 = lambda n : n.ljust(max(len(n1),len(n2)),"0")

        n1 = add_0(n1)
        n2 = add_0(n2)
        
        res: List[str] = []

        remainder: int = 0

        for l1,l2 in zip(n1,n2):
            
            cur = self.d[l1] + self.d[l2] + remainder
            
            if  cur >= self.base:
                res.append(self.d[cur%self.base])
                remainder = cur//self.base
            
            else:
                remainder = 0
                res.append(self.d[cur])
        
        if remainder: res.append(str(remainder))
        
        return base(self.base, "".join(res[::-1]))

    def __radd__(self, other):
        
        if other == 0:
            return self
        
        return self.__add__(other)
    
    def __len__(self) -> int:
        
        return len(self.number)

    def __repr__(self) -> str:
        
        return f"{self.number}x{self.base}"
    
    def __mul__(self, other) -> Self:
        if self.base != other.base:
            raise TypeError("bases must be the same")
        
        res: List[str] = []
        
        for i, n in enumerate(self.number[::-1]):
            for j, m in enumerate(other.number[::-1]):
                cur: int = self.d[m] * self.d[n]
                
                temp: List[str] = []
                
                while cur:
                    temp.append(str(cur%self.base))
                    cur = cur//self.base
                
                temp = temp[::-1]
                
                res.append(base(self.base, "".join(temp) + (i+j)*"0"))
        
        return sum(res)




print(base(10,"123") * base(10,"456"))


 