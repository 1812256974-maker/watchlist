# 1. 从flask库导入核心类Flask
from flask import Flask, url_for, render_template
from markupsafe import escape

# 2. 创建Web应用实例app
app = Flask(__name__)

# 3. 路由装饰器：绑定访问地址 /、/index、/home 三个地址都访问这个页面
@app.route('/')
@app.route('/index')
@app.route('/home')
# 4. 定义处理主页请求的函数
def index():
    # 把页面需要的数据放到函数内（推荐规范写法）
    name = 'zhangjing'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': 1988},
        {'title': 'Dead Poets Society', 'year': 1989},
        {'title': 'A Perfect World', 'year': 1993},
        {'title': 'Leon', 'year': 1994},
        {'title': 'Mahjong', 'year': 1996},
        {'title': 'Swallowtail Butterfly', 'year': 1996},
        {'title': 'King of Comedy', 'year': 1999},
        {'title': 'Devils on the Doorstep', 'year': 1999},
        {'title': 'WALL-E', 'year': 2008},
        {'title': 'The Pork of Music', 'year': 2012},
    ]
    # 5. 渲染模板，传递name和movies变量
    return render_template('index.html', name=name, movies=movies)

# 用户动态路由（带安全转义）
@app.route('/user/<name>')
def user_page(name):
    return f'User: {escape(name)}'

# url_for 测试页面
@app.route('/test')
def test_url_for():
    # 修正：视图函数名是 index，不是 hello
    print(url_for('index'))
    print(url_for('user_page', name='zhangjing'))
    print(url_for('user_page', name='peter'))
    print(url_for('test_url_for'))
    print(url_for('test_url_for', num=2))
    return 'Test page — 去终端看打印的URL'

# 6. 判断：只有直接运行本文件时才执行下方代码
if __name__ == '__main__':
    # 7. 启动内置开发服务器，debug=True开启调试模式
    app.run(debug=True)