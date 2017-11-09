from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect, send
# https://flask-socketio.readthedocs.io/en/latest/
# https://github.com/socketio/socket.io-client

app = Flask(__name__)

app.config[ 'SECRET_KEY' ] = 'jsbcfsbfjefebw237u3gdbdc'
socketio = SocketIO( app )
users = []
connections = []
dic = {}


@app.route( '/' )
def hello():
  return render_template( './ChatApp.html' )

def messageRecived():
  print( 'message was received!!!' )

@socketio.on( 'my event' )
def handle_my_custom_event( json ):
  print( 'recived my event: ' + str( json ) ) #user is the request.sid
  print ('current user id is: ' + request.sid)
  socketio.emit( 'my response', json, callback=messageRecived )



@socketio.on('join')
def on_join(data):
	username = data['username']
	domain = data['domain_name']
	join_room(domain)
	send(username + ' has entered your domain', room=domain)
	emit('enter domain', 'You entered ' + domain + 'successfully!', room=request.sid)


@socketio.on('leave')	
def on_leave(data):
	username = data['username']
	domain = data['domain_name']
	leave_room(domain)
	send(username + ' has left your domain', room=domain)
	emit('leave domain', 'You left ' + domain + 'successfully!', room=request.sid)



@socketio.on( 'change domain' )
def change_domain(data): 
	username = data['username']
	newdomain = data['domain_name']
	olddomain = dic[request.sid]
	dic[request.sid] = newdomain
	leave_room(olddomain)
	join_room(newdomain)
	send(username + ' has entered your domain', room=newdomain)
	emit('new domain', 'You entered ' + newdomain + ' successfully!', room=request.sid)

@socketio.on('send message')
def send_message(data):
	username = data['username']
	message = data['message']
	domain = dic[request.sid]
	emit('new message', {'msg': message, 'users': username}, room=domain)

@socketio.on('new user')
def new_user(data):
	username = data['username']
	users.append(username);
	domain = data['domain_name']
	dic[request.sid] = domain

	join_room(domain)
	send(username + ' has entered your domain', room=domain)
	emit('get domains', domain, room=request.sid)
	emit('get users', users, room=domain)


if __name__ == '__main__':
	socketio.run( app, debug = True )