# Dictionary Auto-Fill Utility

## 📌 개요

이 Python 스크립트는 `dict_work` 내 비어 있는(`None`) 값을 기준 데이터 사전(`dict_db`, `dict_word`)을 활용하여 자동으로 채워주는 유틸리티입니다. 키(Key) 기반의 매칭과 문자열 분해(split) 방식을 혼합하여 최대한 정확하게 텍스트 정보를 자동으로 보완할 수 있습니다.

## ⚙️ 작동 방식

### 입력 구조

- `dict_work`: 처리 대상 딕셔너리. 각 키는 `'en'`, `'ko'` 필드를 가지고 있으며, 일부 값이 `None`으로 비어 있음.
- `dict_db`: 우선 참조되는 기준 사전. 완전 매칭되는 키의 경우 우선적으로 사용.
- `dict_word`: 키 분해 시 사용되는 단어 단위 사전.

### 처리 로직

1. `dict_work` 내 각 항목에 대해 다음 조건을 검사:
   - `'en'` 또는 `'ko'` 값 중 하나라도 `None`인 경우

2. 아래 두 단계로 채움:
   - **1단계:** 키가 `dict_db`에 완전히 일치할 경우 해당 값을 바로 채움.
   - **2단계:** 일치하지 않을 경우, 다음 절차 수행:
     - 지정된 `separator` 목록(`[' ', '-', '_', '*']`)으로 키를 분할하여 `list1` 생성
     - `list1`의 각 요소가 `dict_word`에 존재하는지 검사
       - 존재 시 `list2`에 영어 설명(`'en'`), `list3`에 한국어 설명(`'ko'`) 추가
       - 없을 경우 `'None'`을 해당 리스트에 추가

3. 리스트 조합:
   - `list2`를 공백으로 조합하여 `eng_name` 생성
   - `list3`를 공백으로 조합하여 `kor_name` 생성

4. 키 포맷 변경 조건 (`keep_key_format`):
   - `False`일 경우: `list1`을 `'_'`으로 조합하여 새로운 키(`new_key`) 생성 후 `dict_work`의 키를 교체
   - `True`일 경우: 기존 키를 그대로 유지

5. 최종적으로:
   - `'en'` 값을 `eng_name`으로 업데이트
   - `'ko'` 값을 `kor_name`으로 업데이트

6. 모든 항목의 None 값이 처리될 때까지 위 과정을 반복

7. 최종적으로 업데이트된 `dict_work` 전체를 출력하고 종료

## 🧪 예시

```python
dict_word = {
    'CONST': {'en': 'construction', 'ko': '공사'},
    'AMT': {'en': 'amount', 'ko': '물량'},
}

dict_db = {
    'CONST_PERD': {'en': 'construction period', 'ko': '건설공기'},
}

dict_work = {
    'CONST_PERD': {'en': None, 'ko': None},
    'AMT_CONST-01': {'en': None, 'ko': None},
}

