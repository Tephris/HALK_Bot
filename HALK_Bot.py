#!/usr/bin/python

import praw
import pdb
import re
import os
import codecs
import sys

# Create the Reddit instance
reddit = praw.Reddit('bot1')

# and login
#reddit.login(REDDIT_USERNAME, REDDIT_PASS)

# Have we run this code before? If not, create an empty list
if not os.path.isfile("posts_history.txt"):
	posts_history = []

# If we have run the code before, load the list of posts we have replied to
else:
	# Read the file into a list and remove any empty values
	with open("posts_history.txt", "r") as f:
		posts_history = f.read()
		posts_history = posts_history.split("\n")
		posts_history = list(filter(None, posts_history))
		
if not os.path.isfile("post_history_comments.txt"):
	post_history_comments = []
	
if not os.path.isfile("Deleted_Comments.txt"):
	Deleted_Comments = []

# Get the as many values as possible from our subreddit
subreddit = reddit.subreddit('pythonforengineers')

for comment in subreddit.stream.comments():
	#print(submission.title)
	posts_history.append(comment.id) #Adds comment IDs to posts_history.txt
	with codecs.open("post_history_comments.txt", mode="a", encoding='utf-8') as f:
		CommentString = comment.id + "::::" + comment.body + "::::"
		NewCommentString = bytes(CommentString, 'utf-8').decode('utf-8', 'ignore')
		f.write(NewCommentString)
	if comment.body == "!deleted":
		previousCommentID = comment.parent().id
		with open("post_history_comments.txt", "r") as f:
			post_history_comments1 = f.read()
			post_history_comments1 = post_history_comments1.split("::::")
			post_history_comments1 = list(filter(None, post_history_comments1))
		prevPosition = post_history_comments1.index(previousCommentID)
		with codecs.open("Deleted_Comments.txt", mode="a", encoding='utf-8') as f:
			CommentString = post_history_comments1[prevPosition+1]
			NewCommentString = bytes(CommentString, 'utf-8').decode('utf-8', 'ignore')
			f.write(NewCommentString)


# Write our updated list back to the file
with open("posts_history.txt", "w") as f:
	for post_id in posts_history:
		f.write(post_id + "\n")