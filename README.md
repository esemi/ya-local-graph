Локал граф яндекс музыки
---

Концепт:
- выкачиваем всех исполнителей одного жанра
- выкачиваем похожих исполнителей
- исследуем полученный граф


## TODO
- result img
- link to habrapost
- remove imgs from data


## Usage

```
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ pip install -r requirements.txt

$ ./cli-run.py artists_crawler rock 0
$ ./cli-run.py artists_crawler rusrock 0
$ ./cli-run.py artists_crawler ukrrock 0
$ ./cli-run.py artists_crawler rock-n-roll 0
$ ./cli-run.py artists_crawler prog-rock 0
$ ./cli-run.py artists_crawler post-rock 0
$ ./cli-run.py artists_crawler new-wave 0

$ ./cli-run.py artists_crawler metal 0
$ ./cli-run.py artists_crawler classicmetal 0
$ ./cli-run.py artists_crawler progmetal 0
$ ./cli-run.py artists_crawler Numetal 0
$ ./cli-run.py artists_crawler epicmetal 0
$ ./cli-run.py artists_crawler folkmetal 0
$ ./cli-run.py artists_crawler extrememetal 0

$ ./cli-run.py similar_crawler rusrock,rock,ukrrock,rock-n-roll,prog-rock,post-rock,new-wave,metal,classicmetal,progmetal,Numetal,epicmetal,folkmetal,extrememetal

$ ./cli-run.py graph_export
$ ./cli-run.py graph_plot
```
