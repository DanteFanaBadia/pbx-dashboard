from app import config as app_config
from app.extensions import api, ma, sk, db
from sqlalchemy import func, desc
from sqlalchemy.sql import label
from flask import Flask, render_template, jsonify
from time import sleep
from threading import Thread, Event
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

thread = Thread()
thread_stop_event = Event()


class CDR(db.Model):
    __tablename__ = 'cdr'
    uniqueid = db.Column(db.String(32), primary_key=True)
    calldate = db.Column(db.DateTime())
    clid = db.Column(db.String(80))
    src = db.Column(db.String(80))
    dst = db.Column(db.String(80))
    dcontext = db.Column(db.String(80))
    channel = db.Column(db.String(80))
    dstchannel = db.Column(db.String(80))
    lastapp = db.Column(db.String(80))
    lastdata = db.Column(db.String(80))
    duration = db.Column(db.String(80))
    billsec = db.Column(db.String(80))
    disposition = db.Column(db.String(80))
    amaflags = db.Column(db.String(80))
    accountcode = db.Column(db.String(20))
    userfield = db.Column(db.String(255))
    did = db.Column(db.String(50))
    recordingfile = db.Column(db.String(255))
    cnum = db.Column(db.String(80))
    cnam = db.Column(db.String(80))
    outbound_cnum = db.Column(db.String(80))
    outbound_cnam = db.Column(db.String(80))
    dst_cnam = db.Column(db.String(80))
    linkedid = db.Column(db.String(32))
    peeraccount = db.Column(db.String(80))
    sequence = db.Column(db.Integer)


class CDRSchema(ma.Schema):
    class Meta:
        fields = ('calldate', 'src', 'dst', 'disposition', 'duration', 'billsec', 'calldate')

cdr_schema = CDRSchema()
cdrs_schema = CDRSchema(many=True)


class NotificationThread(Thread):

    def __init__(self, app):
        self.delay = 1
        self.app = app
        super(NotificationThread, self).__init__()

    def get_total_call(self):
        engine = create_engine(app_config.BaseConfig.SQLALCHEMY_DATABASE_URI)
        Session = sessionmaker(bind=engine, autocommit=True)
        session = Session()
        session.begin()
        count = session.query(CDR.uniqueid).count()
        session.commit()
        return count

    def notified(self):
        current_count = self.get_total_call()
        new_count = current_count
        while not thread_stop_event.isSet():
            new_count = self.get_total_call()
            if current_count < new_count:
                sk.emit('notified', new_count, namespace='/notification')
                current_count = new_count
            sleep(self.delay)

    def run(self):
        self.notified()


def create_app(config=app_config.DevConfig):
    app = Flask(__name__)
    app.config.from_object(config)
    register_extensions(app)

    def get_dashboard_data(session):
        top_make_calls = list(session.query(CDR.src, label('call', func.count(CDR.uniqueid))).order_by(desc('2'))
                              .group_by(CDR.src).limit(5).all())
        top_got_calls = list(session.query(CDR.dst, label('call', func.count(CDR.uniqueid))).order_by(desc('2'))
                             .group_by(CDR.dst).limit(5).all())
        top_unanswer_calls = list(session.query(CDR.dst, label('call', func.count(CDR.uniqueid))).order_by(desc('2'))
                                  .group_by(CDR.dst).filter_by(disposition='NO ANSWER').limit(5).all())
        data = {
            'calls': cdrs_schema.dump(CDR.query.order_by(CDR.calldate).all()).data,
            'total_calls': session.query(func.count(CDR.uniqueid)).scalar(),
            'total_unanswer': session.query(func.count(CDR.uniqueid)).filter_by(disposition='NO ANSWER').scalar(),
            'top_make_calls': top_make_calls,
            'top_got_calls': top_got_calls,
            'top_unanswer_calls': top_unanswer_calls,
            'total_ext_active': session.query(CDR.src.distinct().label("src")).count()
        }
        return data

    @sk.on('connect', namespace='/notification')
    def connect():
        global thread
        print('Client connected')
        if not thread.isAlive():
            thread = NotificationThread(app)
            thread.start()

    @sk.on('disconnect', namespace='/notification')
    def disconnect():
        print('Client disconnected')

    @app.route('/', methods=['GET'])
    def index():
        return render_template('index.html')

    @app.route('/dashboard', methods=['GET'])
    def dashboard():
        return jsonify(get_dashboard_data(db.session))

    return app


def register_extensions(app):
    db.init_app(app)
    api.init_app(app)
    ma.init_app(app)
    sk.init_app(app)
