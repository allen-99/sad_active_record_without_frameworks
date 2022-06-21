from flask import Flask, json, request, render_template
import pymysql.cursors

app = Flask(__name__)


@app.route('/all_messages')
def all_messages():

    messages = Message().all_messages()
    return render_template('index.html', messages=json.loads(messages)['messages'])


@app.route('/one_message', methods=['POST', 'GET'])
def one_message():

    if request.method == 'POST':
        if request.form.get('id') == '':
            messages = Message().all_messages()
            return render_template('delete_and_find_one.html', messages=json.loads(messages)['messages'])

        id_ = int(request.form.get('id'))
        messages = Message().one_message_id(id_)
        return render_template('delete_and_find_one.html', messages=json.loads(messages)['messages'])

    if request.method == 'GET':
        messages = Message().all_messages()
        return render_template('delete_and_find_one.html', messages=json.loads(messages)['messages'])


@app.route('/some_messages', methods=['POST', 'GET'])
def some_messages():

    if request.method == 'POST':
        title_name = (request.form.get('title_name'))
        title = (request.form.get('title'))
        try:
            messages = Message().some_messages(title_name, title)
        except:
            messages = Message().all_messages()
        return render_template('index.html', messages=json.loads(messages)['messages'])

    if request.method == 'GET':
        messages = Message().all_messages()
        return render_template('index.html', messages=json.loads(messages)['messages'])


@app.route('/save', methods=['POST', 'GET'])
def save():
    message = Message
    message.title = (request.form.get('title'))
    message.date = (request.form.get('date'))
    message.message = (request.form.get('message'))

    message().save()
    return render_template('add_message.html')


@app.route('/delete', methods=['POST', 'GET'])
def delete():

    if request.method == 'POST':
        if request.form.get('delete') == '':
            messages = Message().all_messages()
            return render_template('delete_and_find_one.html', messages=json.loads(messages)['messages'])
        id_ = int(request.form.get('delete'))
        messages = Message().delete(id_)
        return render_template('delete_and_find_one.html', messages=json.loads(messages)['messages'])

    if request.method == 'GET':
        messages = Message().all_messages()
        return render_template('delete_and_find_one.html', messages=json.loads(messages)['messages'])


if __name__ == '__main__':
    app.run()


class Message:
    id = None
    title = None
    message = None
    date = None
    connection_ = None
    cursor = None

    def __init__(self):
        self.connection_ = pymysql.connect(host='0.0.0.0',
                                      user='hehe',
                                      password='hehe',
                                      db='hmwk',
                                      charset='utf8mb4',
                                      cursorclass=pymysql.cursors.DictCursor)

        self.cursor = self.connection_.cursor()

    def all_messages(self):
        line = f"select * from messages"
        self.cursor.execute(line)
        res = []
        for row in self.cursor:
            res.append(row)
        return json.dumps({'messages': res})

    def one_message_id(self, id):
        line = f"select * from messages where id = {id}"
        self.cursor.execute(line)
        res = []
        for row in self.cursor:
            res.append(row)
        return json.dumps({'messages': res})

    def some_messages(self, title, title_name):
        line = f"select * from messages where {title} = '{title_name}' "
        self.cursor.execute(line)
        res = []
        for row in self.cursor:
            res.append(row)
        return json.dumps({'messages': res})

    def save(self):
        id_line = f"select max(id) from messages "
        self.cursor.execute(id_line)
        id_ = -1
        for row in self.cursor:
            id_ = row['max(id)']
        id_ += 1
        sql = f"insert into messages (id, title, message, date) values (" \
              f"{id_}, " \
              f"'{self.title}'," \
              f"'{self.message}'," \
              f"'{self.date}')"

        self.cursor.execute(sql)
        self.connection_.commit()
        res = []
        for row in self.cursor:
            res.append(row)
        return json.dumps({'messages': res})

    def delete(self, id):
        sql = f"delete from messages where id = {id}"
        self.cursor.execute(sql)
        self.connection_.commit()
        res = []
        for row in self.cursor:
            res.append(row)
        return json.dumps({'messages': res})
