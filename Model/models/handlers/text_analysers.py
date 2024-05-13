def normalise_punctuation(text: str) -> str:
    return text.\
        replace(" запятая", ',').\
        replace("запятая ", ',').\
        replace(" точка", '.').\
        replace("точка ", '.').\
        replace(" восклицательный знак", '!').\
        replace("восклицательный знак ", '!').\
        replace(" вопросительный знак", '?').\
        replace("вопросительный знак ", '?').\
        replace(" равно", '=').\
        replace("равно ", '=').\
        replace(" минус", '-').\
        replace("минус ", '-').\
        replace(" плюс", '+').\
        replace("плюс ", '+').\
        replace(" двоеточие", ':').\
        replace("двоеточие ", ':').\
        replace(" точка с запятой", ';').\
        replace("точка с запятой ", ';').\
        replace(" фигурная открывающая скобка", '{').\
        replace("фигурная открывающая скобка ", '{').\
        replace(" квадратная открывающая скобка", '[').\
        replace("квадратная открывающая скобка ", '[').\
        replace(" открывающая скобка", '(').\
        replace("открывающая скобка ", '(').\
        replace(" фигурная закрывающая скобка", '}').\
        replace("фигурная закрывающая скобка ", '}').\
        replace(" квадратная закрывающая скобка", ']').\
        replace("квадратная закрывающая скобка ", ']').\
        replace(" закрывающая скобка",'))').\
        replace("закрывающая скобка ",'))').\
        replace(" дефис", '-').\
        replace("дефис ", '-').\
        replace(" нижнее подчёркивание", '_').\
        replace("нижнее подчёркивание ", '_').\
        replace(" двочные кавычки", '\"').\
        replace("двочные кавычки ", '\"').\
        replace(" кавычки", '\'').\
        replace("кавычки ", '\'').\
        replace(" тильда", '~').\
        replace("тильда ", '~').\
        replace(" обратная ковычка", '`').\
        replace("обратная ковычка ", '`').\
        replace(" обратный слеш", '\\').\
        replace("обратный слеш ", '\\').\
        replace(" слеш", '/').\
        replace("слеш ", '/').\
        replace(" пробел", ' ').\
        replace("пробел ", ' ')

def hot_keys(data: str) -> str:
    match data:
        case "пробел":
            return " "
        case "табуляция":
            return "\t"
        case "следующая строка":
            return "\n"
        case "слеш":
            return "/"
        case "обратный слеш":
            return "\\"
        case "тильда":
            return "~"
        case "знак процента":
            return "%"
        case "знак умножения":
            return "*"
        case "восклицательный знак":
            return "!"
        case "собака":
            return "@"
        case "хеш":
            return "#"
        case "амперсанд":
            return "&"
        case "открыващая скобка":
            return "("
        case "закрывающая скобка":
            return ")"
        case "открыващая квадратная скобка":
            return "["
        case "закрывающая квадратная скобка":
            return "]"
        case "открыващая фигурная скобка":
            return "{"
        case "закрывающая фигурная скобка":
            return "}"
        case "кавычка":
            return "'"
        case "двойная кавычка":
            return "\""
        case "двойные кавычки":
            return "\""
        case "больше":
            return ">"
        case "меньше":
            return "<"
        case "точка":
            return "."
        case "запятая":
            return ","
        case "точка с запятой":
            return ";"
        case "двоеточие":
            return ":"
        case "номер":
            return "№"
        case "доллар":
            return "$"
        case "вертикальный слеш":
            return "|"
        case "крышечка":
            return "^"
        case "обратная кавычка":
            return "`"

def to_integer(string: str) -> int:
    if string == "":
        return 0
    if string.isdigit():
        return int(string)

    values = {
        "один": 1,
        "два": 2,
        "три": 3,
        "четыре": 4,
        "пять": 5,
        "шесть": 6,
        "семь": 7,
        "восемь": 8,
        "девять": 9,

        "десять": 10,
        "одиннадцать": 11,
        "двенадцать": 12,
        "тринадцать": 13,
        "четырнадцать": 14,
        "пятнадцать": 15,
        "шестнадцать": 16,
        "семнадцать": 17,
        "восемнадцать": 18,
        "девятнадцать": 19,
        
        "двадцать": 20,
        "тридцать": 30,
        "сорок": 40,
        "пятьдесят": 50,
        "шестьдесят": 60,
        "семьдесят": 70,
        "восемьдесят": 80,
        "девяносто": 90,
        
        "сто": 100,
        "двести": 200,
        "триста": 300,
        "четыреста": 400,
        "пятьсот": 500,
        "шестьсот": 600,
        "семьсот": 700,
        "восемьсот": 800,
        "девятьсот": 900
    }
    
    def get_up_to_thousands(substring: str) -> int:
        return sum([
            values.get(number_word)\
                for number_word in substring.split()
        ])

    summa = 0

    for thousands_degree in (
        ("миллиард", 1_000_000_000),
        ("миллион", 1_000_000),
        ("тысяч", 1_000)
    ):
        if thousands_degree[0] in string:
            before_thousand_degree =\
                string[ : string.index(\
                    thousands_degree[0]\
                        ) - 1]

            summa += get_up_to_thousands(
                string[ : string.index(\
                    thousands_degree[0]\
                ) - 1]
            )
            
            string = string.replace(before_thousand_degree, "", 1)
            string = string[string.index(" ") + 1 : ]

    summa += get_up_to_thousands(string)

    return summa
