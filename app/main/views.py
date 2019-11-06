from . import main


@main.route('/')
def index():
    # return redirect('/test3')#render_template('index22.html')
    return "success"
