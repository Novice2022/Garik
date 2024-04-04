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
