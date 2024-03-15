import datetime

from flask import Flask, render_template, request

from data import db_session
from data.jobs import Jobs
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def add_worker(sess):
    worker = Jobs()
    worker.team_leader = 1
    worker.job = 'deployment of residential modules 1 and 2'
    worker.work_size = 15
    worker.collaborators = '2, 3'
    worker.start_date = datetime.datetime.now()
    worker.is_finished = False
    sess.add(worker)
    sess.commit()


def add_captain_and_others(sess):
    captain = User()
    captain.name = 'Ridley'
    captain.surname = 'Scott'
    captain.age = 21
    captain.position = 'captain'
    captain.speciality = 'research engineer'
    captain.address = 'module_1'
    captain.email = 'scott_chief@mars.org'
    sess.add(captain)
    names = ['Kirill', 'Andrew', 'Vasya']
    surnames = ['Petrov', 'Ivanov', 'Pupkin']
    ages = [19, 20, 22]
    positions = ['mladshiy rabotyaga', 'sredniy rabotyaga', 'starshiy rabotyaga']
    specialities = ['pythonist', 'doctor', 'zam captain']
    addresses = ['module_2', 'module_3', 'module_4']
    emails = ['pythonist@mars.org', 'doctor@mars.org', 'zam_captain@mars.org']
    for name, surname, age, position, speciality, address, email in zip(
            names, surnames, ages, positions, specialities, addresses, emails
    ):
        user = User()
        user.name = name
        user.surname = surname
        user.age = age
        user.position = position
        user.speciality = speciality
        user.address = address
        user.email = email
        sess.add(user)
    sess.commit()


def add_user(sess, name, surname, age, pos, spec, password, email, address):
    user = User()
    user.name = name
    user.surname = surname
    user.age = age
    user.position = pos
    user.speciality = spec
    user.hashed_password = password
    user.email = email
    user.address = address
    sess.add(user)
    sess.commit()


@app.route('/register', methods=['GET', 'POST'])
def register():
    print(request.method)
    if request.method == 'GET':
        return render_template('register.html', msg={'msg': ''})
    elif request.method == 'POST':
        if request.form['pass'] != request.form['rep_pass']:
            return '<h1>Пароли не совпадают</h1>'
        if not (
                request.form['name'] and
                request.form['surname'] and
                request.form['age'] and
                request.form['pos'] and
                request.form['spec'] and
                request.form['pass'] and
                request.form['rep_pass'] and
                request.form['email'] and
                request.form['address']
        ):
            return '<h1>Не все параметры заполнены</h1>'
        add_user(
            db_sess, request.form['name'],
            request.form['surname'],
            request.form['age'],
            request.form['pos'],
            request.form['spec'],
            request.form['pass'],
            request.form['email'],
            request.form['address']
        )
        return '<h1>Запись добавлена</h1>'


@app.route('/magazine_of_works')
def magazine_of_works():
    works = db_sess.query(Jobs).all()
    users = db_sess.query(User).all()
    team_leaders = {}
    for worker in works:
        for user in users:
            if worker.team_leader == user.id:
                team_leaders[worker.team_leader] = user.surname + ' ' + user.name
    print(team_leaders)
    updated_works = [{'id': work.id, 'job': work.job, 'leader': team_leaders[worker.team_leader - 1], 'duration': work.start_date, 'collaborators': work.collaborators, 'is_finished': work.is_finished} for work in works]
    print(len(updated_works))
    return render_template('magazine.html', works={'works': updated_works})


def main():
    # add_captain_and_others(db_sess)
    # add_worker(db_sess)
    app.run(host='127.0.0.1', port=5000)


if __name__ == '__main__':
    db_session.global_init("db/marsiane.db")
    db_sess = db_session.create_session()
    main()
