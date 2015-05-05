import re

_nsre = re.compile('([0-9]+)')
def SortNatural_Key(s):
    """
    Takes in a string and returns a key corresponding to its natural ordering.
    See bottom for example
    """
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(_nsre, s)]

if __name__ == '__main__':
    list = ['test10','test1','Test101']
    list.sort(key=SortNatural_Key)
    print list