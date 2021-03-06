import sqlite3
from flask import Flask, g, render_template, request, redirect, flash

app = Flask(__name__)
DATABASE = "plants.db"
app.secret_key = "supergirl07"

def get_db():
    #connects database "plants.db" to Python file.
    db = getattr (g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    #error check for previous function "get_db()".
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

@app.route ("/")
def home():
    #home page, where user is presented with links to other pages.
    return render_template("home.html")

@app.route ("/repository") 
def repository():
    #repository page, where all data are displayed in a table.
    cursor = get_db().cursor()
    #sql statement, displaying data from foreign key onto primary key.
    sql = "SELECT herb.id, herb.name, rarity.level, type.classification, herb.place_of_origin, herb.description, use.category FROM herb JOIN rarity ON herb.rarity = rarity.id JOIN type ON herb.type = type.id JOIN use ON herb.use = use.id"
    if request.args.get ('name')  == 'a-z': #sort by name (a-z).
        sql += " ORDER BY herb.name"
    elif request.args.get ('name') == 'z-a': #sort by name (z-a).
        sql += " ORDER BY herb.name DESC"
    elif request.args.get ('rarity') == 'common': #sort by rarity (common).
        sql += " WHERE rarity.level='common'"
    elif request.args.get ('rarity') == 'rare':#sort by rarity (rare).
        sql += " WHERE rarity.level='rare'"
    elif request.args.get ('rarity') == 'unique': #sort by rarity (unique).
        sql += " WHERE rarity.level='unique'"
    elif request.args.get ('type') == 'flower': #sort by type (flower).
        sql += " WHERE type.classification='flower'" 
    elif request.args.get ('type') == 'fruit':  #sort by type (fruit).
        sql += " WHERE type.classification='fruit'"
    elif request.args.get ('type') == 'leaf': #sort by type (leaf).
        sql += " WHERE type.classification='leaf'"
    elif request.args.get ('type') == 'root': #sort by type (root).
        sql += " WHERE type.classification='root'"
    elif request.args.get ('type') == 'seed': #sort by type (seed).
        sql += " WHERE type.classification='seed'"
    elif request.args.get ('use') == 'anxiety': #sort by use (anxiety).
        sql += " WHERE use.category='anxiety'"
    elif request.args.get ('use') == 'fever': #sort by use (fever).
        sql += " WHERE use.category='fever'"
    elif request.args.get ('use') == 'flu': #sort by use (flu).
        sql += " WHERE use.category='flu'"
    elif request.args.get ('use') == 'headache': #sort by use (headache).
        sql += " WHERE use.category='headache'"
    elif request.args.get ('use') == 'heart disease': #sort by use (heart disease).
        sql += " WHERE use.category='heart disease'"
    elif request.args.get ('use') == 'inflammation': #sort by use (inflammation).
        sql += " WHERE use.category='inflammation'"
    elif request.args.get ('use') == 'insomnia': #sort by use (insomnia).
        sql += " WHERE use.category='insomnia'"
    elif request.args.get ('use') == 'skin conditions': #sort by use (skin conditions).
        sql += " WHERE use.category='skin conditions'"
    elif request.args.get ('use') == 'stomach upsets': #sort by use (stomach upsets).
        sql += " WHERE use.category='stomach upsets'"
    elif request.args.get ('use') == 'wound healing': #sort by use (wound healing).
        sql += " WHERE use.category='wound healing'"
    cursor.execute(sql)
    results = cursor.fetchall()
    if results == None:
        return redirect ("/error")
    else: 
        return render_template("repository.html", results=results)

@app.route ("/search", methods=["POST", "GET"])
def search():
    #search bar, allows user to search for a specific herb and redirects them to the specific page for that herb.
    if request.method == "POST":
        print (request.form.get("filter"))
        cursor = get_db().cursor()
        sql = "SELECT * FROM herb WHERE name LIKE ?"
        cursor.execute (sql, (request.form.get("filter"),))
        results = cursor.fetchone()
        if results == None:
            return redirect ("/error")
        else: 
            print (f"results={results}")
            return redirect (f"/herb/{results[0]}")

@app.route ("/herb/<int:id>")
def herb(id):
    #page that displays all the information about the specific herb the user has searched for.
    cursor = get_db().cursor()
    sql = "SELECT herb.id, herb.name, rarity.level, type.classification, herb.place_of_origin, herb.description, herb.image, use.category, herb.explanation FROM herb JOIN rarity ON herb.rarity = rarity.id JOIN type ON herb.type = type.id JOIN use ON herb.use = use.id WHERE herb.id = ?"
    cursor.execute(sql, (id,))
    result = cursor.fetchone()
    return render_template("herb.html", result=result)

@app.route ("/about")
def about():
    #about page, provides user with more information about the website.
    return render_template("about.html")

@app.route ("/contact")
def contact():
    #contact page, displays email and other information.
    return render_template("contact.html")

@app.route ("/message", methods=["POST"])
def message():
    #allows user to input their name, email and message as contact.
    cursor = get_db().cursor()
    user_first_name = request.form["user_first_name"]
    user_last_name = request.form["user_last_name"]
    user_email = request.form["user_email"]
    user_message = request.form["user_message"]
    sql = "INSERT INTO contact(user_first_name, user_last_name, user_email, user_message) VALUES (?, ?, ?, ?)"
    cursor.execute(sql,(user_first_name, user_last_name, user_email, user_message))
    get_db().commit()
    flash ("Thank you for your time! We will get back to you shortly.", "response")
    return redirect ("/contact")

@app.route ("/error")
def error():
    #error page, for when user input returns no results.
    return render_template("error.html")

if __name__ == "__main__":
    app.run(debug=True)