# Payments_System_Django

Платежная система (имитация webhook от банка)

_Техническое задание:_

```text
Реализовать backend-сервис, который:

- принимает входящие webhook-и от банка
- обрабатывает их
- корректно начисляет баланс организации по ИНН
```

Полный текст ТЗ можно прочесть здесь: [ЗДЕСЬ](https://gist.github.com/an1creator/312d0b7cb68da921e725f9929accc971)

* `/api/webhook/bank/` - адрес приема данных платежа
* `/api/organizations/<inn>/balance/` - адрес просмотра баланса счета по ИНН
* `/api/schema/` - адрес yaml-схемы API-функционала
* `/api/docs/` - адрес swagger-схемы API-функционала
* `/api/redoc/` - адрес redoc-схемы API-функционала

## Примеры:

* #### _API swagger:_
* ![swagger.JPG](README%2Fswagger.JPG)

## Порядок запуска:

* Клонировать: `git clone `
* Установить зависимости: `pip install -r requirements.txt`
* Создать миграции: `python manage.py makemigrations`
* Применить миграции: `python manage.py migrate`
* Запустить сервер: `python manage.py runserver`

### _Примечания:_

1. По необходимости, запустить тесты: `python manage.py test`
