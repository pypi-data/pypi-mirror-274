__all__ = ['wiki']
import wikipedia
import pyttsx3

messages = {
    'ru': {
        'choose_language': 'Выберите язык для поиска и прочтения статьи (ru/en): ',
        'invalid_language': 'Пожалуйста, выберите корректный язык (ru/en).',
        'enter_query': 'Что вы хотите узнать?\n',
        'no_results': 'Ничего не найдено. Пожалуйста, попробуйте другой запрос.',
        'input_article_number': '\nВведите номер статьи для прочтения (или 0 для выхода): ',
        'invalid_article_number': 'Пожалуйста, введите корректный номер статьи.',
        'read_text': 'Хотите чтобы я вам прочитал текст?\n(yes/no) ',
        'http_error': 'Ошибка: превышено время ожидания запроса к Википедии.'
    },
    'en': {
        'choose_language': 'Choose language for searching and reading articles (ru/en): ',
        'invalid_language': 'Please choose a valid language (ru/en).',
        'enter_query': 'What do you want to know?\n',
        'no_results': 'Nothing found. Please try another query.',
        'input_article_number': '\nEnter the article number to read (or 0 to exit): ',
        'invalid_article_number': 'Please enter a valid article number.',
        'read_text': 'Do you want me to read the text?\n(yes/no) ',
        'http_error': 'Error: Wikipedia request timeout.'
    }
}


def wrap_text(text, line_length=150):
    wrapped_text = ""
    words = text.split()
    line = ""
    for word in words:
        if len(line) + len(word) <= line_length:
            line += word + " "
        else:
            wrapped_text += line.strip() + '\n'
            line = word + " "
    wrapped_text += line.strip()
    return wrapped_text


def get_article_summary(query, language):
    wikipedia.set_lang(language)
    try:
        summary = wikipedia.summary(query)
        return wrap_text(summary)
    except wikipedia.exceptions.DisambiguationError:
        return "Неоднозначный запрос. Пожалуйста, уточните ваш запрос."
    except wikipedia.exceptions.PageError:
        return "Страница не найдена. Пожалуйста, попробуйте другой запрос."


def my_swiki():
    """
    Запускает процесс чтения статей из Википедии.

    Эта функция запрашивает у пользователя язык и тему для поиска статей на Википедии.
    Затем она выводит результаты поиска и предлагает выбрать одну из статей для чтения.
    Если пользователь согласится, то функция прочитает краткое описание выбранной статьи.
    """
    pass
    language = input(messages['en']['choose_language']).lower()
    while language not in ('ru', 'en'):
        print(messages['en']['invalid_language'])
        language = input(messages['en']['choose_language']).lower()

    query = input(messages[language]['enter_query'])
    try:
        wikipedia.set_lang(language)
        search_results = wikipedia.search(query)
        if not search_results:
            print(messages[language]['no_results'])
            return
        article_idx = select_article(search_results, language)  # Passing language to select_article
        if article_idx is None:
            return
        print("\n")
        if input(messages[language]['read_text']).lower() == 'yes':
            say = pyttsx3.init()
            say.say(get_article_summary(search_results[article_idx], language))
            print("\n")
            print(get_article_summary(search_results[article_idx], language))
            say.runAndWait()
        else:
            print(get_article_summary(search_results[article_idx], language))
    except wikipedia.exceptions.HTTPTimeoutError:
        print(messages[language]['http_error'])

def select_article(search_results, language):  # Added 'language' as parameter
    for idx, result in enumerate(search_results, start=1):
        print(f"{idx}. {result}")
    while True:
        try:
            choice = int(input(messages[language]['input_article_number']))  # Using 'language' variable
            if choice == 0:
                return None
            elif choice < 1 or choice > len(search_results):
                print(messages[language]['invalid_article_number'])
            else:
                return choice - 1
        except ValueError:
            print("Please enter the number.")
