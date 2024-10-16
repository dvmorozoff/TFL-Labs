def membership(file_name, word):
    #print('Введите значение membership для:', word)
    resault = int(file.readline().strip())
    return resault
#b aba baa aaaba
def equivalence(file_name, matrix_in_mat):
    #print('Введите TRUE в случае эквивалентности и контрпример в противном:')
    counterexample = file.readline().strip()
    return counterexample

print('Введите название файла с тестовыми данными с расширением:')
file_name = input()
#file_name = 'ab.txt'
with open(file_name, 'r') as file:
    e = ''  # Возможность задать epsilon по-разному
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
        check_word = membership(file_name, word)  # true or False
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
                        prefixes.append(new_word)
                        check_new_word = membership(file_name, new_word)
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
                        prefixes.append(new_word)
                        check_new_word = membership(file_name, new_word)
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
    matrix_in_mat = [['', ''] for i in range(count_upper)]
    upper_prefixes = list(class_table.keys())
    #Заполнение таблицы, которую переводят в МАТ
    for number_of_up_pref in range(count_upper):
        matrix_in_mat[number_of_up_pref][0] = upper_prefixes[number_of_up_pref]
        if (class_table[upper_prefixes[number_of_up_pref]][0] == 'T'):
            matrix_in_mat[number_of_up_pref][1] = 1
        else:
            matrix_in_mat[number_of_up_pref][1] = 0
    previous_count_suf = 1
    count_elems_in_table = count_upper - 1
    counterexample = equivalence(file_name, matrix_in_mat)
    while counterexample != 'TRUE':
        #Добавление новых суффиксов
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
                    check_word = membership(file_name, word)
                    count_of_lines += 1
                    print(upper_prefixes[number_of_up_pref], suffixes[number_of_suf], ':', check_word, ':', count_of_lines)
                    table_row = class_table[upper_prefixes[number_of_up_pref]][0]
                    #Добавление элемента в таблицу для МАТ'а
                    count_elems_in_table += 1
                    matrix_in_mat.append(['', ''])
                    matrix_in_mat[count_elems_in_table][0] = word
                    matrix_in_mat[count_elems_in_table][1] = check_word
                    delete_elems = []
                    #2 варианта в зависимости от результата membership
                    if check_word:
                        class_table[upper_prefixes[number_of_up_pref]][0] += 'T'
                        #Проверка каждого элемента из к. э.
                        count_new_word = 0
                        for number_elem_of_class_ec in range(1, len(class_table[upper_prefixes[number_of_up_pref]])):
                            new_word = class_table[upper_prefixes[number_of_up_pref]][number_elem_of_class_ec] + suffixes[number_of_suf]
                            prefix = class_table[upper_prefixes[number_of_up_pref]][number_elem_of_class_ec]
                            check_new_word = membership(file_name, new_word)
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
                                    for suffix_iterator in range(number_of_suf + 1):
                                        count_elems_in_table += 1
                                        matrix_in_mat.append(['', ''])
                                        matrix_in_mat[count_elems_in_table][0] = prefix + suffixes[suffix_iterator]
                                        table_row_string = class_table[prefix][0]
                                        if table_row_string[suffix_iterator] == 'T':
                                            matrix_in_mat[count_elems_in_table][1] = 1
                                        else:
                                            matrix_in_mat[count_elems_in_table][1] = 0
                                    #Расширение префиксов
                                    for symbol in range(1, len(alphabet)):
                                        new_prefix = prefix + alphabet[symbol]
                                        table_row_new_prefix = ''
                                        check_equal_new_pref = True
                                        for suffix_iterator_2 in range(number_of_suf + 1):
                                            new_word_for_prefix = new_prefix + suffixes[suffix_iterator_2]
                                            check_new_prefix = membership(file_name, new_word_for_prefix)
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
                                            for suffix_iterator in range(1, number_of_suf + 1):
                                                count_elems_in_table += 1
                                                matrix_in_mat.append(['', ''])
                                                matrix_in_mat[count_elems_in_table][0] = new_prefix + suffixes[suffix_iterator]
                                                if table_row_new_prefix[suffix_iterator] == 'T':
                                                    matrix_in_mat[count_elems_in_table][1] = 1
                                                else:
                                                    matrix_in_mat[count_elems_in_table][1] = 0
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
                            check_new_word = membership(file_name, new_word)
                            count_of_lines += 1
                            print(class_table[upper_prefixes[number_of_up_pref]][number_elem_of_class_ec], suffixes[number_of_suf], ':', check_new_word, ':', count_of_lines)
                            if check_new_word != check_word:
                                if count_new_word == 0:
                                    count_new_word = 1
                                    class_table[prefix] = [table_row + 'T']
                                    new_word_class = prefix
                                    delete_elems.append(new_word_class)
                                    upper_prefixes.append(prefix)
                                    for suffix_iterator in range(number_of_suf + 1):
                                        matrix_in_mat.append(['', ''])
                                        count_elems_in_table += 1
                                        matrix_in_mat[count_elems_in_table][0] = prefix + suffixes[suffix_iterator]
                                        table_row_string = class_table[prefix][0]
                                        if table_row_string[suffix_iterator] == 'T':
                                            matrix_in_mat[count_elems_in_table][1] = 1
                                        else:
                                            matrix_in_mat[count_elems_in_table][1] = 0
                                    #Расширение префиксов
                                    for symbol in range(1, len(alphabet)):
                                        new_prefix = prefix + alphabet[symbol]
                                        table_row_new_prefix = ''
                                        check_equal_new_pref = True
                                        for suffix_iterator_2 in range(number_of_suf + 1):
                                            new_word_for_prefix = new_prefix + suffixes[suffix_iterator_2]
                                            check_new_prefix = membership(file_name, new_word_for_prefix)
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
                                            for suffix_iterator in range(number_of_suf + 1):
                                                count_elems_in_table += 1
                                                matrix_in_mat.append(['', ''])
                                                matrix_in_mat[count_elems_in_table][0] = new_prefix + suffixes[suffix_iterator]
                                                if table_row_new_prefix[suffix_iterator] == 'T':
                                                    matrix_in_mat[count_elems_in_table][1] = 1
                                                else:
                                                    matrix_in_mat[count_elems_in_table][1] = 0
                                else:
                                    class_table[new_word_class].append(prefix)
                                    delete_elems.append(prefix)
                    for elem in range(len(delete_elems)):
                        class_table[upper_prefixes[number_of_up_pref]].remove(delete_elems[elem])
                    #if delete_flag == 1:
                    #    class_table[upper_prefixes[number_of_up_pref]].remove(new_word_class)
                    #    print('DELETE', new_word_class)
        previous_count_suf = len(suffixes)
        counterexample = equivalence(file_name, matrix_in_mat)

    print('---------------')
    for key, value in class_table.items():  # Вывод словаря (таблицы к. э)
        print(f'{key}: {value}')
    print('---------------')
    for row in matrix_in_mat: #Вывод таблицы для мата
        print("{:>5} {:>5}".format(*row))
    print('---------------')
    print('Суффиксы:', suffixes)