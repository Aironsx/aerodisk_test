# aerodisk_test
Веб приожение которое позволяет управлять сетевыми интерфейсами локальной машины

## Описание фукнционала
Приложение дает возможность включать/ выключать сетевой интерфейс, изменять ip адресс, изменять префикс

## Технологии

- Язык: Python
- Фреймворк: Flask

## Что нужно улучшить

- Добавить валидации входных данных (ip, prefix)
...

## Как развернуть на локальной машине

```
git clone git@github.com:Aironsx/aerodisk_test.git
```
```
cd aerodisk_test
```
```
python3 -m venv env
```
```
source/venv/bin/activate
```
```
python3 -m pip install --upgrade pip
```    
```
pip install -r requirements.txt
``` 
``` 
flask --app run run
``` 
