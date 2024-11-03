from flask import Flask, request, jsonify
import requests
from requests.packages import target

app = Flask(__name__)

payload = {"mode": "easy"}
response = requests.post('http://localhost:8080/generate', json=payload)

def membership(word):
    payload = {"word": word}
    response = requests.post('http://localhost:8080/checkWord', json=payload)
    #response = requests.post('http://localhost:8095/checkWord', json=payload)
    if response.status_code == 200:
        result = response.json()
        return result.get("response", None)
    else:
        return None

def equivalence(class_table, suffixes, сounterexamples):
    upper_prefixes = list(class_table.keys())
    upper_prefixes += сounterexamples
    main_prefixes = ' '.join(upper_prefixes)
    ssuffixes = ' '.join(suffixes)
    table = ''
    non_main_pref = []
    for key in class_table:
        non_main_pref.extend(class_table[key][1:])
    non_main_prefixes = ' '.join(non_main_pref)
    for count_pref in range(len(upper_prefixes)):
        for count_suf in range(len(suffixes)):
            word = upper_prefixes[count_pref] + suffixes[count_suf]
            check_word = membership(word)
            table = table + ' ' + str(check_word)
    main_prefixes = 'ε' + main_prefixes
    ssuffixes = 'ε' + ssuffixes
    if main_prefixes == ssuffixes and ssuffixes == 'ε':
        table = str(membership('ε'))
    payload = {
        "main_prefixes": main_prefixes,
        "non_main_prefixes": "",
        "suffixes": ssuffixes,
        "table": table
    }
    response = requests.post('http://localhost:8080/checkTable', json=payload)
    #response = requests.post('http://localhost:8095/checkTable', json=payload)
    print('Статус-код ответа:', response.status_code)
    print('Текст ответа:', response.text)
    if response.status_code == 200:
        result = response.json()
        response_value = result.get("response", None)
        type_value = result.get("type", None)
        print('_____________________________________')
        return response_value
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

#print('Введите название файла с тестовыми данными с расширением:')
#file_name = input()
file_name = '09.txt'
with open(file_name, 'r') as file:
    #e = 'ε'  # Возможность задать epsilon по-разному
    e = ''
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
        if word != 'ε':
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
    previous_count_suf = 1
    count_elems_in_table = count_upper - 1
    сounterexamples = []
    counterexample = equivalence(class_table, suffixes, сounterexamples)
    while counterexample != 'true':
        #Добавление новых суффиксов
        for suffix_iterator in range(len(counterexample)):
            new_suffix = counterexample[len(counterexample) - suffix_iterator - 1:len(counterexample)]
            check_already_add_suf = True
            for number_of_suf in range(len(suffixes)):
                if new_suffix == suffixes[number_of_suf]:
                    check_already_add_suf = False
                    break
            if check_already_add_suf:
                suffixes.append(new_suffix)
        for count_pref1 in range(len(upper_prefixes), -1, -1):
            for count_pref2 in range(count_pref1 + 1, len(upper_prefixes)):
                key_to_move = upper_prefixes[count_pref1]
                target_key = upper_prefixes[count_pref2]
                if key_to_move == prev_counterexample or key_to_move == counterexample:
                    key_to_move, target_key = target_key, key_to_move
                if key_to_move in class_table and target_key in class_table:
                    table_row1 = class_table[key_to_move][0]
                    table_row2 = class_table[target_key][0]
                    if table_row1 == table_row2:
                        class_table[target_key].extend(filter(lambda x: x != class_table[key_to_move][0], class_table[key_to_move]))
                        class_table[target_key].append(key_to_move)
                        del class_table[key_to_move]
                        upper_prefixes = list(class_table.keys())
                        break
        print('----------------------')
        for key, value in class_table.items():  # Вывод словаря
            print(f'{key}: {value}')
        print('----------------------')
        #Построение продолжения таблицы к. э.
        for number_of_suf in range(previous_count_suf, len(suffixes)):
            for number_of_up_pref in range(len(upper_prefixes)):
                if (len(class_table[upper_prefixes[number_of_up_pref]][0]) < number_of_suf):
                    word = upper_prefixes[number_of_up_pref] + suffixes[number_of_suf]
                    word = word.replace('ε', '')
                    check_word = membership(word)
                    count_of_lines += 1
                    print(upper_prefixes[number_of_up_pref], suffixes[number_of_suf], ':', check_word, ':', count_of_lines)
                    table_row = class_table[upper_prefixes[number_of_up_pref]][0]
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
                                            if (table_row_new_prefix[:number_of_suf] == class_table[upper_prefixes[prefix_iterator]][0]) or (table_row_new_prefix[:number_of_suf-1] == class_table[upper_prefixes[prefix_iterator]][0]):
                                            #if (table_row_new_prefix == class_table[upper_prefixes[prefix_iterator]][0]) or (table_row_new_prefix[:-1] == class_table[upper_prefixes[prefix_iterator]][0]):
                                                class_table[upper_prefixes[prefix_iterator]].append(new_prefix)
                                                check_equal_new_pref = False
                                        if check_equal_new_pref:
                                            class_table[new_prefix] = [table_row_new_prefix]
                                            upper_prefixes.append(new_prefix)
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
                                            if (table_row_new_prefix[:number_of_suf] == class_table[upper_prefixes[prefix_iterator]][0]) or (table_row_new_prefix[:number_of_suf - 1] == class_table[upper_prefixes[prefix_iterator]][0]):
                                            #if (table_row_new_prefix == class_table[upper_prefixes[prefix_iterator]][0]) or (table_row_new_prefix[:-1] == class_table[upper_prefixes[prefix_iterator]][0]):
                                                class_table[upper_prefixes[prefix_iterator]].append(new_prefix)
                                                check_equal_new_pref = False
                                        if check_equal_new_pref:
                                            class_table[new_prefix] = [table_row_new_prefix]
                                            upper_prefixes.append(new_prefix)

                                else:
                                    class_table[new_word_class].append(prefix)
                                    delete_elems.append(prefix)
                    for elem in range(len(delete_elems)):
                        class_table[upper_prefixes[number_of_up_pref]].remove(delete_elems[elem])
                    #if delete_flag == 1:
                    #    class_table[upper_prefixes[number_of_up_pref]].remove(new_word_class)
                    #    print('DELETE', new_word_class)
        table_row = ''
        #Добавление контрпримера, как префикса
        for suffix_iterator in range(1, len(suffixes)):
            new_prefix = counterexample
            word = new_prefix + suffixes[suffix_iterator]
            check_word = membership(word)
            if check_word:
                table_row += 'T'
            else:
                table_row += 'F'
        class_table[new_prefix] = [table_row]
        сounterexamples.append(new_prefix)

        upper_prefixes = list(class_table.keys())
        previous_count_suf = len(suffixes)
        prev_counterexample = counterexample
        counterexample = equivalence(class_table, suffixes, сounterexamples)

    print('---------------')
    for key, value in class_table.items():  # Вывод словаря (таблицы к. э)
        print(f'{key}: {value}')
    print('---------------')
    #for row in matrix_in_mat: #Вывод таблицы для мата
    #    print("{:>5} {:>5} {:>5}".format(*row))
    print('---------------')
    print('Суффиксы:', suffixes)
