Локал граф яндекс музыки MVP
---

Концепт:
- пользователь вводит имя исполнителя
- система ищет инфу по похожим исполнителям
- рекурсивно строит граф по похожим исполнителям от изначального родителя
- рисует красивишный график
- ?????
- PROFIIT!!!1111


Развитие:
- кеш на своей стороне (зачем парсить тех, кого уже находили)
- запросы по официальному апи я.музыки (мечты)
- другие источники схожих исполнителей (более лояльные по количеству реквестов в секунду)
- исследование общего графа музыки


## Usage

```
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ ./cli-run.py similar_graph 'Black Sabbath' 5
```

## TODO

- cache for all info
- shortcut for graph command
- unittest for search artist
- unittest for fetch similar