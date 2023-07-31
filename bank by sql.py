import sqlite3

connection = sqlite3.connect('bank.db')
sql=connection.cursor()
sql.execute('CREATE TABLE IF NOT EXISTS bank_users(user_id INTEGER PRIMARY KEY, user_name TEXT, user_number TEXT, user_balanc FLOAT, balanc_in12 FLOAT, balanc_in24 FLOAT, balanc_in36 FLOAT);')

while True:
    print('-------------------------','\n''1-регистрация клиентов','\n''2-поиск клиентов','\n''3-личный кабинет','\n''4-показат всех ползователей','\n''5-остановит программу')
    operator1=int(input('выбирайте: '))
    balanc=0
    balanc_12=0
    balanc_24=0
    balanc_36=0
    if operator1==1:
        name=input('ведите имя ползователя: ').title()
        number=input('ведите номер телефона: ')
        sql.execute(f'INSERT INTO bank_users(user_name, user_number, user_balanc, balanc_in12, balanc_in24, balanc_in36) VALUES (?, ?, ?, ?, ?, ?)',(name, number, balanc, balanc_12, balanc_24, balanc_36))
        connection.commit()
    elif operator1==2:
        search=input('кого ишете? ').title()
        j = []
        for i in sql.execute('SELECT user_name FROM bank_users').fetchall():
            j += i
        if search in j:
            print(sql.execute(f'SELECT * FROM bank_users WHERE user_name="{search}"').fetchall())
        else:
            print('такого ползователя нету в таблице')
    elif operator1==3:
        operator2=input('в чию кабинет хотите зайти? ').title()
        j = []
        for i in sql.execute('SELECT user_name FROM bank_users').fetchall():
            j += i
        if operator2 in j:
            while True:
                print(f'****Кабинет ползователя {operator2}****')
                print('------------------------------','\n''1-пополнит баланс','\n''2-снят денег со счёта','\n''3-покозать баланс','\n''4-возврашатся назад')
                operator3=int(input('что хотите сделат? '))
                if operator3==1:
                    add_to_balanc=float(input('сумма пополнения: '))
                    balanc+=add_to_balanc
                    balanc_12=balanc+(balanc/100*12)
                    balanc_24=balanc_12+(balanc_12/100*12)
                    balanc_36=balanc_24+(balanc_24/100*12)
                    sql.execute(f'UPDATE bank_users SET user_balanc={balanc}, balanc_in12={balanc_12}, balanc_in24={balanc_24}, balanc_in36={balanc_36} WHERE user_name="{operator2}"')
                    connection.commit()
                    print(f'баланс успещно пополнен в сумму {add_to_balanc}$')
                elif operator3==2:
                    operator4=input('1-частичное снятия денег \n2-снятие всех средств со счета\n')
                    if int(operator4)==1:
                        kesh_balanc=float(input('сумма снятия: '))
                        balanc-=kesh_balanc
                        balanc_12 = balanc + (balanc / 100 * 12)
                        balanc_24 = balanc_12 + (balanc_12 / 100 * 12)
                        balanc_36 = balanc_24 + (balanc_24 / 100 * 12)
                        sql.execute(f'UPDATE bank_users SET user_balanc={balanc}, balanc_in12={balanc_12}, balanc_in24={balanc_24}, balanc_in36={balanc_36} WHERE user_name="{operator2}"')
                        connection.commit()
                        print(f'с баланса успешно снято {kesh_balanc}$')
                    elif int(operator4)==2:
                        a=input('вы уверени? \nyes____or____no \n')
                        if a=='yes':
                            balanc-=balanc
                            balanc_12-=balanc_12
                            balanc_24-=balanc_24
                            balanc_36-=balanc_36
                            sql.execute(f'UPDATE bank_users SET user_balanc={balanc}, balanc_in12={balanc_12}, balanc_in24={balanc_24}, balanc_in36={balanc_36} WHERE user_name="{operator2}"')
                            connection.commit()
                            print(f'счёт ползовотеля {operator2} полностю опусташен')
                        elif a=='no':
                            pass
                        else:
                            print('не верный ответ')
                    else:
                        print("не верный выбор")
                elif operator3==3:
                    print(sql.execute(f'SELECT user_name, user_balanc+"{"$"}", balanc_in12+"{"$"}", balanc_in24"{"$"}", balanc_in36"{"$"}" FROM bank_users WHERE user_name="{operator2}";').fetchall())
                elif operator3==4:
                    break
                else:
                    print('не правилный действиа')
    elif operator1==4:
        s=sql.execute('SELECT * FROM bank_users;').fetchall()
        for i in s:
            print(i)
    elif operator1==5:
        break
    else:
        print("не правилный действиа")