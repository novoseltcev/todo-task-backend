from server import app, db
from flask import request, render_template


@app.route("/create", methods=['POST'])
def add_task():
    db.append(request.form.get('new_task_name'))
    db.serialization()
    return render_template("index.html", tasks=db.dictionary)


@app.route("/delete", methods=['POST'])
def remove_task():
    db.remove(int(list(request.form.keys())[0]))
    db.serialization()
    return render_template("index.html", tasks=db.dictionary)


@app.route("/switch", methods=['POST'])
def switch_task():
    db.switch_competition(int(list(request.form.keys())[0]))
    db.serialization()
    return render_template("index.html", tasks=db.dictionary)
