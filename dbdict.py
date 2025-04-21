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
