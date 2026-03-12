import pymorphy3
from functools import reduce
import json
import re

# Пример индекса (в реальности он должен быть загружен из файлов)
index = json.load(open("index.json", "r", encoding="utf-8"))

# Инициализация морфологического анализатора
morph = pymorphy3.MorphAnalyzer()

def lemmatize_word(word):
    """Приводит слово к лемме"""
    # Убираем возможные знаки препинания в конце слова
    word = re.sub(r'[^\w\s]', '', word)
    if not word:  # если после очистки слово пустое
        return ""
    return morph.parse(word)[0].normal_form

def tokenize_query(query):
    """Улучшенная функция разбиения запроса на токены"""
    # Добавляем пробелы вокруг операторов, если их нет
    # Обрабатываем случаи типа "NOT(" -> "NOT ("
    query = re.sub(r'NOT\s*\(', 'NOT (', query)
    query = re.sub(r'AND\s*\(', 'AND (', query)
    query = re.sub(r'OR\s*\(', 'OR (', query)
    
    # Добавляем пробелы вокруг скобок
    query = query.replace('(', ' ( ').replace(')', ' ) ')
    
    # Добавляем пробелы вокруг операторов, если они слиплись со словами
    query = re.sub(r'(\w+)AND(\w+)', r'\1 AND \2', query)
    query = re.sub(r'(\w+)OR(\w+)', r'\1 OR \2', query)
    query = re.sub(r'NOT(\w+)', r'NOT \1', query)
    
    # Разбиваем на токены и фильтруем пустые
    tokens = [t for t in query.split() if t]
    
    # Приводим операторы к верхнему регистру для единообразия
    normalized_tokens = []
    for token in tokens:
        if token.upper() in ['AND', 'OR', 'NOT']:
            normalized_tokens.append(token.upper())
        else:
            normalized_tokens.append(token)
    
    return normalized_tokens

def parse_expression(tokens):
    """Рекурсивный парсер логического выражения"""
    
    def parse_primary():
        nonlocal pos
        if pos >= len(tokens):
            raise ValueError("Неожиданный конец выражения")
            
        token = tokens[pos]
        
        if token == '(':
            pos += 1
            result = parse_or_expression()
            if pos >= len(tokens) or tokens[pos] != ')':
                raise ValueError("Ожидалась закрывающая скобка")
            pos += 1
            return result
        elif token.upper() in ['AND', 'OR', 'NOT']:
            # Если оператор встретился там, где ожидается операнд
            raise ValueError(f"Неожиданный оператор {token}")
        else:
            # Это слово
            pos += 1
            lemma = lemmatize_word(token)
            if not lemma:  # если лемма пустая (был знак препинания)
                return set()
            result = set(index.get(lemma, []))
            print(f"  Лемма '{lemma}' найдена в файлах: {result}")
            return result
    
    def parse_not_expression():
        nonlocal pos
        if pos < len(tokens) and tokens[pos].upper() == 'NOT':
            pos += 1
            operand = parse_primary()
            # NOT - все файлы минус те, что в операнде
            if operand:
                all_files = set()
                for files in index.values():
                    all_files.update(files)
                result = all_files - operand
                print(f"  NOT операция: все файлы {len(all_files)} - {len(operand)} = {len(result)}")
                return result
            else:
                # Если операнд пустой, NOT дает все файлы
                all_files = set()
                for files in index.values():
                    all_files.update(files)
                print(f"  NOT операция с пустым операндом: все файлы {len(all_files)}")
                return all_files
        else:
            return parse_primary()
    
    def parse_and_expression():
        nonlocal pos
        result = parse_not_expression()
        
        while pos < len(tokens) and tokens[pos].upper() == 'AND':
            pos += 1
            right = parse_not_expression()
            old_size = len(result)
            result = result & right
            print(f"  AND операция: {old_size} & {len(right)} = {len(result)}")
        
        return result
    
    def parse_or_expression():
        nonlocal pos
        result = parse_and_expression()
        
        while pos < len(tokens) and tokens[pos].upper() == 'OR':
            pos += 1
            right = parse_and_expression()
            old_size = len(result)
            result = result | right
            print(f"  OR операция: {old_size} | {len(right)} = {len(result)}")
        
        return result
    
    pos = 0
    try:
        result = parse_or_expression()
        if pos < len(tokens):
            raise ValueError(f"Лишние токены после разбора: {tokens[pos:]}")
        return result
    except Exception as e:
        print(f"Ошибка парсинга на позиции {pos}: {e}")
        raise

def boolean_search(query):
    """Основная функция для выполнения Boolean поиска"""
    try:
        # Токенизируем запрос
        tokens = tokenize_query(query)
        print(f"Токены запроса: {tokens}")
        
        # Парсим и выполняем запрос
        result_set = parse_expression(tokens)
        
        # Преобразуем в список и сортируем
        result = sorted(list(result_set))
        
        return result
    except Exception as e:
        print(f"Ошибка при обработке запроса: {e}")
        import traceback
        traceback.print_exc()
        return []

def display_results(result):
    """Отображает результаты поиска"""
    if result:
        print(f"\nНайдено файлов: {len(result)}")
        print("Результаты поиска:")
        for i, filename in enumerate(result[:10], 1):
            print(f"{i}. {filename}")
        if len(result) > 10:
            print(f"... и еще {len(result) - 10}")
    else:
        print("\nНичего не найдено")

# Тестирование

query1 = "(NOT (дата) AND корректный) or красиво"
print(f"Запрос: {query1}")

result1 = boolean_search(query1)
display_results(result1)

