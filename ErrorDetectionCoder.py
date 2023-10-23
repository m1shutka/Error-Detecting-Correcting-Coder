from field import Field
from Tree import Tree
from math import ceil, log2, floor

class ErrorDetectionCoder():
    def __create_letters(self, alphabet):
        """Создание таблицы"""
        letters = []
        probabilities = [1/len(alphabet)]*len(alphabet)
        for sym, p in zip(alphabet, probabilities):
            letters.append(Field(sym, p))
        return letters

    def __complete_letters(self):
        """Заполнение таблицы"""
        q = self.__cumulative_probability()
        for i in range(len(self.__letters)):
            self.__letters[i].code = self.__create_codewords((q[i] + self.__letters[i].p/2), ceil(-log2(self.__letters[i].p/2)))
            if len(self.__letters[i].code) % 2 == 0:
                j = 0
                s = self.__letters[i].code
                while(j < len(self.__letters[i].code)):
                    j+=2
                    s = s[:j] + self.__xor(s[j-1], s[j-2]) + s[j:]
                    j+=1
                self.__letters[i].subcode = s
            else:
                pass

    def __init__(self):
        """Инициализация класса"""
        self.__letters = self.__create_letters(['11', '12', '13', '14', '15', '16', '17'])
        self.__complete_letters()

    def __create_codewords(self, q, l):
        """Создание кодов слов"""
        digits = ["0", "1"]
        temp = q
        code = ""
        for i in range(l):
            temp *= 2
            j = int(floor(temp))
            code += digits[j]
            temp -= j
        return code

    def __load_encode(self, file_name):
        """Загрузка текста для кодирования"""
        text = []
        alphabet = []
        error = ""
        for i in self.__letters:
             alphabet.append(i.symbol)
        try:
            with open(file_name, "r", encoding="UTF-8") as file_in:
                text = list(map(str, file_in.read().split()))
        except FileNotFoundError:
            error = f"Файл <<{file_name}>> не найден!"
        else:
            if len(text) == 0:
                error = f"Файл <<{file_name}>> пуст!"
            for i in text:
                if i not in alphabet:
                    error = f"Значение {i} отсутсвует в алфавите!"
                    break
        return error, text

    def __load_decode(self, file_name):
        """Загрузка текста для раскодирования"""
        text = []
        codes = []
        deffect = []
        error = ""
        for i in self.__letters:
             codes.append(i.subcode)
        try:
            with open(file_name, "r", encoding="UTF-8") as file_in:
                text = list(map(str, file_in.read().split()))
        except FileNotFoundError:
            error = f"Файл <<{file_name}>> не найден!"
        else:
            if len(text) == 0:
                error = f"Файл <<{file_name}>> пуст!"
            for i in text:
                if not self.__check_code(i):
                    deffect.append(i)
            for i in deffect:
                text.remove(i)
        return error, deffect, text

    def __cumulative_probability(self):
        """Вычисление куммулитивной вероятности"""
        q = []
        _sum = 0
        for i in self.__letters:
            q.append(_sum)
            _sum += i.p
        return q

    def  __xor(self, a, b):
        """Сложение по модулю два"""
        if(a == b):
            return '0'
        else:
            return '1'

    def __check_code(self, code):
        """Проверка кода на четность"""
        res = code[0]
        for i in range(1, len(code)):
            res = self.__xor(res, code[i])
        if res == '0':
            return True
        else:
            return False

    def __create_tree(self):
        """Формирование дерева"""
        tree = Tree()
        for i in self.__letters:
            tree.add(i.subcode, i.symbol, 0)
        return tree

    def __decode_codeword(self, node, code):
        """Декодирование слова"""
        for i in code: 
            if i == "0":
                node = node.left
            elif i == "1":
                node = node.right
        return node.value

    def __decode_text(self, tree, text):
        """Декодирование текста"""
        result = []
        root = tree.get_root()
        for code in text:
            letter = self.__decode_codeword(root, code)
            result.append(letter)
        return result

    def encode(self, file_name):
        """Метод кодирования текста"""
        res = []
        error, text = self.__load_encode(file_name)
        if error == "":
            for symbol in text:
                for field in self.__letters: 
                    if symbol == field.symbol:
                        res.append(field.subcode)
                        break
            return error, " ".join(str(i) for i in res)
        else:
            return error, ""

    def decode(self, file_name):
        """Метод декодирования текста"""
        res = []
        error, deffect, text = self.__load_decode(file_name)
        if error == "":
            tree = self.__create_tree()
            res = self.__decode_text(tree, text)
            return error, deffect,  " ".join(str(i) for i in res)
        else:
            return error, deffect, ""

    def get_alphabet(self):
        """Метод возвращающий текущий алфавит кодировщика"""
        res = []
        for i in self.__letters:
            res.append(i.symbol)
        return res

    def get_probabilities(self):
        """Метод возвращающий текущий набор вероятностей"""
        res = []
        for i in self.__letters:
            res.append(i.p)
        return res

    def get_code(self):
        """Метод возвращающий текущие коды алфавита"""
        res = []
        for i in self.__letters:
            res.append(i.code)
        return res

    def get_subcode(self):
        """Метод возвращающий текущие защищенные коды алфавита"""
        res = []
        for i in self.__letters:
            res.append(i.subcode)
        return res