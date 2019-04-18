import random
import pymysql
from random import randrange
import datetime, time

def random_date():
    random_days = randrange(int_delta)
    return d1 + datetime.timedelta(days=random_days)

d1 = datetime.datetime.strptime('2019/4/16', '%Y/%m/%d')
d2 = datetime.datetime.strptime('2021/12/31', '%Y/%m/%d')
int_delta = (d2 - d1).days

places = ["서울","경기","인천","강원","충북", "세종","충남", "대전", "대구", "경북", "경남", "부산", "울산", "전북", "전남","광주","제주"]
perftitles = ["유치원", "예술의 전당", "웨딩", "워커힐 호텔", "기업행사", "양재 엘타워", "서울스프링페스티벌", "엘지아트센터", "롯데콘서트홀", "라움아트센터", "대구 콘서트하우스","인천아트센터"]
gens = ["0","1","2","3"]
qualifications = ["0","1","2","3"]
num = ["0","1","2","3","4","5","6","7","8","9"]
albe = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","0","1","2","3","4","5","6","7","8","9"]
parts = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17"]
performs_detail = []
# users_detail = [("better3311@naver.com", "1q2w3e", "배준홍", "010-4321-4321", "배럴이왔어요", "서울"), ("joe753@naver.com", "1234", "이현욱", "01012341234", "운영자새끼", "서울")]
users_detail = []
i = 1
perflen = len(perftitles)
while len(performs_detail)<200:
    perform_address = random.choice(places)
    practice_address = random.choice(places)
    qualification = random.choice(qualifications)
    gen = random.choice(gens)
    money = randrange(100000, 3000000, step=100000, _int=int)
    practice_time = randrange(1, 5, step=1, _int=int)
    perform_time = round(practice_time / 2,0)
    costume = randrange(1,4,step=1,_int=int)
    practice_mapx = random.uniform(126.856114, 128.553447)
    practice_mapy = random.uniform(35.221932, 37.750555)
    perform_mapx = random.uniform(126.856114, 128.553447)
    perform_mapy = random.uniform(35.221932, 37.750555)
    board_title = perftitles[random.randrange(perflen)] + "공연"
    detail_info = "디테일 " + perform_address + "공연"
    song_info = "곡 " + perform_address
    user_id = i
    emailst = random.choices(albe, k = random.randrange(6,14))
    email = "".join(emailst)
    password = i
    name = "user" + str(i)
    mid_num = random.choices(num, k = 4)
    midnum = "".join(mid_num)
    end_num = random.choices(num, k = 4)
    endnum = "".join(end_num)
    phone_number = "010-{}-{}".format(midnum, endnum)
    address = random.choice(places)
    nickname = "nickname" + str(i)
    if perform_address == "서울":
        area_number = 1
    elif perform_address == "경기":
        area_number = 2
    elif perform_address == "인천":
        area_number = 3
    elif perform_address == "강원":
        area_number = 4
    elif perform_address == "충북" or perform_address == "세종":
        area_number = 5
    elif perform_address == "충남" or perform_address == "대전":
        area_number = 6
    elif perform_address == "경북" or perform_address == "대구":
        area_number = 7
    elif perform_address == "경남" or perform_address == "부산" or perform_address == "울산":
        area_number = 8
    elif perform_address == "전북":
        area_number = 9
    elif perform_address == "전남" or perform_address == "광주":
        area_number = 10
    else:
        area_number = 11
    # emailaddr = "".join(email_addr)
    due_date = random_date()
    # addr = random.choice(places)
    i += 1
    users_detail.append(("{}@gamil.com".format(email),
                         password,
                         name,
                         phone_number,
                         nickname,
                         address
                         ))

    performs_detail.append((board_title,
                            due_date, 
                            qualification, 
                            gen, 
                            money, 
                            practice_time, 
                            perform_time, 
                            costume, 
                            practice_address, 
                            practice_mapx, 
                            practice_mapy, 
                            perform_address, 
                            area_number, 
                            perform_mapx, 
                            perform_mapy, 
                            detail_info, 
                            song_info, 
                            user_id))
    print("data{} inserting is done".format(i))
    


# print(performs_detail)
# print(users_detail)

# exit()

conn = pymysql.connect(host='34.85.1.117', user='root', password='allclassic', port=3306, db='allclassic', charset='utf8')

with conn:
    cur1 = conn.cursor()
    sql1 = """insert into Board(board_title, 
                               due_date, 
                               qualification, 
                               gen, 
                               money, 
                               practice_time, 
                               perform_time, 
                               costume, 
                               practice_address, 
                               practice_mapx, 
                               practice_mapy, 
                               perform_address, 
                               area_number, 
                               perform_mapx, 
                               perform_mapy, 
                               detail_info, 
                               song_info, 
                               user_id) values(%s, %s, %s, %s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s)"""
    cur1.executemany(sql1, performs_detail)

    cur2 = conn.cursor()
    sql2 = """insert into Users(email, 
                               password, 
                               name, 
                               phone_number, 
                               nickname, 
                               address) values(%s, sha2(%s,0), %s, %s, %s, %s)"""
    cur2.executemany(sql2, users_detail)
    conn.commit()

with conn:
    cur = conn.cursor()
    sqlbis = "select board_id from Board"
    cur.execute(sqlbis)
    board_ids = cur.fetchall()
# print(board_ids)
BI_detail = []
for board_id in board_ids:
    instruments = random.sample(parts, random.randrange(1,8))
    for instrument_id in instruments:
        person = random.randrange(1,3)
        BI_detail.append((str(board_id[0]), instrument_id, str(person)))
        print((str(board_id[0]), instrument_id, str(person)))

with conn:
    cur = conn.cursor()
    sqlbii = """insert into BoardInstrument(board_id, instrument_id, person) values(%s,%s,%s)"""
    cur.executemany(sqlbii, BI_detail)
    conn.commit()

print( "done!!!!")