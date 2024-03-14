from flask import Flask
from data import db_session
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/marsiane.db")
    db_sess = db_session.create_session()
    captain = User()
    captain.name = 'Ridley'
    captain.surname = 'Scott'
    captain.age = 21
    captain.position = 'captain'
    captain.speciality = 'research engineer'
    captain.address = 'module_1'
    captain.email = 'scott_chief@mars.org'
    db_sess.add(captain)
    names = ['Kirill', 'Andrew', 'Vasya']
    surnames = ['Petrov', 'Ivanov', 'Pupkin']
    ages = [19, 20, 22]
    positions = ['mladshiy rabotyaga', 'sredniy rabotyaga', 'starshiy rabotyaga']
    specialities = ['pythonist', 'doctor', 'zam captain']
    addresses = ['module_2', 'module_3', 'module_4']
    emails = ['pythonist@mars.org', 'doctor@mars.org', 'zam_captain@mars.org']
    for name, surname, age, position, speciality, address, email in zip(names, surnames, ages, positions, specialities, addresses, emails):
        user = User()
        user.name = name
        user.surname = surname
        user.age = age
        user.position = position
        user.speciality = speciality
        user.address = address
        user.email = email
        db_sess.add(user)
    db_sess.commit()
    # app.run()


if __name__ == '__main__':
    main()