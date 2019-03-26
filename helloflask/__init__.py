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
    all_data = request.json

    title = all_data['title']
    duedate = all_data['duedate']
    money = all_data['money']
    practice = all_data['practice_time']
    perform = all_data['perform_time']
    prac_address = all_data['practice_address']
    perf_address = all_data['perform_address']
    detail_textarea = all_data['detail_info']
    song_textarea = all_data['song_info']
    costume = all_data['costume']
    qualification =all_data["qualification"]
    gender = all_data["gen"]
    instruments = all_data["instruments"]


    print (title, "\n", duedate, money, practice, perform, prac_address, perf_address, detail_textarea, song_textarea, costume, qualification, gender, instruments)
    
    b = Board( title, duedate, qualification , gender, money, practice, perform, costume, prac_address, perf_address, detail_textarea, song_textarea, '2')
        
    try:
        db_session.add(b)
        db_session.commit()
    
    except Exception as err:
        print (err)
        db_session.rollback()

    return render_template('/perform')
# for instrument in instruments:

        
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

