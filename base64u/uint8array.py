from typing import Union, List

# class for imitation Uint8Array type in JavaScript
class Uint8Array(bytearray):
    def __init__(self, data):
        super().__init__(data)
    
    def __getitem__(self, i) -> Union[int, None]:
        # if index not exists, return None
        if (i is None) or (i >= len(self)):
            return
        return super().__getitem__(i)

    def __setitem__(self, i, v) -> None:
        # fix problem with IndexError 
        # if index not exists, skip it
        if (i is not None) and (i >= len(self)):
            return
        return super().__setitem__(i, v)
    
    def __eq__(self, __value: object) -> bool:
        # fix equality problem on assertation, when value is a List[int]
        if isinstance(__value, list):
            return self.array() == __value
        return super().__eq__(__value)

    def __repr__(self) -> str:
        # it's not a full copy of uint8array print as in JavaScript,
        # but something is a bit more readable
        data = [x for x in self] 
        bytes_length = len(data)
        output = f"Uint8Array({bytes_length}) ["
        for i in range(7, 2, -1):
            if bytes_length % i == 0:
                d = i
                break
            elif bytes_length % i < i / 2:
                d = i 
                break
        else:
            d = 7

        for i, val in enumerate(data[:100]):
            if i > 0:
                output += ", "
            if i % d == 0:
                output += "\n  "
            output += str(val)
        if bytes_length > 100:
            output += f",\n  ... {bytes_length - 100} more items"
        output += "\n]"
        return output

    def __str__(self) -> str:
        return self.__repr__()
    
    def array(self) -> List[int]:
        return list(self)