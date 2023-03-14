from app import app

app.config.from_object('config.DevelopmentConfig')

app.run(host='0.0.0.0',port='5001')#debug=True

#app.config['debug']=True
#app.debug=True