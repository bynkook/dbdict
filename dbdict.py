'''
#프로그램 설명
dict_work 내부에 있는 None 값을 dict_db, dict_word 에 주어져 있는 데이터를 사용하여 채워넣는 프로그램
dict_db, dict_work 의 'en' 키는 dict 의 key(텍스트값)에 대응하는 영어 설명문
dict_db, dict_work 의 'ko' 키는 dict 의 key(텍스트값)에 대응하는 한국어 설명문

#작동 방법
dict_work 의 key 를 읽는다. 'en' key 와 'ko' key 의 value 중 어느 하나라도 None 이 있으면 아래 1, 2 의 작업을 한다.
1. 그 key 가 dict_db 의 key 와 일치되는 매칭이 있으면 dict_work 의 value 를 업데이트 한다.
2. dict_db 의 key 와 일치되는 매칭이 없으면, key 를 seperator 들을 이용해서 split 하여 list1 에 임시로 저장한다.
그 list 의 각각의 값에 매칭되는 key 를 dict_word 에서 찾게되면, list2 에 'en' key의 value 를 append, list3 에는 'ko' key의 value 를 append 한다.  만약 dict_word 에서 매칭되는 key 가 없으면 'None' 을 append 한다.
list2의 값들을 textjoin 하여 eng_name 에 저장. list3의 값들을 textjoin 하여 kor_name 에 저장.  이때 textjoin은 space(공백)으로 한다.
만약 keep_key_format = False 라면, list1의 값을 사용해서 textjoin 하여 new_key에 저장한다.  이때 textjoin 은 '_'로 한다.  key 값을 new_key 로 replace 한다.
keep_key_format = True 라면, dict_work 의 key 값을 유지한다.
'en' key의 value 를 eng_name 으로 업데이트 한다. 'ko' key의 value 를 kor_name 으로 업데이트 한다.
이 과정을 반복해서 dict_work 의 모든 None 값이 제거된다.
dict_work 을 모두 print 하고 작업을 종료한다.
'''


import re
from typing import Dict, List, Optional, Tuple

def dict_update(
    dict_word: Dict[str, Dict[str, str]],
    dict_db: Dict[str, Dict[str, str]],
    dict_work: Dict[str, Dict[str, Optional[str]]],
    seperator: List[str],
    keep_key_format: bool = False
) -> Tuple[Dict[str, Dict[str, str]], List[Dict[str, str]]]:
    """
    dict_work 내부의 'en', 'ko' 값이 None인 항목을 dict_db 또는 dict_word를 활용해 채워넣는 함수.
    키가 변경된 경우에 대한 로그도 함께 반환.
    """
    combined_sep_pattern = '|'.join(map(re.escape, seperator))
    updated_dict = {}
    change_log = []

    for key, value in dict_work.items():
        if value['en'] is not None and value['ko'] is not None:
            updated_dict[key] = value
            continue

        if key in dict_db:
            updated_dict[key] = dict_db[key]
            continue

        tokens = re.split(combined_sep_pattern, key)
        eng_list, kor_list = [], []

        for token in tokens:
            word_info = dict_word.get(token)
            if word_info:
                eng_list.append(word_info['en'])
                kor_list.append(word_info['ko'])
            else:
                eng_list.append('None')
                kor_list.append('None')

        eng_name = ' '.join(eng_list)
        kor_name = ' '.join(kor_list)

        if keep_key_format:
            new_key = key
        else:
            new_key = '_'.join(tokens)
            if new_key != key:
                change_log.append({'old_key': key, 'new_key': new_key})

        updated_dict[new_key] = {'en': eng_name, 'ko': kor_name}

    return updated_dict, change_log

# 테스트 실행
dict_word = {
    'CONST':{'en':'construction', 'ko':'공사'},
    'AMT':{'en':'amount', 'ko':'물량'},
    'OUTS':{'en':'outsourcing', 'ko':'외주'},
    '01':{'en':'01', 'ko':'01'},
}

dict_db = {
    'CONST_PERD':{'en':'construction period', 'ko':'건설공기'},
    'MECH_INSTL':{'en':'mechanical installation', 'ko':'기계 설치'},
}

dict_work = {
    'CONST_PERD':{'en':None, 'ko':None},
    'MECH_DMTL':{'en':None, 'ko':None},
    'AMT_CONST-01':{'en':None, 'ko':None},
    'OUTS 01':{'en':None, 'ko':None},    
}

seperator = [' ', '-', '_', '*']
keep_key_format = False

# 실행
dict_work_updated, change_log = dict_update(dict_word, dict_db, dict_work, seperator, keep_key_format)

# 결과 출력
for k, v in dict_work_updated.items():
    print(f"{k}: {v}")

# 로그 저장
if change_log:
    with open("key_change_log.txt", "w", encoding="utf-8") as f:
        for log in change_log:
            f.write(f"{log['old_key']} -> {log['new_key']}\n")
    print("\n🔔 Key change log saved to 'key_change_log.txt'")