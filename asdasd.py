import json

# Открываем JSON-файл и загружаем его
with open('channel_posts (1).json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Заданный массив с идентификаторами
ids = [1302, 1266, 1161, 1033, 1002, 970, 954, 1519, 1522, 1319, 1229, 1216, 1202, 1522, 1451, 1330, 1319, 1282, 1229, 1201, 1522]
results = []
# Поиск совпадения по id
for item in data:
    if item['id'] in ids:
        # Извлечение текста до первой точки
        text = item['text']
        first_sentence = text.split('.')[0]

        # Поиск CVE в тексте
        cve_start = text.find('CVE-')
        cve = text[cve_start: text.find('`', cve_start)]
        result = {
            'id': item['id'],
            'first_sentence': first_sentence,
            'CVE': cve
        }
        results.append(result)

    # Вывод массива с результатами
print(results)


