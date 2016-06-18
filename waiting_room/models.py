import json
from django.db import models
from django.utils.six import python_2_unicode_compatible 
from django.utils import timezone
from channels import Group
import logging
from django.db.models import Count
#from .settings import MSG_TYPE_MESSAGE

log = logging.getLogger(__name__)

@python_2_unicode_compatible
class WaitRoom(models.Model):
    """
    A room for people to wait in to form groups of 3.
    """

    # Room title
    title = models.CharField(max_length=255)
    #message
    def __str__(self):
        return self.title

    @property
    def websocket_group(self):
        """
        Returns the Channels Group that sockets should subscribe to to get sent
        messages as they are generated.
        """
        return Group("wait-room-%s" % self.id)

    def send_message(self, message, user, msg_type=0):
        """
        Called to send a message to the room on behalf of a user.
        """
        final_msg = {'wait-room': str(self.id), 'message': message, 'username': user.username, 'msg_type': msg_type}

        # Send out the message to everyone in the room
        self.websocket_group.send(
            {"text": json.dumps(final_msg)}
	    )

class Message(models.Model):
    wait_room = models.ForeignKey(WaitRoom, on_delete=models.CASCADE, related_name='messages')
    
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    def __unicode__(self):
        return '[{timestamp}] : {message}'.format(**self.as_dict())

    @property
    def formatted_timestamp(self):
        return self.timestamp.strftime('%b %-d %-I:%M %p')
    
    def as_dict(self):
        return { 'message': self.message, 'timestamp': self.formatted_timestamp}

class CrowdManager(models.Manager):

	def Crowd_which_assign(self):
		CHAT_COMMUNICATION = '_chat'
		FORUM_COMMUNICATION = '_forum'
		crowds = Crowd.objects.all()
		which_crowd = 0
		#Check which crowd is not full,  and get that crowd id	
		cr = Crowd.objects.select_related().annotate(num_members=Count('members'))
		#print A[0].num_B
		i = 0	
		for crowd in crowds:
			
			log.debug(crowd.size)
			log.debug(cr[i].num_members)
			if cr[i].num_members < crowd.size :
				which_crowd = crowd.id
				break

			#if all crowds are full, crowd id = 0 , create a new crowd and get that crowd id
			if which_crowd == 0 :
				#write logic to assign chat/forum, size, task
				new_crowd = Crowd.objects.create(size=3,communication = FORUM_COMMUNICATION, task_id = 3)
				which_crowd = new_crowd.id	
			i = i + 1

		return which_crowd


class Crowd(models.Model):
	#crowd-id: automatically added 


	GROUP_SIZE = 3
	CROWD_SIZE = 30
	SIZE_CHOICES = (
	 	(GROUP_SIZE, '_group'),
	 	(CROWD_SIZE, '_crowd'), 
        )
	#size of 3 or 30
	size = models.PositiveIntegerField(choices = SIZE_CHOICES, default=GROUP_SIZE)
	CHAT_COMMUNICATION = '_chat'
	FORUM_COMMUNICATION = '_forum'
	COMMUNICATION_CHOICES = (
		(CHAT_COMMUNICATION, '_chat'),
		(FORUM_COMMUNICATION, '_forum'),
	)
	#COMMUNICATION CONDITION via chat or forum
	communication = models.CharField(choices = COMMUNICATION_CHOICES, default = CHAT_COMMUNICATION ,max_length=255)

	
	TASK_CHOICES = [(i, i) for i in range(1, 5)]
	#TASK CONDITION 1 to 5
	task_id = models.PositiveIntegerField(choices = TASK_CHOICES, default = 1)
	#waitroom reference
	#waitroom_name = models.ForeignKey(WaitRoom, on_delete = models.CASCADE, related_name = '+')
	
	#@property
	objects = CrowdManager()
	

class Crowd_Members(models.Model):
	crowd_id = models.ForeignKey(Crowd, on_delete = models.CASCADE, related_name = 'members')
	worker_id = models.CharField(max_length = 30)
	time_joined = models.DateTimeField(default=timezone.now)
	cohort_id = models.PositiveIntegerField()



