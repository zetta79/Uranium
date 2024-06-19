from Get_dictionary_Michael import Get_DF_from_Dictionary, Get_Small_Dictionary_from_Excel, select_excel_files, Get_ALL_Dictionary_from_Excel
from Multilingual_e5_Vlad import get_words_from_multilingual_e5_base
from Multilingual_Alex import get_words_from_multilingual_bert

#выбираем файлы
path=select_excel_files()
print(path)
#получаем словарь с заголовками
s=Get_Small_Dictionary_from_Excel(path)
print(s)
#получаем датафрейм из словаря
test_texts=Get_DF_from_Dictionary(s)
print(test_texts)
request='скважина'
#In[]
#получаем ответ в виле списка заголовков [list]
answer= get_words_from_multilingual_e5_base(test_texts,3,request) 
new_list = [item[0] for item in answer]
answer=new_list
print(answer)
 #In[]
 #Пример использования
# #получаем ответ в виде списка заголовков [list]
# answer= get_words_from_multilingual_bert(test_texts,3,request)
# #итоговый список 
# print(answer)
# Удаление значений из словаря
#In[]
# Удаление значений из малого словаря
for key in s.keys():
    s[key] = [value for value in s[key] if value in answer]
print(s)
#In[]
#получаем весь словарь
s_big=Get_ALL_Dictionary_from_Excel(path)
print(s_big)

#In[]
#Вычитаем из всего словаря 
# Удаление лишних ключей
for outer_key in s_big:
    s_big[outer_key] = {k: v for k, v in s_big[outer_key].items() if k in answer}
print('Отформатированный список:',s_big)
#In[]
#Вычитание из большого словаря маленького
s_big=Get_ALL_Dictionary_from_Excel(path)
# Получаем путь к файлу и лист
file_path = list(s.keys())[0]

# Получаем список допустимых столбцов из первого словаря
valid_columns = s[file_path]

# Отфильтровываем столбцы второго словаря
filtered_data = {key: value for key, value in s_big[file_path].items() if key in valid_columns}

# Обновляем второй словарь
filtered_dict2 = {file_path: filtered_data}

# Печатаем результат
print('Отформатированный список:',filtered_dict2)