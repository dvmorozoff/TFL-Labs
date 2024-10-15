from unittest.mock import patch
import io

def membership(word):
    print('Введите значение membership для:', word)
    i = int(input())
    return i == 1

def equivalence(matrix_in_mat):
    print('Введите TRUE в случае эквивалентности и контрпример в противном:')
    counterexample = input()
    return counterexample

e = ''  # Возможность задать epsilon по-разному
alphabet = []
alphabet.append(e)
print("Введите символы алфавита в ряд без пробелов без epsilon:")
stringalphabet = input()
for i in range(len(stringalphabet)):
    alphabet.append(stringalphabet[i])

count_upper = 0  # Число префиксов в верхней таблице
count_lower = 0  # Число префиксов в нижней таблице
suffixes = [e]
prefixes = []
count_suffixes = 1
class_table = {
}

# first iteration
count_true = 0
count_false = 0
for number_elem_in_alph in range(len(alphabet)):
    word = alphabet[number_elem_in_alph] + suffixes[0]
    check_word = membership(word)  # true or False
    prefixes.append(word)
    if check_word == True:
        if count_true == 0:
            count_true = 1
            word_true = word
            class_table[word_true] = ['T'] #Нулевой эл-нт списка = строка таблицы к. э.
            count_upper += 1
            if (word_true != e):
                for number_of_other_symbol in range(1, len(alphabet)):
                    new_word = word_true + alphabet[number_of_other_symbol]
                    prefixes.append(new_word)
                    check_new_word = membership(new_word)
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
                for j in range(1, len(alphabet)):
                    new_word = word_true + alphabet[j]
                    prefixes.append(new_word)
                    check_new_word = membership(new_word)
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

count_elems_in_table = count_upper - 1
counterexample = equivalence(matrix_in_mat)
while counterexample != 'TRUE':
    previous_count_suf = count_suffixes
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
            count_suffixes += 1
    #Построение продолжения таблицы к. э.
    for number_of_suf in range(previous_count_suf, count_suffixes):
        for number_of_up_pref in range(len(upper_prefixes)):
            #for key, value in class_table.items():  # Вывод словаря
            #    print(f'{key}: {value}')
            word = upper_prefixes[number_of_up_pref] + suffixes[number_of_suf]
            check_word = membership(word)
            table_row = class_table[upper_prefixes[number_of_up_pref]][0]
            delete_flag = 0
            #Добавление элемента в таблицу для МАТ'а
            count_elems_in_table += 1
            matrix_in_mat.append(['', ''])
            matrix_in_mat[count_elems_in_table][0] = word
            matrix_in_mat[count_elems_in_table][1] = check_word
            #2 варианта в зависимости от результата membership
            if check_word == True:
                class_table[upper_prefixes[number_of_up_pref]][0] += 'T'
                #Проверка каждого элемента из к. э.
                for number_elem_of_class_ec in range(1, len(class_table[upper_prefixes[number_of_up_pref]])):
                    new_word = class_table[upper_prefixes[number_of_up_pref]][number_elem_of_class_ec] + suffixes[number_of_suf]
                    prefix = class_table[upper_prefixes[number_of_up_pref]][number_elem_of_class_ec]
                    check_new_word = membership(new_word)
                    count_new_word = 0
                    #Если элемент из к. э перестаёт быть его частью на этой итерации
                    if check_new_word != check_word:
                        if count_new_word == 0:
                            count_new_word = 1
                            class_table[prefix] = [table_row + 'F']
                            new_word_class = prefix
                            delete_flag = 1
                            upper_prefixes.append(prefix)
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
                            for symbol in range(len(alphabet)):
                                new_prefix = prefix + alphabet[sybmol]
                                #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        else:
                            class_table[new_word_class].append(prefix)
            else:
                #Если membership word = F, а не T
                class_table[upper_prefixes[number_of_up_pref]][0] += 'F'
                #Аналогичный прогон каждого эл-та из к. э.
                for number_elem_of_class_ec in range(1, len(class_table[upper_prefixes[number_of_up_pref]])):
                    new_word = class_table[upper_prefixes[number_of_up_pref]][number_elem_of_class_ec] + suffixes[j]
                    prefix = class_table[upper_prefixes[number_of_up_pref]][number_elem_of_class_ec]
                    check_new_word = membership(new_word)
                    count_new_word = 0
                    if check_new_word != check:
                        if count_new_word == 0:
                            count_new_word = 1
                            class_table[prefix] = [table_row + 'T']
                            new_word_class = prefix
                            delete_flag = 1
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
                        else:
                            class_table[prefix].append(prefix)
            if delete_flag == 1:
                class_table[upper_prefixes[number_of_up_pref]].remove(new_word_class)

    counterexample = equivalence(matrix_in_mat)

for key, value in class_table.items():  # Вывод словаря
    print(f'{key}: {value}')
#for row in matrix_in_mat: #Вывод таблицы для мата
#    print("{:>5} {:>5}".format(*row))
print(suffixes)