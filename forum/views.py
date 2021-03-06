import random
import string
from django.db import transaction
from django.shortcuts import render, redirect
import haikunator
from .models import Discussion

def about(request):
    return render(request, "forum/about.html")

def new_discussion(request):
    """
    Randomly create a new discussion, and redirect to it.
    """
    new_discussion = None
    while not new_discussion:
        with transaction.atomic():
            label = haikunator.haikunate()
            if Discussion.objects.filter(label=label).exists():
                continue
            new_discussion = Discussion.objects.create(label=label)
    return redirect(discussion_forum, label=label)

def discussion_forum(request, label):
    """
    Room view - show the room, with latest messages.

    The template for this view has the WebSocket business to send and stream
    messages, so see the template for where the magic happens.
    """
    # If the room with the given label doesn't exist, automatically create it
    # upon first visit (a la etherpad).
    discussion, created = Discussion.objects.get_or_create(label=label)

    # We want to show the last 50 messages, ordered most-recent-last
    statements = reversed(discussion.statements.order_by('-timestamp')[:50])

    return render(request, "forum/discussion.html", {
        'discussion': discussion,
        'statements': statements,
    })
