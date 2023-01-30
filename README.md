# aerodisk_test
Веб приожение которое позволяет управлять сетевыми интерфейсами локальной машины

## Описание фукнционала
Приложение дает возможность включать/ выключать сетевой интерфейс, изменять ip адресс, изменять префикс

## Технологии

- Язык: Python
- Фреймворк: Flask

## Что нужно улучшить/доделать

- Добавить валидации входных данных (ip, prefix)
- Миграции
- Перехват ошибок
- Уйти от использования sudo при исполнении команд
- Логирование
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
source env/bin/activate
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
