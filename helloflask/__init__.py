from flask import Flask, g, request, Response, make_response, flash, redirect, jsonify
import json
from flask import session, render_template, Markup
from datetime import date, datetime
from helloflask.db_tables import User, Board, Instrument
from helloflask.init_db import db_session
from sqlalchemy.orm import subqueryload, joinedload
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func

app = Flask(__name__)
app.debug = True
# app.jinja_env.trim_blocks = True


@app.route('/lesson')
def lesson():
    return render_template('lesson.html')

@app.route('/perform/detail/board01')
def p_bbs01():
    row = ["title","기간","user0222"]
    return render_template('board01.html', lst=row)

@app.route('/add/perform/pboard01')
def add_pboard():
    return render_template('add_board.html')

@app.route('/perform')
def perform():
    return render_template('perform.html')

@app.route('/ch_user')
def cg_premium():
    return render_template('cg_premium.html')


@app.route('/test333')
def practice_handlebars() :
    return render_template('test333.html') 

@app.route('/perform/board/<boardid>', methods=["GET"])
def board (boardid) : 
    boardtb = Board.query.params(
        boardid=boardid).order_by(Board.board_id.desc()).all()
    return jsonify([s.json() for s in boardtb])

@app.route('/instrument', methods=["GET"])
def get_instrument () : 
    instruments = Instrument.query.all()
    return jsonify([inst.json() for inst in instruments])


@app.route('/signup', methods=['GET', 'POST'])
def signup_modal():
    email = request.form.get('email')
    password = request.form.get('password')
    cfpassword = request.form.get('cfpassword')
    name = request.form.get('name')
    phone_number = request.form.get('phone')
    nickname = request.form.get('nickname')
    address = request.form.get('address')

    if password != cfpassword :
        flash("암호를 입력주세요!!!")

    else :
        u = User( email, password, name, phone_number, nickname, address)
        print (u)
        try:
            db_session.add(u)
            db_session.commit()
        
        except Exception as err:
            print (err)
            db_session.rollback()

        return redirect('/perform')



@app.route('/sendboard', methods=['GET', 'POST'])
def sendboard():
    print ("OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOKKKKKKKKKKKKKKKKKKKKKKKKKKK")
    title = request.form.get('title')
    duedate = request.form.get('duedate')
    money = request.form.get('money')
    practice = request.form.get('practice_time')
    perform = request.form.get('perform_time')
    prac_address = request.form.get('practice_address')
    perf_address = request.form.get('perform_address')
    detail_textarea = request.form.get('detail_info')
    song_textarea = request.form.get('song_info')
    costume = request.form.get('costume')
    qualification = request.form.get("qualification")
    gender = request.form.get("gen")
    instruments = request.form.get("instruments")
    # instruments = request.get_json("instruments")
    a = request.json
    print(a['title'])


    # print (title, "\n", duedate, money, practice, perform, prac_address, perf_address, detail_textarea, song_textarea, costume, qualification, gender, instruments)
    # if password != cfpassword :
    #     flash("암호를 입력주세요!!!")

    # else :
    #     u = User( email, password, name, phone_number, nickname, address)
    #     print (u)
    #     try:
    #         db_session.add(u)
    #         db_session.commit()
        
    #     except Exception as err:
    #         print (err)
    #         db_session.rollback()

    #     return redirect('/add/perform/pboard01')

# @app.route('/sendboard', methods = ['POST'])
# def sendboard():

@app.route('/<username>')
def show_user(username):
    return username

