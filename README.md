# info-search-3

## Генерация индекса

### Запуск
Запустить index.py
### Результат
В результате построен инвертированный индекс лемм. Он содержит информацию о том, в каком файле содержится конкретная лемма.
Вот пример индекса: index = {'шенген': ['page_1.txt'], 'явиться': ['page_4.txt', 'page_17.txt']}
Индекс записывается в файл "index.json".

## Булев поиск
### Запуск 
Запустить search.py
### Результат
Запрос: (NOT (дата) AND корректный) or красиво

Токены запроса: ['(', 'NOT', '(', 'дата', ')', 'AND', 'корректный', ')', 'OR', 'красиво']

Лемма 'дата' найдена в файлах: {'page_38.txt', 'page_62.txt', 'page_66.txt', 'page_98.txt', 'page_79.txt', 'page_95.txt', 'page_55.txt', 'page_64.txt', 'page_67.txt', 'page_3.txt', 'page_25.txt', 'page_60.txt', 'page_61.txt', 'page_82.txt', 'page_57.txt', 'page_44.txt', 'page_94.txt', 'page_8.txt', 'page_7.txt', 'page_91.txt', 'page_50.txt', 'page_80.txt', 'page_88.txt', 'page_1.txt', 'page_56.txt', 'page_42.txt', 'page_22.txt', 'page_13.txt', 'page_47.txt', 'page_11.txt', 'page_58.txt', 'page_65.txt', 'page_26.txt', 'page_33.txt', 'page_89.txt', 'page_23.txt', 'page_40.txt', 'page_4.txt', 'page_35.txt', 'page_45.txt', 'page_73.txt', 'page_5.txt'}

NOT операция: все файлы 99 - 42 = 57

Лемма 'корректный' найдена в файлах: {'page_10.txt', 'page_19.txt', 'page_26.txt', 'page_41.txt', 'page_3.txt', 'page_31.txt', 'page_47.txt'}

AND операция: 57 & 7 = 4

Лемма 'красиво' найдена в файлах: {'page_40.txt', 'page_10.txt', 'page_84.txt'}

OR операция: 4 | 3 = 6

Найдено файлов: 6
Результаты поиска:
1. page_10.txt
2. page_19.txt
3. page_31.txt
4. page_40.txt
5. page_41.txt
6. page_84.txt

