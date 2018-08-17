# Локал граф яндекс музыки
[![Updates](https://pyup.io/repos/github/esemi/ya-local-graph/shield.svg)](https://pyup.io/repos/github/esemi/ya-local-graph/)

https://habrahabr.ru/company/semrush/blog/337216/

![Summary graph](https://habrastorage.org/web/413/ebc/8cd/413ebc8cd62745ae89c51b1b38dc58c9.png)


## Концепт:

- [x] выкачиваем всех исполнителей одного жанра
- [x] выкачиваем похожих исполнителей
- [x] исследуем полученный граф
- [x] рисуем красивую картинку и пишем статью



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
