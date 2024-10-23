from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

payload = {"mode": "easy"}
response = requests.post('http://localhost:8080/generate', json=payload)

def membership(word):
    payload = {"word": word}
    response = requests.post('http://localhost:8080/checkWord', json=payload)
    if response.status_code == 200:
        result = response.json()
        return result.get("response", None)
    else:
        return None

def equivalence(class_table, suffixes):
    upper_prefixes = list(class_table.keys())
    main_prefixes = ' '.join(upper_prefixes)
    ssuffixes = ' '.join(suffixes)
    table = ''
    lower_prefixes = ''
    for count_pref in range(len(upper_prefixes)):
        for count_low_pref in range(len(class_table[upper_prefixes[count_pref]])):
            if count_low_pref != 0:
                lower_prefixes = lower_prefixes + ' ' + class_table[upper_prefixes[count_pref]][count_low_pref]

    for count_pref in range(len(upper_prefixes)):
        for count_suf in range(len(suffixes)):
            word = prefixes[count_pref] + suffixes[count_suf]
            #word = word.replace('ε', '')
            table = table + ' ' + str(membership(word))
    if main_prefixes == '':
        main_prefixes = 'ε '
    if main_prefixes[0] != 'ε':
        main_prefixes = 'ε ' + main_prefixes[1:]
    if ssuffixes == ' ':
        ssuffixes = 'ε'
    print('______________________')
    print('suffixes:', ssuffixes)
    print('prefixes:', main_prefixes)
    print(table)
    #print('low_pref:', lower_prefixes)
    payload = {
        "main_prefixes": main_prefixes,
        "non_main_prefixes": " ",  # Пустой объект
        "suffixes": ssuffixes,  # Элемент e
        "table": table
    }
    response = requests.post('http://localhost:8080/checkTable', json=payload)
    print('Статус-код ответа:', response.status_code)
    print('Текст ответа:', response.text)
    if response.status_code == 200:
        result = response.json()
        response_value = result.get("response", None)
        type_value = result.get("type", None)
        print('_____________________________________')
        print('type_value:', type_value, response_value)
        if type_value is True:
            return response_value
        elif type_value is False:
            return response_value
        elif type_value is None:
            return 'true'
        else:
            print('Неизвестное значение type')
            return None
    else:
        print('Ошибка эквивалентность')
        return None

'''def equivalence(file_name, matrix_in_mat):
    main_prefixes = ' '.join(row[0] for row in matrix_in_mat)
    table = ' '.join(str(row[1]) for row in matrix_in_mat)
    suffixes = ' '.join(str(row[2]) for row in matrix_in_mat)
    #print(main_prefixes)
    #print(suffixes)
    #print(table)
    payload = {
        "main_prefixes": main_prefixes,
        "non_main_prefixes": "",  # Пустой объект
        "suffixes": suffixes,  # Элемент e
        "table": table
    }
    response = requests.post('http://localhost:8080/checkTable', json=payload)
    print('Статус-код ответа:', response.status_code)
    print('Текст ответа:', response.text)
    if response.status_code == 200:
        result = response.json()
        response_value = result.get("response", None)
        type_value = result.get("type", None)
        print('_____________________________________')
        print('type_value:', type_value, response_value)
        if type_value is True:
            return response_value
        elif type_value is False:
            return response_value
        elif type_value is None:
            return 'true'
        else:
            print('Неизвестное значение type')
            return None
    else:
        print('Ошибка эквивалентность')
        return None
'''
#print('Введите название файла с тестовыми данными с расширением:')
#file_name = input()
file_name = '092.txt'
with open(file_name, 'r') as file:
    e = 'ε'  # Возможность задать epsilon по-разному
    #e = ' '
    alphabet = []
    alphabet.append(e)
    stringalphabet = file.readline().strip()
    for i in range(len(stringalphabet)):
        alphabet.append(stringalphabet[i])
    count_of_lines = 2
    count_upper = 0  # Число префиксов в верхней таблице
    count_lower = 0  # Число префиксов в нижней таблице
    suffixes = [e]
    prefixes = []
    class_table = {
    }

    # first iteration
    count_true = 0
    count_false = 0
    for number_elem_in_alph in range(len(alphabet)):
        word = alphabet[number_elem_in_alph] + suffixes[0]
        if word == 'εε':
            word = 'ε'
        word = word.replace('ε', '')
        check_word = membership(word)  # true or False
        count_of_lines += 1
        print(alphabet[number_elem_in_alph], suffixes[0], ':', check_word, ':', count_of_lines)
        prefixes.append(word)
        if check_word:
            if count_true == 0:
                count_true = 1
                word_true = word
                class_table[word_true] = ['T'] #Нулевой эл-нт списка = строка таблицы к. э.
                count_upper += 1
                if (word_true != e):
                    for number_of_other_symbol in range(1, len(alphabet)):
                        new_word = word_true + alphabet[number_of_other_symbol]
                        new_word = new_word.replace('ε', '')
                        prefixes.append(new_word)
                        check_new_word = membership(new_word)
                        count_of_lines += 1
                        print(word_true, alphabet[number_of_other_symbol], ':', check_new_word, ':', count_of_lines)
                        if check_new_word == check_word:
                            class_table[word_true].append(new_word)
                            count_lower += 1
                        else:
                            if count_false != 0:
                                class_table[word_false].append(new_word)
                                count_lower += 1
                            else:
                                count_false = 1
                                word_false = new_word
                                class_table[word_false] = ['F']  # Нулевой эл-нт списка = строка таблицы к. э.
                                count_upper += 1
            else:
                class_table[word_true].append(word)
                count_lower += 1
                if (word_true != e):
                    for number_of_other_symbol in range(1, len(alphabet)):
                        new_word = word_true + alphabet[number_of_other_symbol]
                        new_word = new_word.replace('ε', '')
                        prefixes.append(new_word)
                        check_new_word = membership(new_word)
                        count_of_lines += 1
                        print(word_true, alphabet[number_of_other_symbol], ':', check_new_word, ':', count_of_lines)
                        if check_new_word == check_word:
                            class_table[word_true].append(new_word)
                            count_lower += 1
                        else:
                            if count_false != 0:
                                class_table[word_false].append(new_word)
                                count_lower += 1
                            else:
                                count_false = 1
                                word_false = new_word
                                class_table[word_false] = ['F']  # Нулевой эл-нт списка = строка таблицы к. э.
                                count_upper += 1
        else:
            if count_false == 0:
                count_false = 1
                word_false = word
                class_table[word_false] = ['F'] #Нулевой эл-нт списка = строка таблицы к. э.
                count_upper += 1
            else:
                class_table[word_false].append(word)
                count_lower += 1
    #--------------------------------------------------------------------
    matrix_in_mat = [['', '', ''] for i in range(count_upper)]
    upper_prefixes = list(class_table.keys())
    #Заполнение таблицы, которую переводят в МАТ
    '''for number_of_up_pref in range(count_upper):
        matrix_in_mat[number_of_up_pref][0] = upper_prefixes[number_of_up_pref]
        if (class_table[upper_prefixes[number_of_up_pref]][0] == 'T'):
            matrix_in_mat[number_of_up_pref][1] = 1
        else:
            matrix_in_mat[number_of_up_pref][1] = 0
        matrix_in_mat[number_of_up_pref][2] = ' '''''
    previous_count_suf = 1
    count_elems_in_table = count_upper - 1
    counterexample = equivalence(class_table, suffixes)
    while counterexample != 'true':
        #Добавление новых суффиксов
        #for row in matrix_in_mat:  # Вывод таблицы для мата
        #    print("{:>5} {:>5}".format(*row))
        #print(counterexample)
        for suffix_iterator in range(len(counterexample)):
            new_suffix = counterexample[len(counterexample) - suffix_iterator - 1:len(counterexample)]
            check_already_add = True
            for number_of_suf in range(len(suffixes)):
                if new_suffix == suffixes[number_of_suf]:
                    check_already_add = False
                    break
            if check_already_add:
                suffixes.append(new_suffix)
        #Построение продолжения таблицы к. э.
        for number_of_suf in range(previous_count_suf, len(suffixes)):
            for number_of_up_pref in range(len(upper_prefixes)):
                if (len(class_table[upper_prefixes[number_of_up_pref]][0]) <= number_of_suf):
                    #print('----------------------')
                    #for key, value in class_table.items():  # Вывод словаря
                    #    print(f'{key}: {value}')
                    #print('----------------------')
                    word = upper_prefixes[number_of_up_pref] + suffixes[number_of_suf]
                    word = word.replace('ε', '')
                    check_word = membership(word)
                    count_of_lines += 1
                    print(upper_prefixes[number_of_up_pref], suffixes[number_of_suf], ':', check_word, ':', count_of_lines)
                    table_row = class_table[upper_prefixes[number_of_up_pref]][0]
                    #Добавление элемента в таблицу для МАТ'а
                    count_elems_in_table += 1
                    '''matrix_in_mat.append(['', '', ''])
                    matrix_in_mat[count_elems_in_table][0] = upper_prefixes[number_of_up_pref]
                    matrix_in_mat[count_elems_in_table][1] = check_word
                    matrix_in_mat[count_elems_in_table][2] = suffixes[number_of_suf]'''
                    delete_elems = []
                    #2 варианта в зависимости от результата membership
                    if check_word:
                        class_table[upper_prefixes[number_of_up_pref]][0] += 'T'
                        #Проверка каждого элемента из к. э.
                        count_new_word = 0
                        for number_elem_of_class_ec in range(1, len(class_table[upper_prefixes[number_of_up_pref]])):
                            new_word = class_table[upper_prefixes[number_of_up_pref]][number_elem_of_class_ec] + suffixes[number_of_suf]
                            prefix = class_table[upper_prefixes[number_of_up_pref]][number_elem_of_class_ec]
                            new_word = new_word.replace('ε', '')
                            check_new_word = membership(new_word)
                            count_of_lines += 1
                            print(class_table[upper_prefixes[number_of_up_pref]][number_elem_of_class_ec], suffixes[number_of_suf], ':', check_new_word, ':', count_of_lines)
                            #Если элемент из к. э перестаёт быть его частью на этой итерации
                            if check_new_word != check_word:
                                if count_new_word == 0:
                                    count_new_word = 1
                                    class_table[prefix] = [table_row + 'F']
                                    new_word_class = prefix
                                    delete_elems.append(new_word_class)
                                    upper_prefixes.append(prefix)
                                    #class_table[upper_prefixes[number_of_up_pref]].remove(new_word_class)
                                    #Добавление новых элементов таблицы для МАТ'а
                                    #с учётом появления нового префикса
                                    '''for suffix_iterator in range(number_of_suf + 1):
                                        count_elems_in_table += 1
                                        matrix_in_mat.append(['', '', ''])
                                        matrix_in_mat[count_elems_in_table][0] = prefix
                                        matrix_in_mat[count_elems_in_table][2] = suffixes[suffix_iterator]
                                        table_row_string = class_table[prefix][0]
                                        if table_row_string[suffix_iterator] == 'T':
                                            matrix_in_mat[count_elems_in_table][1] = 1
                                        else:
                                            matrix_in_mat[count_elems_in_table][1] = 0'''
                                    #Расширение префиксов
                                    for symbol in range(1, len(alphabet)):
                                        new_prefix = prefix + alphabet[symbol]
                                        table_row_new_prefix = ''
                                        check_equal_new_pref = True
                                        for suffix_iterator_2 in range(number_of_suf + 1):
                                            new_word_for_prefix = new_prefix + suffixes[suffix_iterator_2]
                                            new_word_for_prefix = new_word_for_prefix.replace('ε', '')
                                            check_new_prefix = membership(new_word_for_prefix)
                                            count_of_lines += 1
                                            print(new_prefix, suffixes[suffix_iterator_2], ':', check_new_prefix, ':', count_of_lines)
                                            if check_new_prefix:
                                                table_row_new_prefix += 'T'
                                            else:
                                                table_row_new_prefix += 'F'
                                        for prefix_iterator in range(len(upper_prefixes)):
                                            if (table_row_new_prefix == class_table[upper_prefixes[prefix_iterator]][0]) or (table_row_new_prefix[:-1] == class_table[upper_prefixes[prefix_iterator]][0]):
                                                class_table[upper_prefixes[prefix_iterator]].append(new_prefix)
                                                check_equal_new_pref = False
                                        if check_equal_new_pref:
                                            class_table[new_prefix] = [table_row_new_prefix]
                                            upper_prefixes.append(new_prefix)
                                            '''for suffix_iterator in range(1, number_of_suf + 1):
                                                count_elems_in_table += 1
                                                matrix_in_mat.append(['', '', ''])
                                                matrix_in_mat[count_elems_in_table][0] = new_prefix
                                                matrix_in_mat[count_elems_in_table][2] = suffixes[suffix_iterator]
                                                if table_row_new_prefix[suffix_iterator] == 'T':
                                                    matrix_in_mat[count_elems_in_table][1] = 1
                                                else:
                                                    matrix_in_mat[count_elems_in_table][1] = 0'''
                                else:
                                    class_table[new_word_class].append(prefix)
                                    delete_elems.append(prefix)
                    else:
                        #Если membership word = F, а не T
                        class_table[upper_prefixes[number_of_up_pref]][0] += 'F'
                        #Аналогичный прогон каждого эл-та из к. э.
                        count_new_word = 0
                        for number_elem_of_class_ec in range(1, len(class_table[upper_prefixes[number_of_up_pref]])):
                            new_word = class_table[upper_prefixes[number_of_up_pref]][number_elem_of_class_ec] + suffixes[number_of_suf]
                            prefix = class_table[upper_prefixes[number_of_up_pref]][number_elem_of_class_ec]
                            new_word = new_word.replace('ε', '')
                            check_new_word = membership(new_word)
                            count_of_lines += 1
                            print(class_table[upper_prefixes[number_of_up_pref]][number_elem_of_class_ec], suffixes[number_of_suf], ':', check_new_word, ':', count_of_lines)
                            if check_new_word != check_word:
                                if count_new_word == 0:
                                    count_new_word = 1
                                    class_table[prefix] = [table_row + 'T']
                                    new_word_class = prefix
                                    delete_elems.append(new_word_class)
                                    upper_prefixes.append(prefix)
                                    '''for suffix_iterator in range(number_of_suf + 1):
                                        matrix_in_mat.append(['', '', ''])
                                        count_elems_in_table += 1
                                        matrix_in_mat[count_elems_in_table][0] = prefix
                                        matrix_in_mat[count_elems_in_table][2] = suffixes[suffix_iterator]
                                        table_row_string = class_table[prefix][0]
                                        if table_row_string[suffix_iterator] == 'T':
                                            matrix_in_mat[count_elems_in_table][1] = 1
                                        else:
                                            matrix_in_mat[count_elems_in_table][1] = 0'''
                                    #Расширение префиксов
                                    for symbol in range(1, len(alphabet)):
                                        new_prefix = prefix + alphabet[symbol]
                                        table_row_new_prefix = ''
                                        check_equal_new_pref = True
                                        for suffix_iterator_2 in range(number_of_suf + 1):
                                            new_word_for_prefix = new_prefix + suffixes[suffix_iterator_2]
                                            new_word_for_prefix = new_word_for_prefix.replace('ε', '')
                                            check_new_prefix = membership(new_word_for_prefix)
                                            count_of_lines += 1
                                            print(new_prefix, suffixes[suffix_iterator_2], ':', check_new_prefix, ':', count_of_lines)
                                            if check_new_prefix:
                                                table_row_new_prefix += 'T'
                                            else:
                                                table_row_new_prefix += 'F'
                                        for prefix_iterator in range(len(upper_prefixes)):
                                            if (table_row_new_prefix == class_table[upper_prefixes[prefix_iterator]][0]) or (table_row_new_prefix[:-1] == class_table[upper_prefixes[prefix_iterator]][0]):
                                                class_table[upper_prefixes[prefix_iterator]].append(new_prefix)
                                                check_equal_new_pref = False
                                        if check_equal_new_pref:
                                            class_table[new_prefix] = [table_row_new_prefix]
                                            upper_prefixes.append(new_prefix)
                                            '''for suffix_iterator in range(number_of_suf + 1):
                                                count_elems_in_table += 1
                                                matrix_in_mat.append(['', '', ''])
                                                matrix_in_mat[count_elems_in_table][0] = new_prefix
                                                matrix_in_mat[count_elems_in_table][2] = suffixes[suffix_iterator]
                                                if table_row_new_prefix[suffix_iterator] == 'T':
                                                    matrix_in_mat[count_elems_in_table][1] = 1
                                                else:
                                                    matrix_in_mat[count_elems_in_table][1] = 0'''
                                else:
                                    class_table[new_word_class].append(prefix)
                                    delete_elems.append(prefix)
                    for elem in range(len(delete_elems)):
                        class_table[upper_prefixes[number_of_up_pref]].remove(delete_elems[elem])
                    #if delete_flag == 1:
                    #    class_table[upper_prefixes[number_of_up_pref]].remove(new_word_class)
                    #    print('DELETE', new_word_class)
        previous_count_suf = len(suffixes)
        counterexample = equivalence(class_table, suffixes)

    print('---------------')
    for key, value in class_table.items():  # Вывод словаря (таблицы к. э)
        print(f'{key}: {value}')
    print('---------------')
    #for row in matrix_in_mat: #Вывод таблицы для мата
    #    print("{:>5} {:>5} {:>5}".format(*row))
    print('---------------')
    print('Суффиксы:', suffixes)
