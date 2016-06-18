import json
from channels import Channel
import copy
from .models import WaitRoom, Message, Crowd, Crowd_Members
import re
import json
import logging
from channels import Group
from channels.sessions import channel_session
import redis

redis_conn = redis.Redis("localhost", 6379)
log = logging.getLogger(__name__)
@channel_session
def wait_connect(message):
    try:
	log.debug('In the try block of ws_connect')#added by me
        #you can do a check for message path \wait if you want
	title = "wait2"
        
    	if WaitRoom.objects.filter(title=title).exists() :
            #do nothing
	    wait_room = WaitRoom.objects.get(title=title)
	else :
            wait_room = WaitRoom.objects.create(title=title)

    except WaitRoom.DoesNotExist:
        log.debug('ws room does not exist title=%s', title)
	#WaitRoom.objects.create(title=title)
	#log.debug('ws room new object created with title=%s',title)#You have to load the page when it is created
        return

    log.debug('wait connect room=%s client=%s:%s', 
        wait_room.title, message['client'][0], message['client'][1])
    #redis_conn.sadd("waitroom", message.reply_channel.name)
    redis_conn.sadd("waitroom",message['client'])
    #global client_current 
    #client_current = copy.deepcopy(message['client'])
    #log.debug(client_current)
    #client_current[0] = message['client'][0]
    #client_current[1] = message['client'][1]
    #redis_conn.setex("waitroom", 20, message['client'])
    Group('wait-'+title, channel_layer=message.channel_layer).add(message.reply_channel)
    message.channel_session['wait_room'] = wait_room.title



@channel_session
def wait_receive(message):
    # Look up the wait room from the channel session, bailing if it doesn't exist
    try:
        title = message.channel_session['wait_room']
        wait_room = WaitRoom.objects.get(title=title)
    except KeyError:
        log.debug('no wait-room in channel_session')
        return
    except WaitRoom.DoesNotExist:
        log.debug('recieved message, buy wait-room does not exist label=%s', title)
        return

    try:
        data = json.loads(message['text'])
    except ValueError:
        log.debug("ws message isn't json text=%s", text)
        return
    cnt = 0 
    for message['client'] in redis_conn.smembers("waitroom"):
	#log.debug("all message clients are= %s:%s",message['client'][0],message['client'][1])
	cnt = cnt + 1
    log.debug("No of clients: %d",cnt)
    log.debug(redis_conn.smembers("waitroom"))
    log.debug("the no of clients: %d",redis_conn.scard("waitroom"))
    cnt = redis_conn.scard("waitroom")
    #for mvar in redis_conn.smembers("wait-"+title):
	#log.debug("various channels connected are=%s",message.reply_channel.name)
	#cnt= cnt + 1   
    #log.debug("total no of mvar: %d",cnt)
        #Channel(channel).send(content=content, binary=False)

    if data:
	log.debug('chat message room=%s message=%s', 
            wait_room.title, data['message'])
	log.debug(json.dumps(data))
        m = wait_room.messages.create(**data)
	log.debug("Successful models.py")        
	log.debug(json.dumps(m.as_dict()))
	# See above for the note about Group
        if cnt >= 3:
		#check crowd id of empty crowd
		which_crowd = Crowd.objects.Crowd_which_assign()



		#CHAT_COMMUNICATION = '_chat'
		#FORUM_COMMUNICATION = '_forum'
		#crowds = Crowd.objects.all()
		#which_crowd = 0
		
		



		log.debug("which_crowd=%d",which_crowd)
		crowd =  Crowd.objects.get(id = which_crowd)
		# 3 members to insert in crowd members //-cohort-id logic-so it's unique for each cohort--function that returns max cohort in the table & increment that
		#value & insert it into the table-- also take into account of inserting 1st cohort
		#crowd_id = which_crowd
		#c = Crowd_Members(crowd_id = which_crowd,worker_id='WorkerId1',cohort_id=1)
		#c.save()
		c = {}
		c['crowd_id'] = crowd
		c['worker_id'] = 'WorkerId1'
		c['cohort_id'] = 1
		
		crowd.members.create(**c)
		c['worker_id'] = 'Worker2'
		crowd.members.create(**c)
		c['worker_id'] = 'Worker3'
		crowd.members.create(**c)
		log.debug("3 objects created in crowd_members..check your database now")
		#update the message m with the url to be directed onto == url -label== room(crowd-id) == url= chat/forum
		#fetch the object for which crowd & look up the object if it has chat/forum
		t = {}		
		if crowd.communication == '_forum':
				t['message']='http://127.0.0.1:8000/forum/room'
		elif crowd.communication == '_chat':
				t['message']='http://127.0.0.1:8000/chat/room'
		t['message'] += str(which_crowd)
		Group('wait-'+title, channel_layer=message.channel_layer).send({'text': json.dumps(t)})
	#log.debug(title)
	#log.debug(message.channel_layer)
	log.debug("after if & group")
	

@channel_session
def wait_disconnect(message):
    try:
	log.debug('try block of disconnect')
	#disconnect.debug("%s : %s", message['client'][0], message['client'][1])
        title = message.channel_session['wait_room']
        wait_room = WaitRoom.objects.get(title=title)
	log.debug('before redis delete..client_current= ')
	#log.debug(client_current)
        #redis_conn.srem("waitroom", message['client'])
        client_pop = redis_conn.spop("waitroom")
	log.debug('client_pop=')
	log.debug(client_pop)
	#log.debug('Client disconnect = %s : %s', message['client'][0],message['client'][1])
 	
	#Problem-Not displaying message'client' anywhere  & the global variable has the last socket connected info..!! log.debug(message['client'])
	#I can get the count of how many there but not which clients are there..maybe I should try that piece with client js code    	
	#log.debug(highon)
	#redis_conn.srem("waitroom", client_current)
	log.debug("After disconnect.. the no of clients: %d",redis_conn.scard("waitroom"))
	log.debug(redis_conn.smembers("waitroom"))
	Group('wait-'+title, channel_layer=message.channel_layer).discard(message.reply_channel)
    except (KeyError, WaitRoom.DoesNotExist):
        pass





