# Сайт доставки еды Star Burger

Это сайт сети ресторанов Star Burger. Здесь можно заказать превосходные бургеры с доставкой на дом.

![скриншот сайта](https://dvmn.org/filer/canonical/1594651635/686/)


Сеть Star Burger объединяет несколько ресторанов, действующих под единой франшизой. У всех ресторанов одинаковое меню и одинаковые цены. Просто выберите блюдо из меню на сайте и укажите место доставки. Мы сами найдём ближайший к вам ресторан, всё приготовим и привезём.

На сайте есть три независимых интерфейса. Первый — это публичная часть, где можно выбрать блюда из меню, и быстро оформить заказ без регистрации и SMS.

Второй интерфейс предназначен для менеджера. Здесь происходит обработка заказов. Менеджер видит поступившие новые заказы и первым делом созванивается с клиентом, чтобы подтвердить заказ. После оператор выбирает ближайший ресторан и передаёт туда заказ на исполнение. Там всё приготовят и сами доставят еду клиенту.

Третий интерфейс — это админка. Преимущественно им пользуются программисты при разработке сайта. Также сюда заходит менеджер, чтобы обновить меню ресторанов Star Burger.

## Demo
https://star-burger.test-domain-for-example.ru/

## Как запустить dev-версию сайта

Для запуска сайта нужно запустить **одновременно** бэкенд и фронтенд, в двух терминалах.

### Как собрать бэкенд

Скачайте код:
```sh
git clone https://github.com/devmanorg/star-burger.git
```

Перейдите в каталог проекта:
```sh
cd star-burger
```

[Установите Python](https://www.python.org/), если этого ещё не сделали.

Проверьте, что `python` установлен и корректно настроен. Запустите его в командной строке:
```sh
python --version
```
**Важно!** Версия Python должна быть не ниже 3.6.

Возможно, вместо команды `python` здесь и в остальных инструкциях этого README придётся использовать `python3`. Зависит это от операционной системы и от того, установлен ли у вас Python старой второй версии. 

В каталоге проекта создайте виртуальное окружение:
```sh
python -m venv venv
```
Активируйте его. На разных операционных системах это делается разными командами:

- Windows: `.\venv\Scripts\activate`
- MacOS/Linux: `source venv/bin/activate`


Установите зависимости в виртуальное окружение:
```sh
pip install -r requirements.txt
```

Определите переменную окружения `SECRET_KEY`. Создать файл `.env` в каталоге `star_burger/` и положите туда такой код:
```sh
SECRET_KEY=django-insecure-0if40nf4nf93n4
```
Добавьте другие переменные окружения:

- `DEBUG` — дебаг-режим. Поставьте `True`.
- `YANDEX_GEOCODER_API_KEY` — секретный ключ для доступа к HTTP Геокодер Яндекса.
- `ROLLBAR_TOKEN` — секретный ключ для доступа к логированию Rollbar(Необязательно).
- `ROLLBAR_ENV` — название версии проекта(Необязательно).
- `DATABASE_URL` — URL подключения к базе данных. Пример: `sqlite:////path/to/your/db.sqlite3` для SQLite или `postgres://user:password@localhost:5432/mydatabase` для PostgreSQL.


Запустить Docker-контейнер
```sh
docker run --name mydatabase -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=db -p 5432:5432 -d postgres
```

Сделайте миграции:
```sh
python manage.py migrate
```

Запустите сервер:

```sh
python manage.py runserver
```

Откройте сайт в браузере по адресу [http://127.0.0.1:8000/](http://127.0.0.1:8000/). Если вы увидели пустую белую страницу, то не пугайтесь, выдохните. Просто фронтенд пока ещё не собран. Переходите к следующему разделу README.

### Собрать фронтенд

**Откройте новый терминал**. Для работы сайта в dev-режиме необходима одновременная работа сразу двух программ `runserver` и `parcel`. Каждая требует себе отдельного терминала. Чтобы не выключать `runserver` откройте для фронтенда новый терминал и все нижеследующие инструкции выполняйте там.

[Установите Node.js](https://nodejs.org/en/), если у вас его ещё нет.

Проверьте, что Node.js и его пакетный менеджер корректно установлены. Если всё исправно, то терминал выведет их версии:

```sh
nodejs --version
# v16.16.0
# Если ошибка, попробуйте node:
node --version
# v16.16.0

npm --version
# 8.11.0
```

Версия `nodejs` должна быть не младше `10.0` и не старше `16.16`. Лучше ставьте `16.16.0`, её мы тестировали. Версия `npm` не важна. Как обновить Node.js читайте в статье: [How to Update Node.js](https://phoenixnap.com/kb/update-node-js-version).

Перейдите в каталог проекта и установите пакеты Node.js:

```sh
cd star-burger
npm ci --dev
```

Команда `npm ci` создаст каталог `node_modules` и установит туда пакеты Node.js. Получится аналог виртуального окружения как для Python, но для Node.js.

Помимо прочего будет установлен [Parcel](https://parceljs.org/) — это упаковщик веб-приложений, похожий на [Webpack](https://webpack.js.org/). В отличии от Webpack он прост в использовании и совсем не требует настроек.

Теперь запустите сборку фронтенда и не выключайте. Parcel будет работать в фоне и следить за изменениями в JS-коде:

```sh
./node_modules/.bin/parcel watch bundles-src/index.js --dist-dir bundles --public-url="./"
```

Если вы на Windows, то вам нужна та же команда, только с другими слешами в путях:

```sh
.\node_modules\.bin\parcel watch bundles-src/index.js --dist-dir bundles --public-url="./"
```

Дождитесь завершения первичной сборки. Это вполне может занять 10 и более секунд. О готовности вы узнаете по сообщению в консоли:

```
✨  Built in 10.89s
```

Parcel будет следить за файлами в каталоге `bundles-src`. Сначала он прочитает содержимое `index.js` и узнает какие другие файлы он импортирует. Затем Parcel перейдёт в каждый из этих подключенных файлов и узнает что импортируют они. И так далее, пока не закончатся файлы. В итоге Parcel получит полный список зависимостей. Дальше он соберёт все эти сотни мелких файлов в большие бандлы `bundles/index.js` и `bundles/index.css`. Они полностью самодостаточны, и потому пригодны для запуска в браузере. Именно эти бандлы сервер отправит клиенту.

Теперь если зайти на страницу  [http://127.0.0.1:8000/](http://127.0.0.1:8000/), то вместо пустой страницы вы увидите:

![](https://dvmn.org/filer/canonical/1594651900/687/)

Каталог `bundles` в репозитории особенный — туда Parcel складывает результаты своей работы. Эта директория предназначена исключительно для результатов сборки фронтенда и потому исключёна из репозитория с помощью `.gitignore`.

**Сбросьте кэш браузера <kbd>Ctrl-F5</kbd>.** Браузер при любой возможности старается кэшировать файлы статики: CSS, картинки и js-код. Порой это приводит к странному поведению сайта, когда код уже давно изменился, но браузер этого не замечает и продолжает использовать старую закэшированную версию. В норме Parcel решает эту проблему самостоятельно. Он следит за пересборкой фронтенда и предупреждает JS-код в браузере о необходимости подтянуть свежий код. Но если вдруг что-то у вас идёт не так, то начните ремонт со сброса браузерного кэша, жмите <kbd>Ctrl-F5</kbd>.


## Как запустить prod-версию сайта

### Как собрать бэкенд

Установите Python и необходимые пакеты на сервере:
```sh
sudo apt update
```

```sh
sudo apt install python3-pip python3-dev
```
Перейдите в каталог opt:
```sh
cd /opt
``` 

Скачайте код:
```sh
git clone https://github.com/devmanorg/star-burger.git
```

Перейдите в каталог проекта:
```sh
cd star-burger
``` 

В каталоге проекта создайте виртуальное окружение:
```sh
python3 -m venv venv
```
Активируйте его:
```sh
source venv/bin/activate
```

Установите зависимости в виртуальное окружение:
```sh
pip3 install -r requirements.txt
```

Соберите статику:
```sh
python3 manage.py collectstatic
```

Установите Gunicorn:
```sh
pip3 install gunicorn
```

Установите Nginx:
```sh
sudo apt install nginx
```

Настройте конфигурационный файл Nginx для вашего проекта. Создайте файл конфигурации:
```sh
sudo nano /etc/nginx/sites-enabled/myproject
```

Вставьте следующую конфигурацию в файл:
```sh
server {
    listen 80;
    server_name your_domain_or_IP;


    location /media/ {
        alias /opt/Star-burger/media/;
    }

    location /static/ {
        alias /opt/Star-burger/staticfiles/;
    }

    location /api/ {
        include '/etc/nginx/proxy_params';
        proxy_pass http://127.0.0.1:8000/api/;
    }

    location / {
        include '/etc/nginx/proxy_params';
        proxy_pass http://127.0.0.1:8000/;
    }
}
```

Установите Docker:
```sh
sudo apt install docker.io
```

Запустите контейнер с PostgreSQL:
```sh
sudo docker run --name myproject-postgres -e POSTGRES_DB=myproject -e POSTGRES_USER=myprojectuser -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres
```

Выполните миграции:
```sh
python3 manage.py migrate
```

Настройте переменные окружения: создать файл `.env` в каталоге `star_burger/` со следующими настройками:

- `DEBUG` — дебаг-режим. Поставьте `False`.
- `SECRET_KEY` — секретный ключ проекта. Он отвечает за шифрование на сайте. Например, им зашифрованы все пароли на вашем сайте.
- `ALLOWED_HOSTS` — [см. документацию Django](https://docs.djangoproject.com/en/3.1/ref/settings/#allowed-hosts)
- `YANDEX_GEOCODER_API_KEY` — секретный ключ для доступа к HTTP Геокодер Яндекса.
- `ROLLBAR_TOKEN` — секретный ключ для доступа к логированию Rollbar.
- `ROLLBAR_ENV` — название версии проекта.
- `DATABASE_URL` — URL подключения к базе данных. Пример: `sqlite:////path/to/your/db.sqlite3` для SQLite или `postgres://user:password@localhost:5432/mydatabase` для PostgreSQL.

Создайте systemd для вашего postgres-docker.service:
```sh
sudo nano /etc/systemd/system/postgres-docker.service
```
Вставьте конфигурацию:
```sh
[Unit]
Description=PostgreSQL Docker Container
Requires=docker.service
After=docker.service

[Service]
Restart=always
ExecStart=/usr/bin/docker start myproject-postgres
ExecStop=/usr/bin/docker stop myproject-postgres
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
```

Создайте systemd для вашего star-burger.service:
```sh
sudo nano /etc/systemd/system/star-burger.service
```
Вставьте конфигурацию(ориентируйтесь на свою конфигурацию сервера для опеределения количества воркеров):
```sh
[Unit]
Description=Star Burger Django App
After=network.target postgres-docker.service
Requires=postgres-docker.service

[Service]
WorkingDirectory=/opt/Star-burger
ExecStart=/opt/Star-burger/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 star_burger.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
```

Перезапустите systemd и включите службы:
```sh
sudo systemctl daemon-reload
sudo systemctl enable postgres-docker.service
sudo systemctl enable star-burger.service
sudo systemctl enable nginx
sudo systemctl start postgres-docker.service
sudo systemctl start star-burger.service
sudo systemctl restart postgres-docker.service
sudo systemctl restart star-burger.service
sudo systemctl restart nginx
```

### Фронтенд:
Установка пакетов для фронтенда такая же, как в dev версии

Собрать фронтенд:
```sh
./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"
```


## Обновление кода на сервере
Создайте на сервере Bash-скрипт примерно такого содержания:
```sh
#!/bin/bash

set -e

PROJECT_DIR="/opt/Star-burger"

echo "Starting deployment..."

cd $PROJECT_DIR

echo "Pulling latest code from GitHub..."
git pull

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Building JavaScript code with Parcel..."
./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"

echo "Running database migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Restarting PostgreSQL Docker container..."
sudo systemctl restart postgres-docker

echo "Restarting Gunicorn..."
sudo systemctl restart star-burger

echo "Reloading Nginx..."
sudo systemctl reload nginx

echo "Deployment finished successfully!"
```
### Убедитесь, что деплойный скрипт имеет права на выполнение. Если это не так, выполните следующую команду:

```sh
chmod +x deploy_star_burger.sh
```
### После коммита на GitHub запустите ваш Bash-скрипт на сервере:
```sh
./deploy_star_burger.sh
```

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org). За основу был взят код проекта [FoodCart](https://github.com/Saibharath79/FoodCart).

Где используется репозиторий:

- Второй и третий урок [учебного курса Django](https://dvmn.org/modules/django/)
