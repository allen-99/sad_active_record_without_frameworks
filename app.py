from flask import Flask, json, request, render_template
import pymysql.cursors

app = Flask(__name__)


def get_connection():
    connection_ = pymysql.connect(host='0.0.0.0',
                                  user='root',
                                  password='hehe',
                                  db='hmwk',
                                  charset='utf8mb4',
                                  cursorclass=pymysql.cursors.DictCursor)
    return connection_


@app.route('/all_messages')
def all_messages():
    connection = get_connection()
    cursor = connection.cursor()
    messages = Message.all_messages(cursor)
    return render_template('index.html', messages=json.loads(messages)['messages'])


@app.route('/one_message', methods=['POST', 'GET'])
def one_message():
    connection = get_connection()
    cursor = connection.cursor()

    if request.method == 'POST':
        if request.form.get('id') == '':
            messages = Message.all_messages(cursor)
            return render_template('delete_and_find_one.html', messages=json.loads(messages)['messages'])

        id_ = int(request.form.get('id'))
        messages = Message.one_message_id(id_, cursor)
        return render_template('delete_and_find_one.html', messages=json.loads(messages)['messages'])

    if request.method == 'GET':
        messages = Message.all_messages(cursor)
        return render_template('delete_and_find_one.html', messages=json.loads(messages)['messages'])


@app.route('/some_messages', methods=['POST', 'GET'])
def some_messages():
    connection = get_connection()
    cursor = connection.cursor()

    if request.method == 'POST':
        title_name = (request.form.get('title_name'))
        title = (request.form.get('title'))
        try:
            messages = Message.some_messages(title_name, title, cursor)
        except:
            messages = Message.all_messages(cursor)
        return render_template('index.html', messages=json.loads(messages)['messages'])

    if request.method == 'GET':
        messages = Message.all_messages(cursor)
        return render_template('index.html', messages=json.loads(messages)['messages'])


@app.route('/save', methods=['POST', 'GET'])
def save():
    connection = get_connection()
    cursor = connection.cursor()
    message = Message
    message.title = (request.form.get('title'))
    message.date = (request.form.get('date'))
    message.message = (request.form.get('message'))

    message().save(cursor, connection)
    return render_template('add_message.html')


@app.route('/delete', methods=['POST', 'GET'])
def delete():
    connection = get_connection()
    cursor = connection.cursor()
    if request.method == 'POST':
        if request.form.get('delete') == '':
            messages = Message.all_messages(cursor)
            return render_template('delete_and_find_one.html', messages=json.loads(messages)['messages'])
        id_ = int(request.form.get('delete'))
        messages = Message().delete(id_, cursor, connection)
        return render_template('delete_and_find_one.html', messages=json.loads(messages)['messages'])

    if request.method == 'GET':
        messages = Message.all_messages(cursor)
        return render_template('delete_and_find_one.html', messages=json.loads(messages)['messages'])


if __name__ == '__main__':
    app.run()


class Message:
    id = None
    title = None
    message = None
    date = None

    def all_messages(cursor):
        line = f"select * from messages"
        cursor.execute(line)
        res = []
        for row in cursor:
            res.append(row)
        return json.dumps({'messages': res})

    def one_message_id(id, cursor):
        line = f"select * from messages where id = {id}"
        cursor.execute(line)
        res = []
        for row in cursor:
            res.append(row)
        return json.dumps({'messages': res})

    def some_messages(title, title_name, cursor):
        line = f"select * from messages where {title} = '{title_name}' "
        cursor.execute(line)
        res = []
        for row in cursor:
            res.append(row)
        return json.dumps({'messages': res})

    def save(self, cursor, connection):
        id_line = f"select max(id) from messages "
        cursor.execute(id_line)
        id = -1
        for row in cursor:
            id = row['max(id)']
        id += 1
        sql = f"insert into messages (id, title, message, date) values (" \
              f"{id}, " \
              f"'{self.title}'," \
              f"'{self.message}'," \
              f"'{self.date}')"

        cursor.execute(sql)
        connection.commit()
        res = []
        for row in cursor:
            res.append(row)
        return json.dumps({'messages': res})

    def delete(self, id, cursor, connection):
        sql = f"delete from messages where id = {id}"
        cursor.execute(sql)
        connection.commit()
        res = []
        for row in cursor:
            res.append(row)
        return json.dumps({'messages': res})
