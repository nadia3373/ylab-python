# Написать метод domain_name, который вернет домен из url адреса:

import re


def main():
    # Для проверки
    assert domain_name("http://google.com") == "google"
    assert domain_name("http://google.co.jp") == "google"
    assert domain_name("www.xakep.ru") == "xakep"
    assert domain_name("https://youtube.com") == "youtube"

    # Получение ввода от пользователя
    url = input("url = ")

    domain = domain_name(url)
    if not domain == 1:
        print("domain name = " + str(domain))
    else:
        print("Not a valid URL")


def domain_name(url):
    # Проверка, начинается ли строка с http(s)://, http(s)://www.
    url_start = "^\"?(https?:\/\/www\.|https?:\/\/|www\.)"
    match = re.search(url_start, url)
    # Если проверка пройдена, удалить проверяемую часть
    if match is not None:
        domain = re.sub(match.group(), '', url)
    else:
        domain = url
    # Проверить, есть ли в ссылке символы /
    if "/" in domain:
        domain = domain.split("/")
        domain = domain[0]
    domain = domain.split(".")
    temp = []
    # Для простых доменов
    if len(domain) == 2:
        return domain[0]
    else:
        temp = []
        # Для составных доменов удалить короткие элементы и перепроверить длину
        for i in range(len(domain)):
            if len(domain[i]) < 3:
                temp.append(domain[i])
        if temp:
            for i in range(len(temp)):
                domain.remove(temp[i])
        if len(domain) == 1:
            return domain[0]
        else:
            temp = []
            for i in range(len(domain)):
                if len(domain[i]) == 3:
                    temp.append(domain[i])
            if len(temp) > 1:
                return domain[0]
            else:
                return domain[len(domain) - 1]

if __name__ == "__main__":
    main()
