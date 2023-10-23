class Node:
    def __init__(self, value):
        self.left = None
        self.right = None
        self.value = value

class Tree:
    def __init__(self):
        self.__root = None
    
    def get_root(self):
        return self.__root

    def __add(self, node, code, symbol, index):
        if index == len(code):
            node.value = symbol
        if index < len(code) and code[index] == "0":
            if node.left is None:
                node.left = Node("")
            self.__add(node.left, code, symbol, index + 1)
        elif index < len(code) and code[index] == "1":
            if node.right is None:
                node.right = Node("")
            node.rigth = self.__add(node.right, code, symbol, index + 1)

    def add(self, code, symbol, index):
        if self.__root is None:
            self.__root = Node("")
        self.__add(self.__root, code, symbol, index)