import flask, flask.views
app = flask.Flask(__name__)

from flask import request
import json

class View(flask.views.MethodView):
    def get(self, command=None):
    	dict ={}

    	#creating an array of parameters
    	params = 'email,name,start_arr,dest_arr,info,comments,rating'
    	params = params.split(',')
    	
    	#creating a dictionary of url parameters
    	for param in params:
            dict[param] = request.args.get(param) or 'N/A'

    	file = open('/home/sauravtom/public_html/carpool.json', 'a+') 
    	#w+ will create the file if it doesn't exist but will erase any previous data
    	#a+ will read and append to the file
    	#exception handling for the case where file is empty
    	try: 
            arr = eval(file.read())
    	except SyntaxError:
            arr=[]
    	
    	#creating an array of all the emails in the database
    	email_arr = [i['email'] for i in arr]
    	#appending the default value so that no field without email is passed in db, as it will be outcasted in the next step
    	email_arr.append('N/A')
        
        #return a 500 is email is not in the arguments
        if dict['email'] == 'N/A':
            return "{'status':500,\n\t'response':'missing quintessential argument email'}"

    	# if email is already present,do not proceed further
    	if dict['email'] in email_arr:
            #get the index where the element already is
            i = email_arr.index(dict['email'])
            #update the element in arr arr
            arr[i] = dict
        else:
            #we got a new entry so just append it
            arr.append(dict)
    	
    	with open('/home/sauravtom/public_html/carpool.json', 'w') as file:
    	    file.write(json.dumps(arr))

        return "{'status':200,\n\t'response':'record updated for email %s'}"%(dict['email'])

app.add_url_rule('/add', view_func=View.as_view('main'))

app.debug = True
app.run(host='0.0.0.0')
