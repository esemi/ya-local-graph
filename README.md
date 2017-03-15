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

$ ./cli-run.py artists_crawler rock 0
$ ./cli-run.py similar_crawler rusrock,rock,ukrrock,rock-n-roll,prog-rock,post-rock,new-wave,metal

$ ./cli-run.py graph_export
$ ./cli-run.py graph_plot
```
