from flask import Flask, Blueprint, current_app, render_template, make_response, request, redirect, url_for
import requests
import json


app = Blueprint('app', __name__, url_prefix='/')

@app.route('/')
def index():
    api_url = f'{current_app.config["API_URL"]}/poems' 
    data = { "pag": 1, "p_pag": 10 }
    headers = { "Content-Type": "application/json" }
    response = requests.get(api_url, json=data, headers=headers)
    print(response.status_code)  
    print(response.text)
    poems = json.loads(response.text)
    print(poems)
    return render_template('main.html', poems=poems["poems"])


@app.route('/login', methods=['GET','POST'])
def login():
    if (request.method == 'POST'):
        email = request.form['email']
        password = request.form['password']
        print(email, password)

        if email != None and password != None: 
            #url que utilizamos en insomnia
            api_url = f'{current_app.config["API_URL"]}/auth/login'
            data = {"email" : email, "password" : password}
            headers = {"Content-Type" : "application/json"}
            response = requests.post(api_url, json = data, headers = headers) 
            print("login", response)
            if (response.ok): 

                response = json.loads(response.text)
                token = response["access_token"]
                user_id = str(response["id"])

                response = make_response(redirect(url_for('app.user_main')))
                response.set_cookie("access_token", token)
                response.set_cookie("id", user_id)
                return response
                #return render_template('login.html')
        return(render_template('login.html', error = "Usuario o contraseña incorrectos"))
    else:
        return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

''' 
@app.route('/home')
def user_main():
    if request.cookies.get('access_token'):
        api_url = f'{current_app.config["API_URL"]}/poems' 
        data = { "pag": 1, "p_pag": 10 }
        headers = { "Content-Type": "application/json" }
        response = requests.get(api_url, json=data, headers=headers)
        print(response.status_code)  
        print(response.text)
        poems = json.loads(response.text)
        print(poems)
        return render_template('main.html', poems=poems["poems"])    
    else:
        return redirect(url_for('app.login'))
'''

@app.route('/profile')
def user_profile():
    if request.cookies.get('access_token'):
        api_url = f'{current_app.config["API_URL"]}/poems'
        
        data = { "pag": 1, "p_pag": 10 }

        headers = { "Content-Type": "application/json" }

        response = requests.get(api_url, json=data, headers=headers) 
        
        return render_template('user_profile.html', poems = ["Poems"])
    else:
        return redirect(url_for('app.login'))

@app.route('/view/poem/<int:id>', methods=['GET'])
def view_poem(id):
    api_url = f'{current_app.config["API_URL"]}/poem/{id}'
    headers = {"Content-Type" : "application/json"}
    response = requests.get(api_url, headers=headers)
    poem = json.loads(response.text)
    return render_template('poem.html', poem = poem)

@app.route('/logout')
def logout():
    req = make_response(redirect(url_for('app.index')))
    req.delete_cookie("access_token")
    req.delete_cookie("id")
    return req

@app.route('/poem/create', methods=['GET','POST'])
def create_poem():
    jwt = request.cookies.get('access_token')
    if jwt:
        if request.method == 'POST':
            titulo = request.form['titulo']
            cuerpo = request.form['cuerpo']
            print(titulo)
            print(cuerpo)
            user_id = request.cookies.get("id")
            print(user_id)
            data = {"titulo": titulo, "cuerpo": cuerpo, "user_id": user_id  }
            print(data)
            headers = {"Content-Type" : "application/json", "Authorization" : f"Bearer {jwt}"}
            if titulo != "" and cuerpo != "":
                response = requests.post(f'{current_app.config["API_URL"]}/poems', json=data, headers=headers)
                print(response)
                if response.ok:
                    response = json.loads(response.text)
                    return redirect(url_for('app.view_poem', id=response["id"], jwt=jwt))
                else:
                    return redirect(url_for('app.create_poem'))
            else:
                return redirect(url_for('app.create_poem'))
        else:
            return render_template('update.html', jwt=jwt)
    else:
        return redirect(url_for('app.login'))

@app.route('/poem/<int:id>/delete')
def delete_poem(id):
    if request.cookies.get('accsess_token'):
        api_url = f'{current_app.config["API_URL"]}/poem/{id}'
        headers = {"Content-Type" : "application/json"}
        response = requests.delete(api_url, headers=headers)
        return response