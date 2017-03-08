Локал граф яндекс музыки
---

Концепт:
- выкачиваем всех исполнителей одного жанра
- выкачиваем похожих исполнителей
- исследуем полученный граф


## Usage

```
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ ./cli-run.py artists_crawler 'rock'
$ ./cli-run.py similar_crawler
$ ./cli-run.py graph_export
$ ./cli-run.py graph_plot
```
