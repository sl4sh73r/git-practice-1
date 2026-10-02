# Отчёт по практической работе № 1. Система контроля версий Git

Репозиторий: <https://github.com/sl4sh73r/git-practice-1>

## Цель работы

Освоить работу с системой контроля версий Git и сервисом GitHub: создание и клонирование репозитория, коммиты и обмен ими с удалённым репозиторием, ветвление, способы слияния (merge, squash, rebase), разрешение конфликтов, откат изменений, перенос коммитов (cherry-pick, rebase, патчи), а также индивидуальные задания: теги (вариант 1) и reflog (вариант 8).

## Описание проекта

В качестве учебного проекта разработан PulseWatch: система мониторинга доступности сервисов цифрового продукта. Для продуктовой команды доступность сервиса является бизнес-показателем: простой сайта, API или платежей означает потерянную выручку и отток пользователей.

PulseWatch читает журнал проверок доступности (checks.csv) и по каждому сервису считает долю успешных проверок, среднее время ответа и 95-й перцентиль, суммарное время простоя. Показатели сравниваются с целевым уровнем доступности (SLO), рассчитывается бюджет ошибок и скорость его расхода, формируются оповещения с уровнем критичности и каналом доставки.

Бюджет ошибок служит инструментом управления разработкой: пока он не исчерпан, команда выпускает новые функции; когда он расходуется быстрее нормы, приоритет переносится с новых функций на надёжность. Таким образом, отчёт PulseWatch даёт менеджеру продукта основание для решения о приоритетах релиза.

Состав проекта: monitor.py (отчёт), metrics.py (показатели), slo.py (SLO и бюджет ошибок), alerts.py (оповещения), services.py (каталог сервисов и ответственных команд), checks.csv (данные), тесты test_metrics.py и test_slo.py.

## Условия выполнения

Работа выполнена в Git 2.50.1 (macOS), удалённый репозиторий: https://github.com/sl4sh73r/git-practice-1. Работа трёх программистов имитируется тремя клонами одного репозитория: person1 (автор коммитов sl4sh73r), person2 и person3 (автор коммитов VadimKarmazin; в команде пока два человека, поэтому роль третьего разработчика исполняет второй участник). В листингах перед знаком $ указаны рабочий каталог и текущая ветвь; строки, начинающиеся с #, являются пояснениями. Ветвь main соответствует ветви master из текста задания.

## Общая часть

### 1. Создание удалённого репозитория и клонирование

Удалённый репозиторий создан на GitHub с описанием, затем клонирован на локальную машину. Каталог person1 является одновременно локальным репозиторием (подкаталог .git) и рабочим каталогом первого разработчика.

**Удалённый репозиторий с описанием создан на GitHub командой: gh repo create sl4sh73r/git-practice-1 --public --description "...". Проверяем его**

```console
~$ gh repo view sl4sh73r/git-practice-1 --json name,visibility,description,url
{"description":"Практическая работа № 1 (Git). PulseWatch: система мониторинга доступности сервисов цифрового продукта (SLO, бюджет ошибок, оповещения)","name":"git-practice-1","url":"https://github.com/sl4sh73r/git-practice-1","visibility":"PUBLIC"}
```

**Клонирование в локальный рабочий каталог person1**

```console
~$ git clone https://github.com/sl4sh73r/git-practice-1.git person1
Cloning into 'person1'...
warning: You appear to have cloned an empty repository.

person1 (main)$ git remote -v
origin	https://github.com/sl4sh73r/git-practice-1.git (fetch)
origin	https://github.com/sl4sh73r/git-practice-1.git (push)

person1 (main)$ git status
On branch main

No commits yet

nothing to commit (create/copy files and use "git add" to track)
```

**Результат.** Репозиторий доступен по адресу https://github.com/sl4sh73r/git-practice-1. Клон пустой, ветвь по умолчанию называется main (в задании она же master).

### 2. Приложение из трёх файлов, первый коммит и push

В person1 создана первая версия PulseWatch: monitor.py (точка входа, отчёт), metrics.py (расчёт показателей), checks.csv (журнал проверок доступности трёх сервисов: web, api, payments).

**Создаём приложение из трёх файлов: monitor.py, metrics.py, checks.csv**

```console
person1 (main)$ ls
checks.csv
metrics.py
monitor.py

person1 (main)$ head -5 checks.csv
timestamp,service,status,response_ms
2026-09-28T10:00,web,up,241
2026-09-28T10:00,api,up,99
2026-09-28T10:00,payments,up,320
2026-09-28T10:05,web,up,283

person1 (main)$ python3 monitor.py
PulseWatch v1.0: отчёт о доступности сервисов
сервис     доступность  ответ, мс
api            100.00%        104
payments        83.33%        317
web             91.67%        255

person1 (main)$ git status --short
?? checks.csv
?? metrics.py
?? monitor.py

person1 (main)$ git add monitor.py metrics.py checks.csv

person1 (main)$ git commit -m "Первый коммит: отчёт о доступности сервисов (3 файла)"
[main (root-commit) fe06f79] Первый коммит: отчёт о доступности сервисов (3 файла)
 3 files changed, 91 insertions(+)
 create mode 100644 checks.csv
 create mode 100644 metrics.py
 create mode 100644 monitor.py

person1 (main)$ git log --oneline
fe06f79 Первый коммит: отчёт о доступности сервисов (3 файла)
```

**Перенос коммита в удалённый репозиторий**

```console
person1 (main)$ git push -u origin main
To https://github.com/sl4sh73r/git-practice-1.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.

person1 (main)$ git status
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

**Результат.** Файлы прошли путь рабочий каталог → индекс (git add) → локальный репозиторий (git commit) → удалённый репозиторий (git push).

### 3. Второй рабочий каталог person2 и обмен изменениями

Репозиторий клонирован во второй каталог person2. Изменение сделано в person2, затем проверено, в какой момент оно становится видно в person1.

**Второй разработчик клонирует репозиторий в person2**

```console
~$ git clone https://github.com/sl4sh73r/git-practice-1.git person2
Cloning into 'person2'...

person2 (main)$ git log --oneline
fe06f79 Первый коммит: отчёт о доступности сервисов (3 файла)
```

**person2 добавляет в metrics.py новую функцию p95_response()**

```console
person2 (main)$ git diff
diff --git a/metrics.py b/metrics.py
index 60d106d..72f0dac 100644
--- a/metrics.py
+++ b/metrics.py
@@ -23,3 +23,10 @@ def avg_response(checks):
     if not times:
         return 0
     return sum(times) / len(times)
+
+
+def p95_response(checks):
+    times = sorted(int(c["response_ms"]) for c in checks if c["status"] == "up")
+    if not times:
+        return 0
+    return times[max(0, round(0.95 * len(times)) - 1)]

person2 (main)$ git add metrics.py

person2 (main)$ git commit -m "metrics: 95-й перцентиль времени ответа"
[main d6afcde] metrics: 95-й перцентиль времени ответа
 1 file changed, 7 insertions(+)

person2 (main)$ git status
On branch main
Your branch is ahead of 'origin/main' by 1 commit.
  (use "git push" to publish your local commits)

nothing to commit, working tree clean
```

**Проверяем person1: коммит существует только локально у person2, в person1 его нет**

```console
person1 (main)$ git fetch

person1 (main)$ git status
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean

person1 (main)$ git log --oneline
fe06f79 Первый коммит: отчёт о доступности сервисов (3 файла)

person1 (main)$ grep -c p95 metrics.py
0
```

**person2 выгружает коммит в удалённый репозиторий**

```console
person2 (main)$ git push
To https://github.com/sl4sh73r/git-practice-1.git
   fe06f79..d6afcde  main -> main
```

**person1 скачивает изменения и проверяет их**

```console
person1 (main)$ git fetch
From https://github.com/sl4sh73r/git-practice-1
   fe06f79..d6afcde  main       -> origin/main

person1 (main)$ git status
On branch main
Your branch is behind 'origin/main' by 1 commit, and can be fast-forwarded.
  (use "git pull" to update your local branch)

nothing to commit, working tree clean

person1 (main)$ git diff --stat main origin/main
 metrics.py | 7 +++++++
 1 file changed, 7 insertions(+)

person1 (main)$ git pull
Updating fe06f79..d6afcde
Fast-forward
 metrics.py | 7 +++++++
 1 file changed, 7 insertions(+)

person1 (main)$ git log --oneline
d6afcde metrics: 95-й перцентиль времени ответа
fe06f79 Первый коммит: отчёт о доступности сервисов (3 файла)

person1 (main)$ tail -6 metrics.py

def p95_response(checks):
    times = sorted(int(c["response_ms"]) for c in checks if c["status"] == "up")
    if not times:
        return 0
    return times[max(0, round(0.95 * len(times)) - 1)]
```

**Повтор цикла: person2 меняет другой файл (checks.csv, новая порция проверок)**

```console
person2 (main)$ git add checks.csv

person2 (main)$ git commit -m "checks: проверки за 11:00 и 11:05"
[main 67691d0] checks: проверки за 11:00 и 11:05
 1 file changed, 6 insertions(+)

person2 (main)$ git push
To https://github.com/sl4sh73r/git-practice-1.git
   d6afcde..67691d0  main -> main

person1 (main)$ git pull
From https://github.com/sl4sh73r/git-practice-1
   d6afcde..67691d0  main       -> origin/main
Updating d6afcde..67691d0
Fast-forward
 checks.csv | 6 ++++++
 1 file changed, 6 insertions(+)

person1 (main)$ git log --oneline
67691d0 checks: проверки за 11:00 и 11:05
d6afcde metrics: 95-й перцентиль времени ответа
fe06f79 Первый коммит: отчёт о доступности сервисов (3 файла)

person1 (main)$ python3 monitor.py
PulseWatch v1.0: отчёт о доступности сервисов
сервис     доступность  ответ, мс
api            100.00%        107
payments        78.57%        319
web             92.86%        253
```

**Результат.** Пока коммит не отправлен командой git push, он существует только в локальном репозитории person2: в person1 ни git fetch, ни git status его не показывают. После push команда git fetch сообщает, что ветвь отстаёт на один коммит, а git pull переносит изменение в рабочий каталог. Цикл повторён для второго файла (checks.csv).

### 4. Новая ветвь dev в person1

Для разработки новой функциональности (целевые уровни доступности и бюджет ошибок) создана ветвь dev, в ней добавлен новый файл и коммит, ветвь опубликована в удалённом репозитории.

**person1 создаёт ветвь dev и переключается на неё**

```console
person1 (main)$ git branch dev

person1 (main)$ git checkout dev
Switched to branch 'dev'

person1 (dev)$ git branch
* dev
  main
```

**Новый файл slo.py в ветви dev: целевые уровни доступности и бюджет ошибок**

```console
person1 (dev)$ git add slo.py

person1 (dev)$ git commit -m "dev: SLO сервисов и бюджет ошибок (slo.py)"
[dev 0125555] dev: SLO сервисов и бюджет ошибок (slo.py)
 1 file changed, 12 insertions(+)
 create mode 100644 slo.py

person1 (dev)$ git push -u origin dev
remote: 
remote: Create a pull request for 'dev' on GitHub by visiting:        
remote:      https://github.com/sl4sh73r/git-practice-1/pull/new/dev        
remote: 
To https://github.com/sl4sh73r/git-practice-1.git
 * [new branch]      dev -> dev
branch 'dev' set up to track 'origin/dev'.

person1 (dev)$ git branch -vv
* dev  0125555 [origin/dev] dev: SLO сервисов и бюджет ошибок (slo.py)
  main 67691d0 [origin/main] checks: проверки за 11:00 и 11:05
```

**Результат.** Ветвь dev существует локально и на сервере и связана с origin/dev; main при этом не изменился.

### 5. Ветвь dev2 в person2 и дополнение предыдущего коммита

person2 получает обновления, создаёт ветвь dev2 с новым файлом alerts.py, отправляет её на сервер, после чего вносит небольшую правку и добавляет её в предыдущий коммит командой git commit --amend.

**person2 получает обновления (в том числе новую ветвь dev)**

```console
person2 (main)$ git pull
From https://github.com/sl4sh73r/git-practice-1
 * [new branch]      dev        -> origin/dev
Already up to date.

person2 (main)$ git branch -a
* main
  remotes/origin/HEAD -> origin/main
  remotes/origin/dev
  remotes/origin/main
```

**Создаём ветвь dev2 и новый файл alerts.py (правила оповещений)**

```console
person2 (main)$ git checkout -b dev2
Switched to a new branch 'dev2'

person2 (dev2)$ git add alerts.py

person2 (dev2)$ git commit -m "dev2: оповещение о низкой доступности"
[dev2 bfbe91e] dev2: оповещение о низкой доступности
 1 file changed, 9 insertions(+)
 create mode 100644 alerts.py

person2 (dev2)$ git push -u origin dev2
remote: 
remote: Create a pull request for 'dev2' on GitHub by visiting:        
remote:      https://github.com/sl4sh73r/git-practice-1/pull/new/dev2        
remote: 
To https://github.com/sl4sh73r/git-practice-1.git
 * [new branch]      dev2 -> dev2
branch 'dev2' set up to track 'origin/dev2'.
```

**Небольшая правка в новом файле и добавление её в предыдущий коммит (amend)**

```console
person2 (dev2)$ git log --oneline -2
bfbe91e dev2: оповещение о низкой доступности
67691d0 checks: проверки за 11:00 и 11:05

person2 (dev2)$ git add alerts.py

person2 (dev2)$ git commit --amend --no-edit
[dev2 2925c08] dev2: оповещение о низкой доступности
 Date: Fri Oct 2 18:46:39 2026 +0300
 1 file changed, 18 insertions(+)
 create mode 100644 alerts.py

person2 (dev2)$ git log --oneline -2
2925c08 dev2: оповещение о низкой доступности
67691d0 checks: проверки за 11:00 и 11:05

person2 (dev2)$ git status
On branch dev2
Your branch and 'origin/dev2' have diverged,
and have 1 and 1 different commits each, respectively.
  (use "git pull" if you want to integrate the remote branch with yours)

nothing to commit, working tree clean
```

**Хэш коммита изменился, история разошлась с origin/dev2, обычный push будет отклонён**

```console
person2 (dev2)$ git push
To https://github.com/sl4sh73r/git-practice-1.git
 ! [rejected]        dev2 -> dev2 (non-fast-forward)
error: failed to push some refs to 'https://github.com/sl4sh73r/git-practice-1.git'
hint: Updates were rejected because the tip of your current branch is behind
hint: its remote counterpart. If you want to integrate the remote changes,
hint: use 'git pull' before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.

person2 (dev2)$ git push --force-with-lease
To https://github.com/sl4sh73r/git-practice-1.git
 + bfbe91e...2925c08 dev2 -> dev2 (forced update)

person2 (dev2)$ git status
On branch dev2
Your branch is up to date with 'origin/dev2'.

nothing to commit, working tree clean
```

**Результат.** amend не дописывает старый коммит, а создаёт новый с другим хэшем (bfbe91e → 2925c08). Так как старый коммит уже был на сервере, обычный push отклоняется и нужен git push --force-with-lease. Переписывать опубликованную историю можно только в собственной ветви.

### 6. Слияние ветвей: Merge, Squash, Rebase

Для каждого способа создана отдельная новая ветвь от одной и той же точки main, после чего ветви по очереди слиты в main.

```console
person1 (dev)$ git checkout main
Switched to branch 'main'
Your branch is up to date with 'origin/main'.
```

**Три новые ветви от одной точки main: под merge, squash и rebase**

**Ветвь feature-merge: два коммита (время простоя сервиса)**

```console
person1 (main)$ git checkout -b feature-merge main
Switched to a new branch 'feature-merge'

person1 (feature-merge)$ git commit -am "metrics: время простоя сервиса downtime_minutes"
[feature-merge e617134] metrics: время простоя сервиса downtime_minutes
 1 file changed, 4 insertions(+)

person1 (feature-merge)$ git commit -am "monitor: в отчёте колонки p95 и простой"
[feature-merge 437b360] monitor: в отчёте колонки p95 и простой
 1 file changed, 2 insertions(+), 1 deletion(-)
```

**Ветвь feature-squash: три мелких коммита, новый файл services.py**

```console
person1 (feature-merge)$ git checkout -b feature-squash main
Switched to a new branch 'feature-squash'

person1 (feature-squash)$ git add services.py

person1 (feature-squash)$ git commit -m "services: каталог сервисов (черновик)"
[feature-squash 7966347] services: каталог сервисов (черновик)
 1 file changed, 6 insertions(+)
 create mode 100644 services.py

person1 (feature-squash)$ git commit -am "services: добавлен сервис payments"
[feature-squash 617633c] services: добавлен сервис payments
 1 file changed, 1 insertion(+)

person1 (feature-squash)$ git commit -am "services: функция owner для поиска ответственной команды"
[feature-squash ec55c73] services: функция owner для поиска ответственной команды
 1 file changed, 5 insertions(+)
```

**Ветвь feature-rebase: два коммита с README.md**

```console
person1 (feature-squash)$ git checkout -b feature-rebase main
Switched to a new branch 'feature-rebase'

person1 (feature-rebase)$ git add README.md

person1 (feature-rebase)$ git commit -m "README: описание проекта"
[feature-rebase 2746194] README: описание проекта
 1 file changed, 3 insertions(+)
 create mode 100644 README.md

person1 (feature-rebase)$ git commit -am "README: раздел Запуск"
[feature-rebase bd940c9] README: раздел Запуск
 1 file changed, 6 insertions(+)

person1 (feature-rebase)$ git log --oneline --graph --all -12
* 437b360 monitor: в отчёте колонки p95 и простой
* e617134 metrics: время простоя сервиса downtime_minutes
| * bd940c9 README: раздел Запуск
| * 2746194 README: описание проекта
|/  
| * ec55c73 services: функция owner для поиска ответственной команды
| * 617633c services: добавлен сервис payments
| * 7966347 services: каталог сервисов (черновик)
|/  
| * 0125555 dev: SLO сервисов и бюджет ошибок (slo.py)
|/  
* 67691d0 checks: проверки за 11:00 и 11:05
* d6afcde metrics: 95-й перцентиль времени ответа
* fe06f79 Первый коммит: отчёт о доступности сервисов (3 файла)
```

**1. MERGE: обычное слияние с коммитом слияния (--no-ff)**

```console
person1 (feature-rebase)$ git checkout main
Switched to branch 'main'
Your branch is up to date with 'origin/main'.

person1 (main)$ git merge --no-ff feature-merge -m "Merge branch feature-merge: простой и p95 в отчёте"
Merge made by the 'ort' strategy.
 metrics.py | 4 ++++
 monitor.py | 3 ++-
 2 files changed, 6 insertions(+), 1 deletion(-)

person1 (main)$ git log --oneline --graph -6
*   05376ec Merge branch feature-merge: простой и p95 в отчёте
|\  
| * 437b360 monitor: в отчёте колонки p95 и простой
| * e617134 metrics: время простоя сервиса downtime_minutes
|/  
* 67691d0 checks: проверки за 11:00 и 11:05
* d6afcde metrics: 95-й перцентиль времени ответа
* fe06f79 Первый коммит: отчёт о доступности сервисов (3 файла)

person1 (main)$ python3 monitor.py
PulseWatch v1.0: отчёт о доступности сервисов
сервис     доступность  ответ, мс  p95, мс  простой, мин
api            100.00%        107      154             0
payments        78.57%        319      342            15
web             92.86%        253      280             5
```

**2. SQUASH: три коммита ветви превращаются в один коммит в main**

```console
person1 (main)$ git merge --squash feature-squash
Automatic merge went well; stopped before committing as requested
Squash commit -- not updating HEAD

person1 (main)$ git status --short
A  services.py

person1 (main)$ git commit -m "services: каталог сервисов и ответственных команд (squash ветви feature-squash)"
[main e9f919e] services: каталог сервисов и ответственных команд (squash ветви feature-squash)
 1 file changed, 12 insertions(+)
 create mode 100644 services.py

person1 (main)$ git log --oneline --graph -6
* e9f919e services: каталог сервисов и ответственных команд (squash ветви feature-squash)
*   05376ec Merge branch feature-merge: простой и p95 в отчёте
|\  
| * 437b360 monitor: в отчёте колонки p95 и простой
| * e617134 metrics: время простоя сервиса downtime_minutes
|/  
* 67691d0 checks: проверки за 11:00 и 11:05
* d6afcde metrics: 95-й перцентиль времени ответа
```

**После squash Git не считает ветвь слитой: обычное удаление -d отклоняется, нужно -D**

```console
person1 (main)$ git branch -d feature-squash
error: the branch 'feature-squash' is not fully merged
hint: If you are sure you want to delete it, run 'git branch -D feature-squash'
hint: Disable this message with "git config set advice.forceDeleteBranch false"

person1 (main)$ git branch -D feature-squash
Deleted branch feature-squash (was ec55c73).
```

**3. REBASE: перенос коммитов ветви на вершину main, затем fast-forward**

```console
person1 (main)$ git checkout feature-rebase
Switched to branch 'feature-rebase'

person1 (feature-rebase)$ git log --oneline -3
bd940c9 README: раздел Запуск
2746194 README: описание проекта
67691d0 checks: проверки за 11:00 и 11:05

person1 (feature-rebase)$ git rebase main
Rebasing (1/2)
Rebasing (2/2)
Successfully rebased and updated refs/heads/feature-rebase.

person1 (feature-rebase)$ git log --oneline -4
3b918ee README: раздел Запуск
71fd05b README: описание проекта
e9f919e services: каталог сервисов и ответственных команд (squash ветви feature-squash)
05376ec Merge branch feature-merge: простой и p95 в отчёте

person1 (feature-rebase)$ git checkout main
Switched to branch 'main'
Your branch is ahead of 'origin/main' by 4 commits.
  (use "git push" to publish your local commits)

person1 (main)$ git merge feature-rebase
Updating e9f919e..3b918ee
Fast-forward
 README.md | 9 +++++++++
 1 file changed, 9 insertions(+)
 create mode 100644 README.md

person1 (main)$ git log --oneline --graph -9
* 3b918ee README: раздел Запуск
* 71fd05b README: описание проекта
* e9f919e services: каталог сервисов и ответственных команд (squash ветви feature-squash)
*   05376ec Merge branch feature-merge: простой и p95 в отчёте
|\  
| * 437b360 monitor: в отчёте колонки p95 и простой
| * e617134 metrics: время простоя сервиса downtime_minutes
|/  
* 67691d0 checks: проверки за 11:00 и 11:05
* d6afcde metrics: 95-й перцентиль времени ответа
* fe06f79 Первый коммит: отчёт о доступности сервисов (3 файла)

person1 (main)$ git branch -d feature-merge feature-rebase
Deleted branch feature-merge (was 437b360).
Deleted branch feature-rebase (was 3b918ee).

person1 (main)$ git push
To https://github.com/sl4sh73r/git-practice-1.git
   67691d0..3b918ee  main -> main
```

**Результат.** Merge (--no-ff) сохраняет все коммиты ветви и добавляет коммит слияния, в графе видна развилка. Squash складывает три коммита ветви в один обычный коммит в main: история линейная, но связь с ветвью теряется, поэтому git branch -d считает ветвь неслитой. Rebase пересоздаёт коммиты ветви поверх вершины main (хэши меняются: 2746194 → 71fd05b), после чего слияние выполняется перемоткой fast-forward без коммита слияния.

### 7. Три разработчика и поочерёдное слияние ветвей в main

Создан третий каталог person3 с ветвью dev3. person3 меняет metrics.py в начале файла, person2 в dev2 меняет другой файл (checks.csv), person1 в ветви dev1 (продолжение dev) меняет тот же metrics.py, но в другом месте. Затем ветви по очереди сливаются в main (в задании master).

**Третий разработчик: клон person3 и ветвь dev3**

```console
~$ git clone https://github.com/sl4sh73r/git-practice-1.git person3
Cloning into 'person3'...

person3 (main)$ git checkout -b dev3
Switched to a new branch 'dev3'
```

**person3 меняет metrics.py в НАЧАЛЕ файла (docstring у load_checks и for_service)**

```console
person3 (dev3)$ git diff
diff --git a/metrics.py b/metrics.py
index 8fa0e3f..23ea52b 100644
--- a/metrics.py
+++ b/metrics.py
@@ -3,11 +3,13 @@ import csv
 
 
 def load_checks(path):
+    """Читает журнал проверок из CSV."""
     with open(path, newline="", encoding="utf-8") as f:
         return list(csv.DictReader(f))
 
 
 def for_service(checks, service):
+    """Проверки одного сервиса."""
     return [c for c in checks if c["service"] == service]
 
 

person3 (dev3)$ git commit -am "dev3: docstring для load_checks и for_service"
[dev3 0f3a541] dev3: docstring для load_checks и for_service
 1 file changed, 2 insertions(+)

person3 (dev3)$ git push -u origin dev3
remote: 
remote: Create a pull request for 'dev3' on GitHub by visiting:        
remote:      https://github.com/sl4sh73r/git-practice-1/pull/new/dev3        
remote: 
To https://github.com/sl4sh73r/git-practice-1.git
 * [new branch]      dev3 -> dev3
branch 'dev3' set up to track 'origin/dev3'.
```

**person2 в ветви dev2 меняет ДРУГОЙ файл (checks.csv, проверки за 11:10)**

```console
person2 (dev2)$ git checkout dev2
Already on 'dev2'
Your branch is up to date with 'origin/dev2'.

person2 (dev2)$ git diff --stat
 checks.csv | 3 +++
 1 file changed, 3 insertions(+)

person2 (dev2)$ git commit -am "dev2: проверки за 11:10"
[dev2 199192b] dev2: проверки за 11:10
 1 file changed, 3 insertions(+)

person2 (dev2)$ git push
To https://github.com/sl4sh73r/git-practice-1.git
   2925c08..199192b  dev2 -> dev2
```

**person1: ветвь dev1 (продолжение dev), тот же metrics.py, но ДРУГОЕ место (функция avg_response)**

```console
person1 (main)$ git checkout -b dev1 dev
Switched to a new branch 'dev1'

person1 (dev1)$ git diff
diff --git a/metrics.py b/metrics.py
index 72f0dac..828267c 100644
--- a/metrics.py
+++ b/metrics.py
@@ -22,7 +22,7 @@ def avg_response(checks):
     times = [int(c["response_ms"]) for c in checks if c["status"] == "up"]
     if not times:
         return 0
-    return sum(times) / len(times)
+    return round(sum(times) / len(times))
 
 
 def p95_response(checks):

person1 (dev1)$ git commit -am "dev1: среднее время ответа округляется до целых"
[dev1 99613f3] dev1: среднее время ответа округляется до целых
 1 file changed, 1 insertion(+), 1 deletion(-)

person1 (dev1)$ git push -u origin dev1
remote: 
remote: Create a pull request for 'dev1' on GitHub by visiting:        
remote:      https://github.com/sl4sh73r/git-practice-1/pull/new/dev1        
remote: 
To https://github.com/sl4sh73r/git-practice-1.git
 * [new branch]      dev1 -> dev1
branch 'dev1' set up to track 'origin/dev1'.
```

**Поочерёдное слияние ветвей dev1, dev2, dev3 в main**

```console
person1 (dev1)$ git checkout main
Switched to branch 'main'
Your branch is up to date with 'origin/main'.

person1 (main)$ git fetch
From https://github.com/sl4sh73r/git-practice-1
 * [new branch]      dev2       -> origin/dev2
 * [new branch]      dev3       -> origin/dev3

person1 (main)$ git branch -a
  dev
  dev1
* main
  remotes/origin/HEAD -> origin/main
  remotes/origin/dev
  remotes/origin/dev1
  remotes/origin/dev2
  remotes/origin/dev3
  remotes/origin/main
```

**1) dev1 -> main (в main попадают slo.py из dev и правка avg_response)**

```console
person1 (main)$ git merge --no-edit dev1
Auto-merging metrics.py
Merge made by the 'ort' strategy.
 metrics.py |  2 +-
 slo.py     | 12 ++++++++++++
 2 files changed, 13 insertions(+), 1 deletion(-)
 create mode 100644 slo.py
```

**2) dev2 -> main (alerts.py и новые строки checks.csv)**

```console
person1 (main)$ git merge --no-edit origin/dev2
Merge made by the 'ort' strategy.
 alerts.py  | 18 ++++++++++++++++++
 checks.csv |  3 +++
 2 files changed, 21 insertions(+)
 create mode 100644 alerts.py
```

**3) dev3 -> main (metrics.py менялся и в dev1, и в dev3, но в разных местах: автослияние)**

```console
person1 (main)$ git merge --no-edit origin/dev3
Auto-merging metrics.py
Merge made by the 'ort' strategy.
 metrics.py | 2 ++
 1 file changed, 2 insertions(+)

person1 (main)$ git log --oneline --graph -12
*   00976d4 Merge remote-tracking branch 'origin/dev3'
|\  
| * 0f3a541 dev3: docstring для load_checks и for_service
* |   f1da4da Merge remote-tracking branch 'origin/dev2'
|\ \  
| * | 199192b dev2: проверки за 11:10
| * | 2925c08 dev2: оповещение о низкой доступности
* | |   f3fa4c7 Merge branch 'dev1'
|\ \ \  
| |_|/  
|/| |   
| * | 99613f3 dev1: среднее время ответа округляется до целых
| * | 0125555 dev: SLO сервисов и бюджет ошибок (slo.py)
| |/  
* | 3b918ee README: раздел Запуск
* | 71fd05b README: описание проекта
* | e9f919e services: каталог сервисов и ответственных команд (squash ветви feature-squash)
* |   05376ec Merge branch feature-merge: простой и p95 в отчёте
|\ \  
| |/  
|/|   

person1 (main)$ sed -n "5,14p" metrics.py
def load_checks(path):
    """Читает журнал проверок из CSV."""
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def for_service(checks, service):
    """Проверки одного сервиса."""
    return [c for c in checks if c["service"] == service]

person1 (main)$ python3 monitor.py
PulseWatch v1.0: отчёт о доступности сервисов
сервис     доступность  ответ, мс  p95, мс  простой, мин
api            100.00%        108      154             0
payments        80.00%        317      342            15
web             93.33%        254      280             5

person1 (main)$ git push
To https://github.com/sl4sh73r/git-practice-1.git
   3b918ee..00976d4  main -> main
```

**Результат.** Все три слияния прошли автоматически. Git сливает построчно: правки одного файла в разных местах (dev1 и dev3 в metrics.py) объединяются без участия человека, о чём сообщает строка Auto-merging.

### 8. Конфликты слияния и способы их разрешения

Чтобы получить настоящий конфликт, одна и та же строка изменена в двух ветвях. Рассмотрены четыре способа действий.

**person3 в dev3 (не зная о правке dev1) меняет ТУ ЖЕ строку в avg_response**

```console
person3 (dev3)$ git commit -am "dev3: среднее время ответа с точностью до 0.1 мс"
[dev3 cf00619] dev3: среднее время ответа с точностью до 0.1 мс
 1 file changed, 1 insertion(+), 1 deletion(-)

person3 (dev3)$ git push
To https://github.com/sl4sh73r/git-practice-1.git
   0f3a541..cf00619  dev3 -> dev3
```

**Конфликт 1: одна и та же строка изменена в main (из dev1) и в dev3**

```console
person1 (main)$ git fetch
From https://github.com/sl4sh73r/git-practice-1
   0f3a541..cf00619  dev3       -> origin/dev3

person1 (main)$ git merge --no-edit origin/dev3
Auto-merging metrics.py
CONFLICT (content): Merge conflict in metrics.py
Automatic merge failed; fix conflicts and then commit the result.

person1 (main)$ git status
On branch main
Your branch is up to date with 'origin/main'.

You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)

Unmerged paths:
  (use "git add <file>..." to mark resolution)
	both modified:   metrics.py

no changes added to commit (use "git add" and/or "git commit -a")

person1 (main)$ git diff
diff --cc metrics.py
index 4860300,d3b8b2b..0000000
--- a/metrics.py
+++ b/metrics.py
@@@ -24,7 -24,7 +24,11 @@@ def avg_response(checks)
      times = [int(c["response_ms"]) for c in checks if c["status"] == "up"]
      if not times:
          return 0
++<<<<<<< HEAD
 +    return round(sum(times) / len(times))
++=======
+     return round(sum(times) / len(times), 1)
++>>>>>>> origin/dev3
  
  
  def p95_response(checks):
```

**Способ А: отказаться от слияния и вернуть состояние до него**

```console
person1 (main)$ git merge --abort

person1 (main)$ git status --short --branch
## main...origin/main
```

**Способ Б: ручное разрешение. Повторяем слияние, правим файл, убирая маркеры <<<<<<< ======= >>>>>>>**

```console
person1 (main)$ git merge --no-edit origin/dev3
Auto-merging metrics.py
CONFLICT (content): Merge conflict in metrics.py
Automatic merge failed; fix conflicts and then commit the result.

person1 (main)$ grep -n -B4 "return round" metrics.py
23-def avg_response(checks):
24-    times = [int(c["response_ms"]) for c in checks if c["status"] == "up"]
25-    if not times:
26-        return 0
27:    return round(sum(times) / len(times), 1)

person1 (main)$ git add metrics.py

person1 (main)$ git status --short --branch
## main...origin/main
M  metrics.py

person1 (main)$ git commit -m "Merge origin/dev3: конфликт в avg_response разрешён вручную"
[main 3d5f8cf] Merge origin/dev3: конфликт в avg_response разрешён вручную

person1 (main)$ git log --oneline --graph -5
*   3d5f8cf Merge origin/dev3: конфликт в avg_response разрешён вручную
|\  
| * cf00619 dev3: среднее время ответа с точностью до 0.1 мс
* | 00976d4 Merge remote-tracking branch 'origin/dev3'
|\| 
| * 0f3a541 dev3: docstring для load_checks и for_service
* |   f1da4da Merge remote-tracking branch 'origin/dev2'
|\ \  
```

**Конфликт 2: строка VERSION в monitor.py изменена и в main, и в dev2**

```console
person1 (main)$ git commit -am "monitor: версия 1.1"
[main 59127e9] monitor: версия 1.1
 1 file changed, 1 insertion(+), 1 deletion(-)

person2 (dev2)$ git commit -am "dev2: версия 1.2"
[dev2 6754112] dev2: версия 1.2
 1 file changed, 1 insertion(+), 1 deletion(-)

person2 (dev2)$ git push
To https://github.com/sl4sh73r/git-practice-1.git
   199192b..6754112  dev2 -> dev2

person1 (main)$ git fetch
From https://github.com/sl4sh73r/git-practice-1
   199192b..6754112  dev2       -> origin/dev2

person1 (main)$ git merge --no-edit origin/dev2
Auto-merging monitor.py
CONFLICT (content): Merge conflict in monitor.py
Automatic merge failed; fix conflicts and then commit the result.

person1 (main)$ git diff --name-only --diff-filter=U
monitor.py

person1 (main)$ grep -n -A4 "<<<<<<<" monitor.py
6:<<<<<<< HEAD
7-VERSION = "1.1"
8-=======
9-VERSION = "1.2"
10->>>>>>> origin/dev2
```

**Способ В: взять файл целиком из одной из сторон (--ours = наша ветвь, --theirs = вливаемая)**

```console
person1 (main)$ git checkout --theirs monitor.py
Updated 1 path from the index

person1 (main)$ grep -n VERSION monitor.py | head -1
6:VERSION = "1.2"

person1 (main)$ git add monitor.py

person1 (main)$ git commit -m "Merge origin/dev2: в конфликте VERSION принята версия dev2 (--theirs)"
[main eab9a36] Merge origin/dev2: в конфликте VERSION принята версия dev2 (--theirs)

person1 (main)$ git log --oneline --graph -7
*   eab9a36 Merge origin/dev2: в конфликте VERSION принята версия dev2 (--theirs)
|\  
| * 6754112 dev2: версия 1.2
* | 59127e9 monitor: версия 1.1
* |   3d5f8cf Merge origin/dev3: конфликт в avg_response разрешён вручную
|\ \  
| * | cf00619 dev3: среднее время ответа с точностью до 0.1 мс
* | | 00976d4 Merge remote-tracking branch 'origin/dev3'
|\| | 
| * | 0f3a541 dev3: docstring для load_checks и for_service
```

**Проверка после способа В: checkout --theirs берёт файл ЦЕЛИКОМ из dev2, поэтому пропали и неконфликтные правки main (колонки p95 и простой)**

```console
person1 (main)$ git diff 59127e9 HEAD -- monitor.py
diff --git a/monitor.py b/monitor.py
index 66ca426..2b787da 100644
--- a/monitor.py
+++ b/monitor.py
@@ -3,19 +3,18 @@ import sys
 
 import metrics
 
-VERSION = "1.1"
+VERSION = "1.2"
 
 
 def build_report(checks):
     lines = [
         f"PulseWatch v{VERSION}: отчёт о доступности сервисов",
-        f"{'сервис':<10}{'доступность':>12}{'ответ, мс':>11}{'p95, мс':>9}{'простой, мин':>14}",
+        f"{'сервис':<10}{'доступность':>12}{'ответ, мс':>11}",
     ]
     for name in sorted({c["service"] for c in checks}):
         rows = metrics.for_service(checks, name)
         lines.append(
             f"{name:<10}{metrics.availability(rows):>11.2f}%{metrics.avg_response(rows):>11.0f}"
-            f"{metrics.p95_response(rows):>9}{metrics.downtime_minutes(rows):>14}"
         )
     return "\n".join(lines)
 

person1 (main)$ python3 monitor.py
PulseWatch v1.2: отчёт о доступности сервисов
сервис     доступность  ответ, мс
api            100.00%        108
payments        80.00%        317
web             93.33%        254
```

**Исправляем: возвращаем потерянные строки отдельным коммитом**

```console
person1 (main)$ git commit -am "monitor: возвращены колонки p95 и простой, потерянные при checkout --theirs"
[main 1df263d] monitor: возвращены колонки p95 и простой, потерянные при checkout --theirs
 1 file changed, 2 insertions(+), 1 deletion(-)

person1 (main)$ python3 monitor.py
PulseWatch v1.2: отчёт о доступности сервисов
сервис     доступность  ответ, мс  p95, мс  простой, мин
api            100.00%        108      154             0
payments        80.00%        317      342            15
web             93.33%        254      280             5
```

**Способ Г (для сравнения, на временной ветви): стратегия -X theirs берёт чужую сторону только в конфликтных фрагментах, остальное сливает как обычно**

```console
person1 (main)$ git checkout -q -b demo-x-theirs 59127e9

person1 (demo-x-theirs)$ git merge -X theirs --no-edit origin/dev2
Auto-merging monitor.py
Merge made by the 'ort' strategy.
 monitor.py | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)

person1 (demo-x-theirs)$ grep -n -e VERSION -e p95 monitor.py
6:VERSION = "1.2"
11:        f"PulseWatch v{VERSION}: отчёт о доступности сервисов",
12:        f"{'сервис':<10}{'доступность':>12}{'ответ, мс':>11}{'p95, мс':>9}{'простой, мин':>14}",
18:            f"{metrics.p95_response(rows):>9}{metrics.downtime_minutes(rows):>14}"

person1 (demo-x-theirs)$ git checkout -q main

person1 (main)$ git branch -D demo-x-theirs
Deleted branch demo-x-theirs (was 73313ff).

person1 (main)$ git push
To https://github.com/sl4sh73r/git-practice-1.git
   00976d4..1df263d  main -> main
```

**Результат.** Способы: А) git merge --abort отменяет слияние целиком; Б) ручная правка файла между маркерами, затем git add и git commit; В) git checkout --ours/--theirs берёт файл целиком с одной стороны; Г) git merge -X ours/-X theirs выбирает сторону только в конфликтных фрагментах. Практический вывод: способ В заменил файл полностью и вместе с конфликтной строкой убрал неконфликтные правки main (колонки p95 и простоя в отчёте), их пришлось вернуть отдельным коммитом. Способ Г этого недостатка лишён. Также доступен графический инструмент git mergetool.

### 9. Поиск коммита через git log и откат git reset --hard

В main сделан заведомо неудачный коммит (не отправленный на сервер): доступность стала считаться долей, а не процентами. Через git log найден хэш предыдущего коммита, git log -p показывает содержимое изменений.

**Делаем в main неудачный (не отправленный на сервер) коммит**

```console
person1 (main)$ git commit -am "Неудачный эксперимент с availability"
[main 19c72c6] Неудачный эксперимент с availability
 1 file changed, 1 insertion(+), 1 deletion(-)

person1 (main)$ python3 monitor.py
PulseWatch v1.2: отчёт о доступности сервисов
сервис     доступность  ответ, мс  p95, мс  простой, мин
api              1.00%        108      154             0
payments         0.80%        317      342            15
web              0.93%        254      280             5
```

**Ищем хэш нужного коммита через git log, смотрим содержимое коммитов через git log -p**

```console
person1 (main)$ git log --oneline -4
19c72c6 Неудачный эксперимент с availability
1df263d monitor: возвращены колонки p95 и простой, потерянные при checkout --theirs
eab9a36 Merge origin/dev2: в конфликте VERSION принята версия dev2 (--theirs)
59127e9 monitor: версия 1.1

person1 (main)$ git log -p -1
commit 19c72c60579bbbdaf052c4261404a679324bc23b
Author: sl4sh73r <87204613+sl4sh73r@users.noreply.github.com>
Date:   Fri Oct 2 18:48:20 2026 +0300

    Неудачный эксперимент с availability

diff --git a/metrics.py b/metrics.py
index d3b8b2b..9011d79 100644
--- a/metrics.py
+++ b/metrics.py
@@ -17,7 +17,7 @@ def availability(checks):
     if not checks:
         return 0.0
     ok = sum(1 for c in checks if c["status"] == "up")
-    return 100 * ok / len(checks)
+    return ok / len(checks)  # эксперимент: доля вместо процентов
 
 
 def avg_response(checks):
```

**Откат к выбранному коммиту 1df263d**

```console
person1 (main)$ git reset --hard 1df263d
HEAD is now at 1df263d monitor: возвращены колонки p95 и простой, потерянные при checkout --theirs

person1 (main)$ git log --oneline -3
1df263d monitor: возвращены колонки p95 и простой, потерянные при checkout --theirs
eab9a36 Merge origin/dev2: в конфликте VERSION принята версия dev2 (--theirs)
59127e9 monitor: версия 1.1

person1 (main)$ python3 monitor.py
PulseWatch v1.2: отчёт о доступности сервисов
сервис     доступность  ответ, мс  p95, мс  простой, мин
api            100.00%        108      154             0
payments        80.00%        317      342            15
web             93.33%        254      280             5

person1 (main)$ git status --short --branch
## main...origin/main
```

**Результат.** git reset --hard переместил ветвь на выбранный коммит и привёл индекс и рабочий каталог в его состояние; неудачный коммит исчез из истории ветви, отчёт снова верный. Команду безопасно применять только к неопубликованным коммитам.

### 10. Перенос отдельного коммита: git cherry-pick

В dev2 сделаны два новых коммита, в main нужен только один из них (уровень критичности оповещения).

**person2 делает в dev2 два новых коммита**

```console
person2 (dev2)$ git commit -am "dev2: уровень критичности оповещения"
[dev2 5e341d5] dev2: уровень критичности оповещения
 1 file changed, 5 insertions(+)

person2 (dev2)$ git commit -am "dev2: каналы доставки оповещений"
[dev2 a894d1f] dev2: каналы доставки оповещений
 1 file changed, 7 insertions(+)

person2 (dev2)$ git push
To https://github.com/sl4sh73r/git-practice-1.git
   6754112..a894d1f  dev2 -> dev2
```

**person1 забирает в main только ОДИН коммит из dev2 (уровень критичности)**

```console
person1 (main)$ git fetch
From https://github.com/sl4sh73r/git-practice-1
   6754112..a894d1f  dev2       -> origin/dev2

person1 (main)$ git log --oneline main..origin/dev2
a894d1f dev2: каналы доставки оповещений
5e341d5 dev2: уровень критичности оповещения

person1 (main)$ git cherry-pick 5e341d5
[main 1007b3e] dev2: уровень критичности оповещения
 Author: VadimKarmazin <99864658+VadimKarmazin@users.noreply.github.com>
 Date: Fri Oct 2 18:48:20 2026 +0300
 1 file changed, 5 insertions(+)

person1 (main)$ git log --oneline -3
1007b3e dev2: уровень критичности оповещения
1df263d monitor: возвращены колонки p95 и простой, потерянные при checkout --theirs
eab9a36 Merge origin/dev2: в конфликте VERSION принята версия dev2 (--theirs)

person1 (main)$ git log -1 --format="автор: %an, коммиттер: %cn"
автор: VadimKarmazin, коммиттер: sl4sh73r

person1 (main)$ grep -n "^def" alerts.py
6:def availability_alert(service, availability):
15:def slow_alert(service, avg_ms):
21:def severity(availability):

person1 (main)$ git push
To https://github.com/sl4sh73r/git-practice-1.git
   1df263d..1007b3e  main -> main
```

**Результат.** cherry-pick создал в main копию выбранного коммита с новым хэшем (5e341d5 → 1007b3e), сохранив автора и сообщение; коммиттером стал тот, кто выполнил перенос. Второй коммит dev2 в main не попал.

### 11. Перебазирование dev1 и интерактивный rebase

В dev1 добавлены три коммита, один из которых исправляет ошибку предыдущего. Ветвь перебазирована на main, затем через git rebase -i <хэш> коммит-исправление объединён с исходным. При ручном выполнении git rebase -i открывает список действий в редакторе; здесь правка списка (pick → fixup во второй строке) выполнена скриптом через переменную GIT_SEQUENCE_EDITOR.

**В dev1 появляются три новых коммита (slo.py)**

```console
person1 (main)$ git checkout dev1
Switched to branch 'dev1'
Your branch is up to date with 'origin/dev1'.

person1 (dev1)$ git commit -am "dev1: остаток бюджета ошибок budget_left()"
[dev1 7ccdf20] dev1: остаток бюджета ошибок budget_left()
 1 file changed, 5 insertions(+)

person1 (dev1)$ git commit -am "dev1: исправлено округление в budget_left"
[dev1 0bef4e3] dev1: исправлено округление в budget_left
 1 file changed, 1 insertion(+), 1 deletion(-)

person1 (dev1)$ git commit -am "dev1: скорость расхода бюджета burn_rate()"
[dev1 c7cf9e5] dev1: скорость расхода бюджета burn_rate()
 1 file changed, 5 insertions(+)

person1 (dev1)$ git log --oneline --graph -8 dev1 main
* c7cf9e5 dev1: скорость расхода бюджета burn_rate()
* 0bef4e3 dev1: исправлено округление в budget_left
* 7ccdf20 dev1: остаток бюджета ошибок budget_left()
| * 1007b3e dev2: уровень критичности оповещения
| * 1df263d monitor: возвращены колонки p95 и простой, потерянные при checkout --theirs
| *   eab9a36 Merge origin/dev2: в конфликте VERSION принята версия dev2 (--theirs)
| |\  
| | * 6754112 dev2: версия 1.2
| * | 59127e9 monitor: версия 1.1
```

**Перебазирование dev1 на main: три новых коммита переносятся на вершину main**

```console
person1 (dev1)$ git rebase main
Rebasing (1/3)
Rebasing (2/3)
Rebasing (3/3)
Successfully rebased and updated refs/heads/dev1.

person1 (dev1)$ git log --oneline --graph -6 dev1 main
* b87fecb dev1: скорость расхода бюджета burn_rate()
* 05e0997 dev1: исправлено округление в budget_left
* 9f6943f dev1: остаток бюджета ошибок budget_left()
* 1007b3e dev2: уровень критичности оповещения
* 1df263d monitor: возвращены колонки p95 и простой, потерянные при checkout --theirs
*   eab9a36 Merge origin/dev2: в конфликте VERSION принята версия dev2 (--theirs)
|\  
```

**Интерактивный rebase от коммита 1007b3e: объединяем коммит-исправление с предыдущим (pick -> fixup)**

```console
person1 (dev1)$ GIT_SEQUENCE_EDITOR=seqedit.sh git rebase -i 1007b3e
Rebasing (2/3)
Rebasing (3/3)
Successfully rebased and updated refs/heads/dev1.
```

**Список действий, который открыл Git:**

```console
pick 9f6943f # dev1: остаток бюджета ошибок budget_left()
pick 05e0997 # dev1: исправлено округление в budget_left
pick b87fecb # dev1: скорость расхода бюджета burn_rate()
```

**Список после редактирования:**

```console
pick 9f6943f # dev1: остаток бюджета ошибок budget_left()
fixup 05e0997 # dev1: исправлено округление в budget_left
pick b87fecb # dev1: скорость расхода бюджета burn_rate()

person1 (dev1)$ git log --oneline -4
d7607ec dev1: скорость расхода бюджета burn_rate()
f4d95f8 dev1: остаток бюджета ошибок budget_left()
1007b3e dev2: уровень критичности оповещения
1df263d monitor: возвращены колонки p95 и простой, потерянные при checkout --theirs

person1 (dev1)$ git status --short --branch
## dev1...origin/dev1 [ahead 21]
```

**История dev1 переписана, поэтому выгрузка с --force-with-lease**

```console
person1 (dev1)$ git push --force-with-lease
To https://github.com/sl4sh73r/git-practice-1.git
   99613f3..d7607ec  dev1 -> dev1

person1 (dev1)$ git checkout main
Switched to branch 'main'
Your branch is up to date with 'origin/main'.
```

**Результат.** После git rebase main три коммита dev1 стоят поверх вершины main, история линейная. После интерактивного rebase коммитов стало два. В списке действий можно также менять порядок строк (перемещение коммитов), использовать squash, reword, edit, drop.

### 12. Патчи: git format-patch и git apply

В dev3 создана серия из трёх коммитов с тестами. Для них сформированы патчи и применены к ветви main.

**person3 обновляет main и подтягивает dev3 до актуального main**

```console
person3 (dev3)$ git checkout main
Switched to branch 'main'
Your branch is up to date with 'origin/main'.

person3 (main)$ git pull
From https://github.com/sl4sh73r/git-practice-1
   3b918ee..1007b3e  main       -> origin/main
 * [new branch]      dev1       -> origin/dev1
   2925c08..a894d1f  dev2       -> origin/dev2
Updating 3b918ee..1007b3e
Fast-forward
 alerts.py  | 23 +++++++++++++++++++++++
 checks.csv |  3 +++
 metrics.py |  4 +++-
 monitor.py |  2 +-
 slo.py     | 12 ++++++++++++
 5 files changed, 42 insertions(+), 2 deletions(-)
 create mode 100644 alerts.py
 create mode 100644 slo.py

person3 (main)$ git checkout dev3
Switched to branch 'dev3'
Your branch is up to date with 'origin/dev3'.

person3 (dev3)$ git merge --no-edit main
Updating cf00619..1007b3e
Fast-forward
 alerts.py  | 23 +++++++++++++++++++++++
 checks.csv |  3 +++
 monitor.py |  2 +-
 slo.py     | 12 ++++++++++++
 4 files changed, 39 insertions(+), 1 deletion(-)
 create mode 100644 alerts.py
 create mode 100644 slo.py
```

**Серия из трёх коммитов в dev3: тесты**

```console
person3 (dev3)$ git add test_metrics.py

person3 (dev3)$ git commit -m "dev3: тест расчёта доступности"
[dev3 783340f] dev3: тест расчёта доступности
 1 file changed, 17 insertions(+)
 create mode 100644 test_metrics.py

person3 (dev3)$ git commit -am "dev3: тесты времени ответа и простоя"
[dev3 e33a1f5] dev3: тесты времени ответа и простоя
 1 file changed, 4 insertions(+)

person3 (dev3)$ git add test_slo.py

person3 (dev3)$ git commit -m "dev3: тесты SLO"
[dev3 10d19f7] dev3: тесты SLO
 1 file changed, 15 insertions(+)
 create mode 100644 test_slo.py

person3 (dev3)$ git push
To https://github.com/sl4sh73r/git-practice-1.git
   cf00619..10d19f7  dev3 -> dev3

person3 (dev3)$ git log --oneline main..dev3
10d19f7 dev3: тесты SLO
e33a1f5 dev3: тесты времени ответа и простоя
783340f dev3: тест расчёта доступности
```

**Создаём патчи для этих коммитов**

```console
person3 (dev3)$ git format-patch main -o ../patches
../patches/0001-dev3.patch
../patches/0002-dev3.patch
../patches/0003-dev3-SLO.patch

person3 (dev3)$ head -20 ../patches/0001-*.patch
From 783340f5773896500d698cdb29be28584fb2064f Mon Sep 17 00:00:00 2001
From: VadimKarmazin <99864658+VadimKarmazin@users.noreply.github.com>
Date: Fri, 2 Oct 2026 18:48:29 +0300
Subject: [PATCH 1/3] =?UTF-8?q?dev3:=20=D1=82=D0=B5=D1=81=D1=82=20=D1=80?=
 =?UTF-8?q?=D0=B0=D1=81=D1=87=D1=91=D1=82=D0=B0=20=D0=B4=D0=BE=D1=81=D1=82?=
 =?UTF-8?q?=D1=83=D0=BF=D0=BD=D0=BE=D1=81=D1=82=D0=B8?=
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit

---
 test_metrics.py | 17 +++++++++++++++++
 1 file changed, 17 insertions(+)
 create mode 100644 test_metrics.py

diff --git a/test_metrics.py b/test_metrics.py
new file mode 100644
index 0000000..0e29aed
--- /dev/null
+++ b/test_metrics.py
```

**Применяем патчи к ветви main**

```console
person3 (dev3)$ git checkout main
Switched to branch 'main'
Your branch is up to date with 'origin/main'.

person3 (main)$ git apply --stat ../patches/*.patch
 test_metrics.py |   17 +++++++++++++++++
 1 file changed, 17 insertions(+)
 test_metrics.py |    4 ++++
 1 file changed, 4 insertions(+)
 test_slo.py     |   15 +++++++++++++++
 1 file changed, 15 insertions(+)

person3 (main)$ git apply --check ../patches/0001-*.patch && echo "патч 0001 применим"
патч 0001 применим

person3 (main)$ git apply ../patches/*.patch
```

**git apply меняет только рабочий каталог и не создаёт коммитов (в отличие от git am)**

```console
person3 (main)$ git status --short
?? test_metrics.py
?? test_slo.py

person3 (main)$ python3 -m unittest 2>&1 | tail -3
Ran 3 tests in 0.000s

OK

person3 (main)$ git add test_metrics.py test_slo.py

person3 (main)$ git commit -m "Тесты показателей и SLO (патчи из dev3 применены через git apply)"
[main dae0aaa] Тесты показателей и SLO (патчи из dev3 применены через git apply)
 2 files changed, 36 insertions(+)
 create mode 100644 test_metrics.py
 create mode 100644 test_slo.py

person3 (main)$ git push
To https://github.com/sl4sh73r/git-practice-1.git
   1007b3e..dae0aaa  main -> main

person3 (main)$ git log --oneline -4
dae0aaa Тесты показателей и SLO (патчи из dev3 применены через git apply)
1007b3e dev2: уровень критичности оповещения
1df263d monitor: возвращены колонки p95 и простой, потерянные при checkout --theirs
eab9a36 Merge origin/dev2: в конфликте VERSION принята версия dev2 (--theirs)
```

**Результат.** format-patch создаёт по одному файлу .patch на коммит (с автором, датой и сообщением). git apply переносит только изменения файлов в рабочий каталог, коммит создаётся вручную; чтобы перенести патчи вместе с коммитами, используется git am.

### 13. Итоговая версия продукта

После индивидуальных заданий (разделы ниже) работа над проектом продолжена: доработанная ветвь dev1 влита в main, а модули SLO и оповещений подключены к отчёту.

**person1 вливает доработанную ветвь dev1 (остаток и скорость расхода бюджета ошибок) в main**

```console
person1 (main)$ git pull
From https://github.com/sl4sh73r/git-practice-1
   dae0aaa..aed3b2a  main       -> origin/main
Updating dae0aaa..aed3b2a
Fast-forward
 CHANGELOG.md | 6 ++++++
 1 file changed, 6 insertions(+)
 create mode 100644 CHANGELOG.md

person1 (main)$ git merge --no-edit dev1
Merge made by the 'ort' strategy.
 slo.py | 10 ++++++++++
 1 file changed, 10 insertions(+)

person1 (main)$ git push
To https://github.com/sl4sh73r/git-practice-1.git
   aed3b2a..5517385  main -> main
```

**person2 получает main и подключает SLO и оповещения к отчёту**

```console
person2 (main)$ git pull
From https://github.com/sl4sh73r/git-practice-1
   aed3b2a..5517385  main       -> origin/main
Updating aed3b2a..5517385
Fast-forward
 slo.py | 10 ++++++++++
 1 file changed, 10 insertions(+)

person2 (main)$ git diff --stat
 CHANGELOG.md |  3 +++
 monitor.py   | 22 +++++++++++++++++++---
 2 files changed, 22 insertions(+), 3 deletions(-)

person2 (main)$ python3 monitor.py
PulseWatch v1.3: отчёт о доступности сервисов
сервис     доступность  ответ, мс  p95, мс  простой, мин
api            100.00%        108      154             0
payments        80.00%        317      342            15
web             93.33%        254      280             5

SLO api (99.5%): выполнен, расход бюджета ошибок x0.0 от нормы
SLO payments (99.9%): НАРУШЕН, расход бюджета ошибок x200.0 от нормы
ALERT payments: доступность 80.00% ниже 99.0% [critical]
ALERT payments: среднее время ответа 317 мс выше 300 мс [critical]
SLO web (99.0%): НАРУШЕН, расход бюджета ошибок x6.67 от нормы
ALERT web: доступность 93.33% ниже 99.0% [critical]

person2 (main)$ python3 -m unittest 2>&1 | tail -3
Ran 3 tests in 0.000s

OK

person2 (main)$ git commit -am "monitor: в отчёте статус SLO, расход бюджета ошибок и оповещения (версия 1.3)"
[main 5ba8974] monitor: в отчёте статус SLO, расход бюджета ошибок и оповещения (версия 1.3)
 2 files changed, 22 insertions(+), 3 deletions(-)

person2 (main)$ git push
To https://github.com/sl4sh73r/git-practice-1.git
   5517385..5ba8974  main -> main

person2 (main)$ git log --oneline --graph -6
* 5ba8974 monitor: в отчёте статус SLO, расход бюджета ошибок и оповещения (версия 1.3)
*   5517385 Merge branch 'dev1'
|\  
| * d7607ec dev1: скорость расхода бюджета burn_rate()
| * f4d95f8 dev1: остаток бюджета ошибок budget_left()
* | aed3b2a CHANGELOG: запись о восстановлении через reflog
* | 639d3a4 CHANGELOG: журнал изменений версии 1.2
```

**Результат.** Итоговый отчёт PulseWatch показывает по каждому сервису доступность, время ответа, простой, выполнение SLO, скорость расхода бюджета ошибок и активные оповещения с уровнем критичности.

## Индивидуальные задания

### Вариант 1. Создание тегов для версионирования кода

Выполнил sl4sh73r в рабочем каталоге person1 на ветви main.

```console
person1 (main)$ git pull
From https://github.com/sl4sh73r/git-practice-1
   1007b3e..dae0aaa  main       -> origin/main
   cf00619..10d19f7  dev3       -> origin/dev3
Updating 1007b3e..dae0aaa
Fast-forward
 test_metrics.py | 21 +++++++++++++++++++++
 test_slo.py     | 15 +++++++++++++++
 2 files changed, 36 insertions(+)
 create mode 100644 test_metrics.py
 create mode 100644 test_slo.py
```

**1. Легковесный тег для текущего состояния репозитория**

```console
person1 (main)$ git tag v1.0
```

**2. Проверка созданного тега**

```console
person1 (main)$ git tag
v1.0
```

**3. Аннотированный тег с сообщением**

```console
person1 (main)$ git tag -a v1.1 -m "Версия 1.1: отчёт о доступности, SLO, оповещения, тесты"
```

**4. Список всех тегов**

```console
person1 (main)$ git tag -l
v1.0
v1.1

person1 (main)$ git show --no-patch v1.1
tag v1.1
Tagger: sl4sh73r <87204613+sl4sh73r@users.noreply.github.com>
Date:   Fri Oct 2 18:48:34 2026 +0300

Версия 1.1: отчёт о доступности, SLO, оповещения, тесты

commit dae0aaaba5104beb8e6c7bd28e29504825e00254
Author: VadimKarmazin <99864658+VadimKarmazin@users.noreply.github.com>
Date:   Fri Oct 2 18:48:31 2026 +0300

    Тесты показателей и SLO (патчи из dev3 применены через git apply)

person1 (main)$ git cat-file -t v1.0; git cat-file -t v1.1
commit
tag
```

**5. Публикация одного тега в удалённом репозитории**

```console
person1 (main)$ git push origin v1.0
To https://github.com/sl4sh73r/git-practice-1.git
 * [new tag]         v1.0 -> v1.0
```

**6. Проверка: на сервере есть только v1.0**

```console
person1 (main)$ git ls-remote --tags origin
dae0aaaba5104beb8e6c7bd28e29504825e00254	refs/tags/v1.0
```

**7. Ещё один легковесный тег с другим именем**

```console
person1 (main)$ git tag v1.2-beta
```

**8. Список тегов после создания нового**

```console
person1 (main)$ git tag -l
v1.0
v1.1
v1.2-beta
```

**9. Отправка всех тегов**

```console
person1 (main)$ git push origin --tags
To https://github.com/sl4sh73r/git-practice-1.git
 * [new tag]         v1.1 -> v1.1
 * [new tag]         v1.2-beta -> v1.2-beta
```

**10. Проверка наличия всех тегов в удалённом репозитории**

```console
person1 (main)$ git ls-remote --tags origin
dae0aaaba5104beb8e6c7bd28e29504825e00254	refs/tags/v1.0
1fb64df88ee89a7da2aeb79c0aa67956c19d27ad	refs/tags/v1.1
dae0aaaba5104beb8e6c7bd28e29504825e00254	refs/tags/v1.1^{}
dae0aaaba5104beb8e6c7bd28e29504825e00254	refs/tags/v1.2-beta
```

**Результат.** Легковесный тег является простым указателем на коммит (тип объекта commit). Аннотированный тег является отдельным объектом (тип tag) с автором, датой и сообщением, поэтому в git ls-remote у него две строки: сам тег и коммит, на который он указывает (^{}). git push origin <тег> публикует один тег, git push origin --tags публикует все. Теги видны на GitHub: https://github.com/sl4sh73r/git-practice-1/tags

### Вариант 8. Git reflog: восстановление потерянных коммитов

Выполнил VadimKarmazin в рабочем каталоге person2 на ветви main.

```console
person2 (dev2)$ git checkout main
Switched to branch 'main'
Your branch is up to date with 'origin/main'.

person2 (main)$ git pull
From https://github.com/sl4sh73r/git-practice-1
   67691d0..dae0aaa  main       -> origin/main
 * [new branch]      dev1       -> origin/dev1
 * [new branch]      dev3       -> origin/dev3
 * [new tag]         v1.0       -> v1.0
 * [new tag]         v1.1       -> v1.1
 * [new tag]         v1.2-beta  -> v1.2-beta
Updating 67691d0..dae0aaa
Fast-forward
 README.md       |  9 +++++++++
 alerts.py       | 23 +++++++++++++++++++++++
 checks.csv      |  3 +++
 metrics.py      |  8 +++++++-
 monitor.py      |  5 +++--
 services.py     | 12 ++++++++++++
 slo.py          | 12 ++++++++++++
 test_metrics.py | 21 +++++++++++++++++++++
 test_slo.py     | 15 +++++++++++++++
 9 files changed, 105 insertions(+), 3 deletions(-)
 create mode 100644 README.md
 create mode 100644 alerts.py
 create mode 100644 services.py
 create mode 100644 slo.py
 create mode 100644 test_metrics.py
 create mode 100644 test_slo.py
```

**1. История перемещений HEAD**

```console
person2 (main)$ git reflog -6
dae0aaa HEAD@{0}: pull: Fast-forward
67691d0 HEAD@{1}: checkout: moving from dev2 to main
a894d1f HEAD@{2}: commit: dev2: каналы доставки оповещений
5e341d5 HEAD@{3}: commit: dev2: уровень критичности оповещения
6754112 HEAD@{4}: commit: dev2: версия 1.2
199192b HEAD@{5}: commit: dev2: проверки за 11:10
```

**Делаем коммит, который затем «потеряем»**

```console
person2 (main)$ git add CHANGELOG.md

person2 (main)$ git commit -m "CHANGELOG: журнал изменений версии 1.2"
[main 639d3a4] CHANGELOG: журнал изменений версии 1.2
 1 file changed, 5 insertions(+)
 create mode 100644 CHANGELOG.md

person2 (main)$ git log --oneline -3
639d3a4 CHANGELOG: журнал изменений версии 1.2
dae0aaa Тесты показателей и SLO (патчи из dev3 применены через git apply)
1007b3e dev2: уровень критичности оповещения
```

**2. Откат на предыдущий коммит: последний коммит и его изменения исчезают из ветви**

```console
person2 (main)$ git reset --hard HEAD~1
HEAD is now at dae0aaa Тесты показателей и SLO (патчи из dev3 применены через git apply)

person2 (main)$ git log --oneline -3
dae0aaa Тесты показателей и SLO (патчи из dev3 применены через git apply)
1007b3e dev2: уровень критичности оповещения
1df263d monitor: возвращены колонки p95 и простой, потерянные при checkout --theirs

person2 (main)$ ls CHANGELOG.md
ls: CHANGELOG.md: No such file or directory
```

**3. Ищем потерянный коммит в reflog**

```console
person2 (main)$ git reflog -4
dae0aaa HEAD@{0}: reset: moving to HEAD~1
639d3a4 HEAD@{1}: commit: CHANGELOG: журнал изменений версии 1.2
dae0aaa HEAD@{2}: pull: Fast-forward
67691d0 HEAD@{3}: checkout: moving from dev2 to main
```

**4. Создаём новую ветвь от хэша потерянного коммита 639d3a4**

```console
person2 (main)$ git checkout -b restored 639d3a4
Switched to a new branch 'restored'

person2 (restored)$ ls CHANGELOG.md
CHANGELOG.md
```

**5. Проверяем историю: коммит восстановлен**

```console
person2 (restored)$ git log --oneline -3
639d3a4 CHANGELOG: журнал изменений версии 1.2
dae0aaa Тесты показателей и SLO (патчи из dev3 применены через git apply)
1007b3e dev2: уровень критичности оповещения
```

**6. Дополняем и фиксируем восстановленные изменения, возвращаем их в main и на сервер**

```console
person2 (restored)$ git commit -am "CHANGELOG: запись о восстановлении через reflog"
[restored aed3b2a] CHANGELOG: запись о восстановлении через reflog
 1 file changed, 1 insertion(+)

person2 (restored)$ git checkout main
Switched to branch 'main'
Your branch is up to date with 'origin/main'.

person2 (main)$ git merge restored
Updating dae0aaa..aed3b2a
Fast-forward
 CHANGELOG.md | 6 ++++++
 1 file changed, 6 insertions(+)
 create mode 100644 CHANGELOG.md

person2 (main)$ git push
To https://github.com/sl4sh73r/git-practice-1.git
   dae0aaa..aed3b2a  main -> main

person2 (main)$ git branch -d restored
Deleted branch restored (was aed3b2a).

person2 (main)$ git log --oneline -3
aed3b2a CHANGELOG: запись о восстановлении через reflog
639d3a4 CHANGELOG: журнал изменений версии 1.2
dae0aaa Тесты показателей и SLO (патчи из dev3 применены через git apply)

person2 (main)$ git status
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean

person2 (main)$ git reflog -8
aed3b2a HEAD@{0}: merge restored: Fast-forward
dae0aaa HEAD@{1}: checkout: moving from restored to main
aed3b2a HEAD@{2}: commit: CHANGELOG: запись о восстановлении через reflog
639d3a4 HEAD@{3}: checkout: moving from main to restored
dae0aaa HEAD@{4}: reset: moving to HEAD~1
639d3a4 HEAD@{5}: commit: CHANGELOG: журнал изменений версии 1.2
dae0aaa HEAD@{6}: pull: Fast-forward
67691d0 HEAD@{7}: checkout: moving from dev2 to main
```

**Результат.** После git reset --hard HEAD~1 коммит 639d3a4 исчез из git log, но остался в базе объектов; reflog хранит все перемещения HEAD и позволил найти его хэш. Ветвь restored, созданная от этого хэша, вернула коммит и файл CHANGELOG.md, после чего изменения дополнены, слиты в main и отправлены на сервер.

## Выводы

1. Создан удалённый репозиторий на GitHub, с ним работали три локальных рабочих каталога. Отработан полный цикл add → commit → push → fetch/pull.
2. Изучены три способа слияния. Merge сохраняет полную историю ветви, squash даёт один аккуратный коммит, rebase делает историю линейной ценой пересоздания коммитов.
3. Правки одного файла в разных местах Git сливает автоматически; конфликт возникает только при изменении одних и тех же строк. Освоены отмена слияния, ручное разрешение, выбор стороны (--ours/--theirs, -X theirs).
4. Команды, переписывающие историю (commit --amend, rebase, reset --hard), меняют хэши коммитов; для опубликованных ветвей после них требуется push --force-with-lease, поэтому применять их следует только в собственных ветвях.
5. Теги фиксируют версии продукта, а reflog позволяет вернуть коммиты, потерянные после reset --hard.
6. В ходе работы двумя участниками разработан и доведён до версии 1.3 продукт PulseWatch: мониторинг доступности сервисов с контролем SLO, бюджета ошибок и оповещениями.
