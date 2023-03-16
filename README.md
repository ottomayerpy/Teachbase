## Тестовое задание для Backend-разработчика от Teachbase

### Задача
#### Необходимо разработать:
- Client для работы с Teachbase API. 
- Авторизация.
- Проверка токена.
- Отправка запросов.
##### Реализовать в клиенте методы для получения/отправки данных из (в) Teachbase API (POST, GET). 
1) https://go.teachbase.ru/api-docs/index.html#/courses/get_courses - список курсов
2) https://go.teachbase.ru/api-docs/index.html#/courses/get_courses__id_ - детальное представление курса
3) https://go.teachbase.ru/api-docs/index.html#/users/post_users_create - создание пользователя
4) https://go.teachbase.ru/api-docs/index.html#/course_sessions/post_course_sessions__session_id__register - запись пользователя на сессию
5) https://go.teachbase.ru/api-docs/index.html#/course_sessions/get_courses__course_id__course_sessions - сессии курсов
##### Создать модель курса с сохранение данных из Teachbase (*).

##### DRF. Реализовать метод для получения данных курса из модели Django (*).
- Список всех курсов - /courses/
- Детальное представление курса - /courses/<id>


### Зависимости

- Django - 4.1.7
- djangorestframework - 3.14.0

### Запуск приложения
1) ```git clone https://github.com/Teachbase_test_task```
2) переименуйте **.env.example** файл на **.env**
3) ```docker-compose up -d --build```
4) http://127.0.0.1:8000/swagger/

### Flow проверки задания
Для проверки работы приложения предлагаю использовать swagger

### Документация 
- swagger  url http://127.0.0.1:8000/swagger/


##### Создание суперпользователя
Для создания суперпользователя пользователя используйте команды:
```
docker-compose exec web bash
python manage.py createsuperuser
```

