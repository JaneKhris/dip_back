### Для запуска сервера
- клонировать репозиторий
- создать базу данных postrges
- в корне проекта создать папку
- в /settings/settings.py внести имя папки, имя базы данных, имя пользователя и пароль postgres
- создать рабочее окружение `python -m vnv venv`
- активировать рабочее окружение `.\venv\Scripts\activate`
- установить пакеты `pip install -r requirements.txt`
- применить миграции `python manage.py migrate`
- запустить сервер `python manage.py runserver`

Данные администратора:
- username: chief_admin
- email:email@email.com
- password: password
  
### Сделать
- обрабатывать ситуацию, когда имя загружвемого файла слишком длинное
- написать функцию переименования для случая, когда файл с таким именем есть в папке (сейчас она есть, работает неправильно)
- заполнение поля downloaded_at при загрузке

### Вопросы
- функции download, download_url в files/viws.py для каких-то файлов открывается окно для загрузки файла, а для каких-то файл открывается в браузере бинарный файл
