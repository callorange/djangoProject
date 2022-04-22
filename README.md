# djangoProject

django를 이용해 rest api를 구현하는 프로젝트 입니다.

## 요약
샌드위치 제작 / 재료 등록 및 재고 관리 등을 rest api 로 구현하는것이 목표입니다.

## 폴더

### .secrets 폴더
SECRET_KEY를 분리용으로 별도 json파일을 로드합니다.\
개발 편의상 로컬 개발용 파일만 소스코드에 포함합니다. \
**실제 production 한경에서는 별도로 분리되어야 합니다.**
```text
# .gitignore 에서 해당 폴더내 production이 들어가는 파일 무시하도록 설정
# 다른 세팅을 사용할 경우 추가 필요
.secrets/**/*production*
```

### sandwich 폴더
django 소스코드 폴더입니다.


## Django

### 실행 환경 및 패키지
1. python 3.9.5
2. Django 3.2.13
3. djangorestframework 3.13.1
4. black 22.3.0

### settings.py 분리
차후 동작환경에 따라 설정이 달라지므로 settings.py를 패키지화 하여 분리되었습니다.\
현재는 개발용 설정인 developement.py만 있습니다.

### 패키지 설치
```shell
# .../sandwich/requirements.txt 이용
sandwich> pip install -r requiements.txt
```

### 슈퍼유저 등록
```shell
sandwich> python manage.py createsuperuser
...
```

### 실행
```shell
sandwich> python manage.py runserver
# 혹은
sandwich> python manage.py runserver --settings=config.settings.developement
```
