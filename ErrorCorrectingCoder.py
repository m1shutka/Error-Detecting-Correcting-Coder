from Field import Field

class ErrorCorrectingCoder():
    def  __create_letters(self):
        for i in range(32):
            self.__letters.append(Field(str(i), self.__create_code(i), self.__create_protected_code(self.__create_code(i))))

    def __init__(self):
        self.__G = [[1, 0, 0, 0, 0, 0, 1, 0, 1], 
                    [0, 1, 0, 0, 0, 1, 0, 1, 1],
                    [0, 0, 1, 0, 0, 1, 1, 0, 0],
                    [0, 0, 0, 1, 0, 0, 1, 1, 0],
                    [0, 0, 0, 0, 1, 0, 0, 1, 1]]
        self.__H = [[0, 1, 0, 1],
                    [1, 0, 1, 1],
                    [1, 1, 0, 0],
                    [0, 1, 1, 0],
                    [0, 0, 1, 1],
                    [1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1],]
        self.__letters = []
        self.__create_letters()

    def __create_protected_code(self, code):
        """Генерация защищенного кода"""
        answer = ''
        list_code = []
        for i in code:
            list_code.append(int(i))
        res = self.__dot(list_code, self.__G)
        for i in res:
            answer += str(i)
        return answer

    def __create_code(self, symbol):
        """Кодирование символов"""
        res = bin(symbol)[2:]
        while len(res) < 5:
            res = "0" + res
        return res

    def  __xor(self, a, b):
        """Сложение по модулю два"""
        if(a == b):
            return 0
        else:
            return 1

    def __dot(self, a, b):
        """Произведение вектор-строки на матрицу"""
        result = [None]*len(b[0])
        for i in range(len(b[0])):
            for j in range(len(a)):
                if result[i] == None:
                    result[i] = a[j]*b[j][i]
                else:
                    result[i] = self.__xor(result[i], a[j]*b[j][i])
        return result

    def __check_code(self, code):
        """Проверка кода"""
        list_code = []
        for i in code:
            list_code.append(int(i))
        res = self.__dot(list_code, self.__H)
        return res

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
        result = []
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
                syndrome = self.__check_code(i)
                if 1 in syndrome:
                    deffect.append(i)
                    result.append(self.__correcting(i, syndrome))
                else:
                    result.append(i)
        return error, deffect, result

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

    def __decode_codeword(self, code):
        """Декодирование слова"""
        return int('0b' + code[:5], 2)

    def __decode_text(self,text):
        """Декодирование текста"""
        result = []
        for code in text:
            result.append(self.__decode_codeword(code))
        return result

    def __encorrect_index(self, syndrome):
        for i in range(len(self.__H)):
            if syndrome == self.__H[i]:
                return i

    def __correcting(self, code, syndrome):
        pos = self.__encorrect_index(syndrome)
        result = ''
        for i in range(len(code)):
            if i == pos:
                if code[pos] == '0':
                    result += '1'
                else:
                    result += '0'
            else:
                result += code[i]
        return result

    def decode(self, file_name):
        """Метод декодирования текста"""
        res = []
        error, deffect, text = self.__load_decode(file_name)
        if error == "":
            res = self.__decode_text(text)
            return error, deffect,  " ".join(str(i) for i in res)
        else:
            return error, deffect, ""

    def get_alphabet(self):
        """Метод возвращающий текущий алфавит кодировщика"""
        res = []
        for i in self.__letters:
            res.append(i.symbol)
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