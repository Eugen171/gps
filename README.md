# Как запустить 🏃

0. Установить [Docker](https://www.docker.com/products/docker-desktop)

1. Скачать или склонировать этот репозиторий

2. Открыть папку проекта в терминале

3. Собрать образ:
```sh
docker build -t diplom .
```

4. Запустить 🏎
```sh
docker run -p 80:3000 diplom
```

Теперь можно перейти на [localhost](http://localhost)

# Установка IP ESP

Как только перейдешь на [localhost](http://localhost/), увидешь окно
настроек. Здесь в поле ввода нужно указать IP адрес ESP (Компьютер и
esp должны находиться в одной сети).

При этом ожидается, что esp настроена таким образом, чтобы при
обращении к ней в "/" она возвращала никак не обработанные строки NMEA.

Дальше просто выбираешь любой пункт и смотришь на результат.
