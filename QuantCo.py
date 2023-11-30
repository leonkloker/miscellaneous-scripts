class Series:

    @staticmethod
    def __check_data(data):
        if type(data) != list:
            raise ValueError("Given data is not in list format!")
        
        data_type = None
        mixed_numeric = False
        for elem in data:
            if elem != None:
                if data_type == None:
                    data_type = type(elem)

                elif (data_type == int and type(elem) == float) or (data_type == float and type(elem) == int):
                    mixed_numeric = True

                elif type(elem) != data_type:
                    raise ValueError("The list of values specified contains elements of different data types!")
                
        if mixed_numeric:
            data_type = float
            data = [float(elem) if elem != None else None for elem in data]
        
        return data, data_type
    
    def __equality_check(self, other):
        if not isinstance(other, Series):
            raise ValueError("Can't compare Series to non-Series type!")
        if len(self) != len(other):
            raise ValueError("Can't compare two Series of different lengths!")
        if self.type != other.type:
            raise ValueError("Can't compare two Series of different types!")

    @staticmethod
    def __new__(cls, data = []):
        data, data_type = Series.__check_data(data)

        if data_type == int:
            return super(Series, cls).__new__(SeriesInt)
        elif data_type == float:
            return super(Series, cls).__new__(SeriesFloat)
        elif data_type == bool:
            return super(Series, cls).__new__(SeriesBool)
        elif data_type == str:
            return super(Series, cls).__new__(SeriesString)
        else:
            return super(Series, cls).__new__(cls)
        
    def __init__(self, data = []):
        self.data, self.type = Series.__check_data(data)

    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, index):
        if type(index) == int:
            return self.data[index]
        
        elif type(index) == SeriesBool:
            if len(index) != len(self):
                raise ValueError("The given index Series is not the same length as the data Series!")
            
            data = []
            for i, elem in enumerate(self.data):
                if index[i]:
                    data.append(elem)
            return Series(data)
        
        else:
            raise ValueError("The given index is not of type int or SeriesBool!")
        
    def __eq__(self, other):
        self.__equality_check(other)
        
        data = []
        for i, elem in enumerate(self.data):
            data.append(elem == other[i])
        return SeriesBool(data)
    
    def __ne__(self, other):
        self.__equality_check(other)
        
        data = []
        for i, elem in enumerate(self.data):
            data.append(elem != other[i])
        return SeriesBool(data)
    
    def __repr__(self) -> str:
        return ', '.join(map(str, self.data))
    
class SeriesBool(Series):

    def __init__(self, data = []):
        super().__init__(data)
        if self.type != bool:
            raise ValueError("Can't create SeriesBool with non-boolean data!")
        
    def __boolean_check(self, other):
        if type(other) != SeriesBool and type(other) != bool:
            raise ValueError("Can't perform boolean operator on Series and non-Series, non-bool type!")
        elif type(other) == SeriesBool:
            if len(self) != len(other):
                raise ValueError("Can't perform boolean operator on two Series of different lengths!")
            else:
                return False
        else:
            return True
    
    def __and__(self, other):
        flag = self.__boolean_check(other)
        if flag:
            data = []
            for elem in self.data:
                if elem == None:
                    data.append(None)
                else:
                    data.append(elem & other)
            return SeriesBool(data)
        else:
            data = []
            for elem1, elem2 in zip(self.data, other.data):
                if elem1 == None or elem2 == None:
                    data.append(None)
                else:
                    data.append(elem1 & elem2)
            return SeriesBool(data)
    
    def __or__(self, other):
        flag = self.__boolean_check(other)
        if flag:
            data = []
            for elem in self.data:
                if elem == None:
                    data.append(None)
                else:
                    data.append(elem | other)
            return SeriesBool(data)
        else:
            data = []
            for elem1, elem2 in zip(self.data, other.data):
                if elem1 == None or elem2 == None:
                    data.append(None)
                else:
                    data.append(elem1 | elem2)
            return SeriesBool(data)
    
    def __xor__(self, other):
        flag = self.__boolean_check(other)
        if flag:
            data = []
            for elem in self.data:
                if elem == None:
                    data.append(None)
                else:
                    data.append(elem ^ other)
            return SeriesBool(data)
        else:
            data = []
            for elem1, elem2 in zip(self.data, other.data):
                if elem1 == None or elem2 == None:
                    data.append(None)
                else:
                    data.append(elem1 ^ elem2)
            return SeriesBool(data)
    
    def __invert__(self):
        data = []
        for elem in self.data:
            if elem == None:
                data.append(None)
            else:
                data.append(not elem)
        return SeriesBool(data)
    
class SeriesString(Series):

    def __init__(self, data = []):
        super().__init__(data)
        if self.type != str:
            raise ValueError("Can't create SeriesString with non-string data!")
    
class SeriesInt(Series):

    def __init__(self, data = []):
        super().__init__(data)
        if self.type != int:
            raise ValueError("Can't create SeriesInt with non-integer data!")
        
    def __int_check(self, other):
        if type(other) != SeriesInt and type(other) != int:
            raise ValueError("Can't perform arithmetic operation on SeriesInt and non-SeriesInt, non-int type!")
        elif type(other) == SeriesInt:
            if len(self) != len(other):
                raise ValueError("Can't perform arithmetic operation on two Series of different lengths!")
            else:
                return False
        else:
            return True
        
    def __add__(self, other):
        flag = self.__int_check(other)
        if flag:
            data = []
            for elem in self.data:
                if elem == None:
                    data.append(None)
                else:
                    data.append(elem + other)
            return SeriesInt(data)
        else:
            data = []
            for elem1, elem2 in zip(self.data, other.data):
                if elem1 == None or elem2 == None:
                    data.append(None)
                else:
                    data.append(elem1 + elem2)
            return SeriesInt(data)
    
    def __sub__(self, other):
        flag = self.__int_check(other)
        if flag:
            data = []
            for elem in self.data:
                if elem == None:
                    data.append(None)
                else:
                    data.append(elem - other)
            return SeriesInt(data)
        else:
            data = []
            for elem1, elem2 in zip(self.data, other.data):
                if elem1 == None or elem2 == None:
                    data.append(None)
                else:
                    data.append(elem1 - elem2)
            return SeriesInt(data)
    
    def __mul__(self, other):
        flag = self.__int_check(other)
        if flag:
            data = []
            for elem in self.data:
                if elem == None:
                    data.append(None)
                else:
                    data.append(elem * other)
            return SeriesInt(data)
        else:
            data = []
            for elem1, elem2 in zip(self.data, other.data):
                if elem1 == None or elem2 == None:
                    data.append(None)
                else:
                    data.append(elem1 * elem2)
            return SeriesInt(data)
    
    def __truediv__(self, other):
        flag = self.__int_check(other)
        if flag:
            data = []
            for elem in self.data:
                if elem == None:
                    data.append(None)
                else:
                    data.append(elem / other)
            return SeriesFloat(data)
        else:
            data = []
            for elem1, elem2 in zip(self.data, other.data):
                if elem1 == None or elem2 == None:
                    data.append(None)
                else:
                    data.append(elem1 / elem2)
            return SeriesFloat(data)
    
    def __lt__(self, other):
        flag = self.__int_check(other)
        if flag:
            data = []
            for elem in self.data:
                if elem == None:
                    data.append(None)
                else:
                    data.append(elem < other)
            return SeriesBool(data)
        else:
            data = []
            for elem1, elem2 in zip(self.data, other.data):
                if elem1 == None or elem2 == None:
                    data.append(None)
                else:
                    data.append(elem1 < elem2)
            return SeriesBool(data)
    
    def __le__(self, other):
        flag = self.__int_check(other)
        if flag:
            data = []
            for elem in self.data:
                if elem == None:
                    data.append(None)
                else:
                    data.append(elem <= other)
            return SeriesBool(data)
        else:
            data = []
            for elem1, elem2 in zip(self.data, other.data):
                if elem1 == None or elem2 == None:
                    data.append(None)
                else:
                    data.append(elem1 <= elem2)
            return SeriesBool(data)
    
    def __gt__(self, other):
        flag = self.__int_check(other)
        if flag:
            data = []
            for elem in self.data:
                if elem == None:
                    data.append(None)
                else:
                    data.append(elem > other)
            return SeriesBool(data)
        else:
            data = []
            for elem1, elem2 in zip(self.data, other.data):
                if elem1 == None or elem2 == None:
                    data.append(None)
                else:
                    data.append(elem1 > elem2)
            return SeriesBool(data)
    
    def __ge__(self, other):
        flag = self.__int_check(other)
        if flag:
            data = []
            for elem in self.data:
                if elem == None:
                    data.append(None)
                else:
                    data.append(elem >= other)
            return SeriesBool(data)
        else:
            data = []
            for elem1, elem2 in zip(self.data, other.data):
                if elem1 == None or elem2 == None:
                    data.append(None)
                else:
                    data.append(elem1 >= elem2)
            return SeriesBool(data)
    
class SeriesFloat(Series):

    def __init__(self, data = []):
        super().__init__(data)
        if self.type != float:
            raise ValueError("Can't create SeriesFloat with non-float data!")
        
    def __float_check(self, other):
        if type(other) != SeriesFloat and type(other) != float:
            raise ValueError("Can't perform arithmetic operation on SeriesFloat and non-SeriesFloat, non-float type!")
        elif type(other) == SeriesFloat:
            if len(self) != len(other):
                raise ValueError("Can't perform arithmetic operation on two Series of different lengths!")
            else:
                return False
        else:
            return True
    
    def __add__(self, other):
        flag = self.__float_check(other)
        if flag:
            data = []
            for elem in self.data:
                if elem == None:
                    data.append(None)
                else:
                    data.append(elem + other)
            return SeriesFloat(data)
        else:
            data = []
            for elem1, elem2 in zip(self.data, other.data):
                if elem1 == None or elem2 == None:
                    data.append(None)
                else:
                    data.append(elem1 + elem2)
            return SeriesFloat(data)
    
    def __sub__(self, other):
        flag = self.__float_check(other)
        if flag:
            data = []
            for elem in self.data:
                if elem == None:
                    data.append(None)
                else:
                    data.append(elem - other)
            return SeriesFloat(data)
        else:
            data = []
            for elem1, elem2 in zip(self.data, other.data):
                if elem1 == None or elem2 == None:
                    data.append(None)
                else:
                    data.append(elem1 - elem2)
            return SeriesFloat(data)
    
    def __mul__(self, other):
        flag = self.__float_check(other)
        if flag:
            data = []
            for elem in self.data:
                if elem == None:
                    data.append(None)
                else:
                    data.append(elem * other)
            return SeriesFloat(data)
        else:
            data = []
            for elem1, elem2 in zip(self.data, other.data):
                if elem1 == None or elem2 == None:
                    data.append(None)
                else:
                    data.append(elem1 * elem2)
            return SeriesFloat(data)
    
    def __truediv__(self, other):
        flag = self.__float_check(other)
        if flag:
            data = []
            for elem in self.data:
                if elem == None:
                    data.append(None)
                else:
                    data.append(elem / other)
            return SeriesFloat(data)
        else:
            data = []
            for elem1, elem2 in zip(self.data, other.data):
                if elem1 == None or elem2 == None:
                    data.append(None)
                else:
                    data.append(elem1 / elem2)
            return SeriesFloat(data)
    
    def __lt__(self, other):
        flag = self.__float_check(other)
        if flag:
            data = []
            for elem in self.data:
                if elem == None:
                    data.append(None)
                else:
                    data.append(elem < other)
            return SeriesBool(data)
        else:
            data = []
            for elem1, elem2 in zip(self.data, other.data):
                if elem1 == None or elem2 == None:
                    data.append(None)
                else:
                    data.append(elem1 < elem2)
            return SeriesBool(data)
    
    def __le__(self, other):
        flag = self.__float_check(other)
        if flag:
            data = []
            for elem in self.data:
                if elem == None:
                    data.append(None)
                else:
                    data.append(elem <= other)
            return SeriesBool(data)
        else:
            data = []
            for elem1, elem2 in zip(self.data, other.data):
                if elem1 == None or elem2 == None:
                    data.append(None)
                else:
                    data.append(elem1 <= elem2)
            return SeriesBool(data)
    
    def __gt__(self, other):
        flag = self.__float_check(other)
        if flag:
            data = []
            for elem in self.data:
                if elem == None:
                    data.append(None)
                else:
                    data.append(elem > other)
            return SeriesBool(data)
        else:
            data = []
            for elem1, elem2 in zip(self.data, other.data):
                if elem1 == None or elem2 == None:
                    data.append(None)
                else:
                    data.append(elem1 > elem2)
            return SeriesBool(data)
    
    def __ge__(self, other):
        flag = self.__float_check(other)
        if flag:
            data = []
            for elem in self.data:
                if elem == None:
                    data.append(None)
                else:
                    data.append(elem >= other)
            return SeriesBool(data)
        else:
            data = []
            for elem1, elem2 in zip(self.data, other.data):
                if elem1 == None or elem2 == None:
                    data.append(None)
                else:
                    data.append(elem1 >= elem2)
            return SeriesBool(data)
    
class DataFrame:

    def __init__(self, data = {}, index = []):
        if type(data) != dict:
            raise ValueError("Given data is not in dict format!")
        
        for key in data:
            if not isinstance(data[key], Series):
                raise ValueError("Given data is not in Series format!")
        self.data = data
    
    def __getitem__(self, key):
        if type(key) == str:
            return self.data[key]
        
        elif type(key) == SeriesBool:
            if len(key) != len(self):
                raise ValueError("The given index Series is not the same length as the DataFrame!")
            
            data = {}
            for index, value in self.data.items():
                data[index] = value[key]
            return DataFrame(data)
        
        else:
            raise ValueError("The given index is not of type str or SeriesBool!")
    
    def __len__(self):
        for key in self.data:
            return len(self.data[key])
    
    def __repr__(self):
        string = "DataFrame \n" 
        for key in self.data:
            string += str(key) + ": " + str(self.data[key]) + "\n"
        return string
