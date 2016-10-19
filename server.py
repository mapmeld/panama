# pip install web.py
import web
render = web.template.render('templates/')

urls = (
  '/', 'home',
  '/bootstrap.min.css', 'bootstrap'
)

class home:
    def GET(self):
        return render.home()

class bootstrap:
    def GET(self):
        f = open('static/bootstrap.min.css', 'r')
        content = f.read()
        f.close()
        return content

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
