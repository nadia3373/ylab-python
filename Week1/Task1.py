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
        print("domain name = " + domain)
    else:
        print("Not a valid URL")


def domain_name(url):
    # Проверка, начинается ли строка с http(s)://, http(s)://www.
    url_start = "^\"?(https?:\/\/www\.|https?:\/\/|www\.)"
    match = re.search(url_start, url)
    # Если проверка пройдена, удалить проверяемую часть и получить доменное имя
    if match is not None:
        domain = re.sub(match.group(), '', url)
        domain = domain.split(".")[0]
        return domain
    # Если проверка не пройдена, сообщить, что ссылка в некорректном формате
    else:
        return 1

if __name__ == "__main__":
    main()
