from flask import Flask, json, request, render_template
import pymysql.cursors

app = Flask(__name__)


def get_connection():
    connection_ = pymysql.connect(host='0.0.0.0',
                                  user='root',
                                  password='77720140',
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


@app.route('/one_message', methods=['POST'])
def one_message():
    connection = get_connection()
    cursor = connection.cursor()
    id_ = int(request.args.get('id'))
    messages = Message.one_message_id(id_, cursor)
    return messages


@app.route('/some_messages', methods=['POST'])
def some_messages():
    connection = get_connection()
    cursor = connection.cursor()
    title_name = (request.args.get('title_name'))
    title = (request.args.get('title'))

    messages = Message.some_messages(title_name, title, cursor)
    return messages


@app.route('/save', methods=['POST'])
def save():
    connection = get_connection()
    cursor = connection.cursor()
    message = Message
    message.title = (request.args.get('title'))
    message.date = (request.args.get('date'))
    message.message = (request.args.get('message'))

    message().save(cursor, connection)
    return json.dumps({'message': 'add successfully'})


@app.route('/delete', methods=['POST'])
def delete():
    connection = get_connection()
    cursor = connection.cursor()
    id = (request.args.get('id'))
    message = Message
    message().delete(id, cursor, connection)
    return json.dumps({'message': 'delete successfully'})


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
