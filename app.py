from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.exceptions import HTTPException, NotFound, InternalServerError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fishing_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # セッション管理のためのシークレットキー
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# モデル定義
class Season(db.Model):
    season_id = db.Column(db.Integer, primary_key=True)
    season_name = db.Column(db.String(50), nullable=False)

class Fish(db.Model):
    fish_id = db.Column(db.Integer, primary_key=True)
    fish_name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.String(50))
    habitat = db.Column(db.String(200))
    bait = db.Column(db.String(200))
    gear = db.Column(db.String(200))
    rod_image = db.Column(db.String(50))
    bait_image = db.Column(db.String(50))
    season = db.Column(db.String(50))

# エラーハンドリング
@app.errorhandler(HTTPException)
def handle_exception(e):
    flash(f"エラーが発生しました: {e.description}", 'danger')
    return redirect(url_for('index'))

@app.errorhandler(404)
def not_found_error(e):
    flash("ページが見つかりません。", 'warning')
    return redirect(url_for('index'))

@app.errorhandler(500)
def internal_error(e):
    flash("内部サーバーエラーが発生しました。", 'danger')
    return redirect(url_for('index'))

# 初期データの挿入
def insert_initial_data():
    db.create_all()
    if not Season.query.first():
        season_data = [
            {'season_name': '春'},
            {'season_name': '夏'},
            {'season_name': '秋'},
            {'season_name': '冬'}
        ]
        for season in season_data:
            db.session.add(Season(**season))
        
        fish_data = [
            {"fish_name": "アマゴ（ヤマメ）", "image": "amago.jpg", "habitat": "冷たい山間部の清流", "bait": "イクラ, ミミズ, 虫（クロカワムシ、カワゲラ）", "gear": "初心者: 短めの渓流竿（3.6m）、小型スピニングリール、4lbライン", "rod_image": "beginner_rod.jpg", "bait_image": "worm.jpg", "season": "春"},
            {"fish_name": "ニジマス", "image": "nijimasu.jpg", "habitat": "清流や渓流", "bait": "ペレット, ミミズ, 虫（カワゲラ）", "gear": "初心者: 3.6mの渓流竿、4lbライン、小型スピニングリール", "rod_image": "beginner_rod.jpg", "bait_image": "pellet.jpg", "season": "春"},
            {"fish_name": "ウグイ", "image": "ugui.jpg", "habitat": "清流や中流域", "bait": "ミミズ, イクラ, 練り餌", "gear": "初心者: 2.7mの小型の竿、ナイロンライン、ウキ釣りセット", "rod_image": "beginner_rod.jpg", "bait_image": "worm.jpg", "season": "春"},
            {"fish_name": "ハヤ", "image": "haya.jpg", "habitat": "清流や中流域", "bait": "ミミズ, パン, 練り餌", "gear": "初心者: 2.7mの小型の竿、ナイロンライン、ウキ釣りセット", "rod_image": "beginner_rod.jpg", "bait_image": "bread.jpg", "season": "春"},
            {"fish_name": "アユ", "image": "ayu.jpg", "habitat": "大きな川の中流域", "bait": "友釣り用の生きたアユ, イクラ", "gear": "初心者: 友釣り用の9mのアユ竿、ナイロンライン、ウキ仕掛け", "rod_image": "beginner_rod.jpg", "bait_image": "ayu_live.jpg", "season": "夏"},
            {"fish_name": "テナガエビ", "image": "tenagaebi.jpg", "habitat": "河口付近の汽水域", "bait": "ミミズ, 小さなエビ, 練り餌", "gear": "初心者: 1.8mのエビ用竿、細いナイロンライン、小型ウキ", "rod_image": "beginner_rod.jpg", "bait_image": "worm.jpg", "season": "夏"},
            {"fish_name": "オイカワ", "image": "oikawa.jpg", "habitat": "清流や中流域", "bait": "ミミズ, 練り餌, 虫（アカムシ）", "gear": "初心者: 2.1mの小型竿、ナイロンライン、小型ウキ", "rod_image": "beginner_rod.jpg", "bait_image": "worm.jpg", "season": "夏"},
            {"fish_name": "ナマズ", "image": "namazu.jpg", "habitat": "中流から下流域、湖沼", "bait": "ミミズ, 小魚, エビ", "gear": "初心者: 3mの強めの竿、ナイロンライン、ウキ仕掛け", "rod_image": "strong_rod.jpg", "bait_image": "small_fish.jpg", "season": "夏"},
            {"fish_name": "イワナ", "image": "iwana.jpg", "habitat": "冷たい山間部の渓流", "bait": "ミミズ, イクラ, 虫（カゲロウの幼虫）", "gear": "初心者: 3.6mの渓流竿、小型スピニングリール、4lbライン", "rod_image": "beginner_rod.jpg", "bait_image": "worm.jpg", "season": "秋"},
            {"fish_name": "ウグイ", "image": "ugui.jpg", "habitat": "清流や中流域", "bait": "ミミズ, イクラ, 練り餌", "gear": "初心者: 2.7mの小型の竿、ナイロンライン、ウキ釣りセット", "rod_image": "beginner_rod.jpg", "bait_image": "worm.jpg", "season": "秋"},
            {"fish_name": "カワムツ", "image": "kawamutsu.jpg", "habitat": "中流から下流域", "bait": "ミミズ, 練り餌, パン", "gear": "初心者: 2.1mの小型竿、ナイロンライン、小型ウキ", "rod_image": "beginner_rod.jpg", "bait_image": "worm.jpg", "season": "秋"},
            {"fish_name": "ブラックバス", "image": "blackbass.jpg", "habitat": "湖沼や緩やかな流れのある川", "bait": "ワーム, 小魚, 虫（カゲロウの幼虫）", "gear": "初心者: 2.7mのベイトロッド、ナイロンライン、スピナーベイト", "rod_image": "bait_rod.jpg", "bait_image": "worm.jpg", "season": "秋"},
            {"fish_name": "ニゴイ", "image": "nigoi.jpg", "habitat": "中流から下流域", "bait": "ミミズ, 練り餌, イクラ", "gear": "初心者: 3mの竿、ナイロンライン、ウキ仕掛け", "rod_image": "beginner_rod.jpg", "bait_image": "worm.jpg", "season": "冬"},
            {"fish_name": "コイ", "image": "koi.jpg", "habitat": "河口付近や大きな川の中流域", "bait": "ミミズ, 練り餌, パン", "gear": "初心者: 3.6mの強めの竿、ナイロンライン、ウキ仕掛け", "rod_image": "strong_rod.jpg", "bait_image": "worm.jpg", "season": "冬"},
            {"fish_name": "フナ", "image": "funa.jpg", "habitat": "池や湖、緩やかな流れのある川", "bait": "練り餌, ミミズ, パン", "gear": "初心者: 2.1mの小型竿、ナイロンライン、小型ウキ", "rod_image": "beginner_rod.jpg", "bait_image": "worm.jpg", "season": "冬"},
            {"fish_name": "ヤツメウナギ", "image": "yatsumeunagi.jpg", "habitat": "冷たい清流や渓流", "bait": "ミミズ, 小魚, 練り餌", "gear": "初心者: 2.7mの小型竿、ナイロンライン、小型ウキ", "rod_image": "beginner_rod.jpg", "bait_image": "worm.jpg", "season": "冬"}
        ]
        for fish in fish_data:
            db.session.add(Fish(**fish))
        
        db.session.commit()

@app.route('/')
def index():
    # ホームページをレンダリング
    return render_template('index.html')

@app.route('/fish/<season>')
def fish(season):
    # 季節名をマッピングする辞書
    season_map = {
        'all': '全ての季節',
        'spring': '春',
        'summer': '夏',
        'autumn': '秋',
        'winter': '冬'
    }
    season_name = season_map.get(season, '全ての季節')
    try:
        # 条件に応じて魚のリストを取得
        if season == 'all':
            fish_list = Fish.query.all()
        else:
            fish_list = Fish.query.filter_by(season=season_name).all()
    except Exception as e:
        flash('魚データの取得中にエラーが発生しました。', 'danger')
        return redirect(url_for('index'))
    
    # 魚のリストページをレンダリング
    return render_template('fish.html', fish_list=fish_list, season_name=season_name)

@app.route('/fish_detail/<int:fish_id>')
def fish_detail(fish_id):
    try:
        # 魚の詳細情報を取得
        fish = Fish.query.get_or_404(fish_id)
    except Exception as e:
        flash('魚の詳細データの取得中にエラーが発生しました。', 'danger')
        return redirect(url_for('index'))
    
    # 魚の詳細ページをレンダリング
    return render_template('fish_detail.html', fish=fish)

if __name__ == '__main__':
    with app.app_context():
        insert_initial_data()
    app.run(debug=True)
