def main():
    # Получаем предложение от пользователя
    sentence = input("Введите предложение: ")



    words = sentence.split()
    search_words = ['DHCP']
    matches = []
    for word in words:
        if word in search_words:
            matches.append(word)

    if matches:
        print("Найденные совпадения:")
        for match in matches:
            print(match)
    else:
        print("Совпадений не найдено")


if __name__ == "__main__":
    main()
