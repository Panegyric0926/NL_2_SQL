from call_llm import call_llm
from prompt import natural_language_to_structure, structure_to_sql, sql_code_check, database_meta_information
import json
from call_database import insert_record, query_record

def natural_language_2_structure(user_input):
    prompt = natural_language_to_structure.replace('{database_meta_information}', database_meta_information).replace('{user_input}', user_input)
    answer, duration, _ = call_llm(prompt)
    position = answer.find('</think>')
    answer = answer[position + len('</think>'):].lstrip()
    answer = json.loads(answer)
    print(answer)
    print(duration)
    return answer, duration

def structure_2_sql(structure):
    prompt = structure_to_sql.replace('{database_meta_information}', database_meta_information).replace('{user_input}', structure)
    answer, duration, _ = call_llm(prompt)
    position = answer.find('</think>')
    answer = answer[position + len('</think>'):].lstrip()
    print(answer)
    print(duration)
    return answer, duration

def code_check(code):
    prompt = sql_code_check.replace('{database_meta_information}', database_meta_information).replace('{user_input}', code)
    answer, duration, _ = call_llm(prompt)
    position = answer.find('</think>')
    answer = answer[position + len('</think>'):].lstrip()
    print(answer)
    print(duration)
    return answer, duration

def main(user_input):
    answer,_ = natural_language_2_structure(user_input)
    relevance = answer['Relevance']
    if relevance == 'Irrelevant Query':
        print('Irrelevant Query')
        return
    tables = answer['Tables_Involved']
    tables = ', '.join(sorted(name.strip() for name in tables.split(',')))
    structure = answer['Structure']

    matches = query_record(user_input, structure, tables)
    if matches['match']:
        print(matches['Code'])
        return
    
    code,_ = structure_2_sql(structure)
    code_check(code)
    insert_record(user_input, tables, structure, code)


if __name__ == '__main__':
    user_input = 'Get the top 5 products that have the highest average rating.'
    main(user_input)