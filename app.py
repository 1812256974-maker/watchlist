# 基础Flask导入
from flask import Flask, url_for, render_template
from markupsafe import escape
# SQLAlchemy数据库相关导入
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from pathlib import Path
# 命令行工具click
import click
import sys
from sqlalchemy import select


# 创建应用实例
app = Flask(__name__)

# SQLite数据库配置
SQLITE_PREFIX = 'sqlite:///' if sys.platform.startswith('win') else 'sqlite:////'
db_path = Path(__file__).parent / "watchlist.db"
app.config["SQLALCHEMY_DATABASE_URI"] = SQLITE_PREFIX + str(db_path)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# SQLAlchemy 基类
class Base(DeclarativeBase):
    pass

# 初始化数据库对象
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# 数据库模型：用户表
class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20))

# 数据库模型：电影表
class Movie(db.Model):
    __tablename__ = "movie"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(60))
    year: Mapped[str] = mapped_column(String(4))

# 自定义Flask命令：初始化数据库
@app.cli.command("init-db")
@click.option("--drop", is_flag=True, help="先删除所有表再重建")
def init_database(drop):
    """初始化数据库表"""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo("数据库表初始化完成！")

import click

@app.cli.command()
def forge():
    """Generate fake data."""
    db.drop_all()
    db.create_all()

    # 全局的两个变量移动到这个函数内
    name = 'Zhang Jing'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')

# 首页路由
@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    # 查询单条用户记录
    # user = db.session.execute(select(User)).scalar()
    # 查询全部电影记录
    movies = db.session.execute(select(Movie)).scalars().all()
    # 将数据传给 index.html 模板
    return render_template('index.html',  movies=movies)  #user=user,

# 用户动态路由
@app.route("/user/<name>")
def user_page(name):
    return f"User: {escape(name)}"

# url_for测试路由
@app.route("/test")
def test_url_for():
    print(url_for("index"))
    print(url_for("user_page", name="zhangjing"))
    print(url_for("user_page", name="peter"))
    print(url_for("test_url_for"))
    print(url_for("test_url_for", num=2))
    return "Test page — 查看终端打印的URL"

@app.errorhandler(404)
def page_not_found(error):
    user = db.session.execute(select(User)).scalar()
    return render_template('404.html'), 404  #,user=user

# 模板上下文处理器：全局注入user变量到所有模板
@app.context_processor
def inject_user():
    user = db.session.execute(select(User)).scalar()
    return dict(user=user)

# 程序启动入口
if __name__ == "__main__":
    app.run(debug=True)