def membership(word):
    print('Введите значение membership для:', word)
    i = int(input())
    return i == 1

def equivalence(matrix_in_mat):
    print('Введите TRUE в случае эквивалентности и контрпример в противном:')
    counterexample = input()
    return counterexample

e = ''  # Возможность задать epsilon по-разному
#alphabet = [e, '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
alphabet = [e, 'a', 'b']
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
for i in range(len(alphabet)):
    word = alphabet[i] + suffixes[0]
    check = membership(word)  # true or False
    prefixes.append(word)
    if check == True:
        if count_true == 0:
            count_true = 1
            word_true = word
            class_table[word_true] = ['T'] #Нулевой эл-нт списка = строка таблицы к. э.
            count_upper += 1
            if (word_true != e):
                for j in range(1, len(alphabet)):
                    new_word = word_true + alphabet[j]
                    prefixes.append(new_word)
                    check2 = membership(new_word)
                    if check2 == check:
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
                    check2 = membership(new_word)
                    if check2 == check:
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

#for key, value in class_table.items(): #Вывод словаря
    #print(f'{key}: {value}')
#--------------------------------------------------------------------
matrix_in_mat = [['', ''] for i in range(count_upper)]
upper_prefixes = list(class_table.keys())

for i in range(count_upper):
    matrix_in_mat[i][0] = upper_prefixes[i]
    if (class_table[upper_prefixes[i]][0] == 'T'):
        matrix_in_mat[i][1] = 1
    else:
        matrix_in_mat[i][1] = 0
count_elems_in_table = count_upper - 1
counterexample = equivalence(matrix_in_mat)
while counterexample != 'TRUE':
    previous_count_suf = count_suffixes
    for i in range(len(counterexample)):
        new_suffix = counterexample[len(counterexample) - i - 1:len(counterexample)]
        check4 = True
        for k in range(len(suffixes)):
            if new_suffix == suffixes[k]:
                check4 = False
                break
        if check4:
            suffixes.append(new_suffix)
            count_suffixes += 1
    for j in range(previous_count_suf, count_suffixes):
        for i in range(len(upper_prefixes)):
            #for key, value in class_table.items():  # Вывод словаря
            #    print(f'{key}: {value}')

            word = upper_prefixes[i] + suffixes[j]
            check = membership(word)  # true or False
            table_row = class_table[upper_prefixes[i]][0]
            delete_flag = 0

            count_elems_in_table += 1
            matrix_in_mat.append(['', ''])
            matrix_in_mat[count_elems_in_table][0] = word
            matrix_in_mat[count_elems_in_table][1] = check

            if check == True:
                class_table[upper_prefixes[i]][0] += 'T'
                for k in range(1, len(class_table[upper_prefixes[i]])):
                    new_word = class_table[upper_prefixes[i]][k] + suffixes[j]
                    prefix = class_table[upper_prefixes[i]][k]
                    check2 = membership(new_word)
                    count_new_word = 0
                    if check2 != check:
                        if count_new_word == 0:
                            count_new_word = 1
                            class_table[prefix] = [table_row + 'F']
                            new_word_class = prefix
                            delete_flag = 1
                            upper_prefixes.append(prefix)
                            for g in range(j + 1):
                                count_elems_in_table += 1
                                matrix_in_mat.append(['', ''])
                                matrix_in_mat[count_elems_in_table][0] = prefix + suffixes[g]
                                table_row_string = class_table[prefix][0]
                                if table_row_string[g] == 'T':
                                    matrix_in_mat[count_elems_in_table][1] = 1
                                else:
                                    matrix_in_mat[count_elems_in_table][1] = 0
                        else:
                            class_table[new_word_class].append(prefix)
            else:
                class_table[upper_prefixes[i]][0] += 'F'
                for k in range(1, len(class_table[upper_prefixes[i]])):
                    new_word = class_table[upper_prefixes[i]][k] + suffixes[j]
                    prefix = class_table[upper_prefixes[i]][k]
                    check2 = membership(new_word)
                    count_new_word = 0
                    if check2 != check:
                        if count_new_word == 0:
                            count_new_word = 1
                            class_table[prefix] = [table_row + 'T']
                            new_word_class = prefix
                            delete_flag = 1
                            upper_prefixes.append(prefix)
                            for g in range(j + 1):
                                matrix_in_mat.append(['', ''])
                                count_elems_in_table += 1
                                matrix_in_mat[count_elems_in_table][0] = prefix + suffixes[g]
                                table_row_string = class_table[prefix][0]
                                if table_row_string[g] == 'T':
                                    matrix_in_mat[count_elems_in_table][1] = 1
                                else:
                                    matrix_in_mat[count_elems_in_table][1] = 0
                        else:
                            class_table[prefix].append(prefix)
            if delete_flag == 1:
                class_table[upper_prefixes[i]].remove(new_word_class)

    counterexample = equivalence(matrix_in_mat)

for key, value in class_table.items():  # Вывод словаря
    print(f'{key}: {value}')
#for row in matrix_in_mat: #Вывод таблицы для мата
#    print("{:>5} {:>5}".format(*row))
print(suffixes)