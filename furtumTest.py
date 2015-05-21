import praw
import kdapi
import time
from operator import itemgetter

r = praw.Reddit(user_agent='Test Script by u/{}'.format(INSERT USERNAME))

r.login('USERNAME','PASSWORD')

################################################################################################################################################
#                                                         Top comment grabber                                                                  #
################################################################################################################################################


def karmaComment(link):
    assert isinstance(link, str), "The karmaLink needs to be a string"
    submission = r.get_submission(submission_id=link.split("/")[6])
    karmaList = []
    for item in kdapi.check(link):
        if item.score != None and item.score != "None" and submission.short_link.split('/')[3] != item.link.split("/")[6]:

            # ^^^ Check for if a) has score b) is greater than 500 and c) is not the same thing that we are looking for
            karmaID = item.link.split("/")[6]  # Karma{} is just the stuff i have stolen.
            karmaSubmission = r.get_submission(submission_id = karmaID, comment_limit= 0)  # Submis OBJ for KD
            karmaSubmission.replace_more_comments(limit=0, threshold=0)  # Messing with morecomments is dumb, this works
            for karmaComment in karmaSubmission.comments:  # iterates through top 10 comments and grabs top
                if karmaComment.body != "None" and "(/" not in karmaComment.body and karmaComment.body != "[deleted]" and karmaComment.is_root:
                    commentTuple = [karmaComment.body, karmaComment.score]
                    karmaList.append(commentTuple)

    if not karmaList:
        return None
    else:
        return sorted(karmaList, key=itemgetter(1))[-1][0] # Sorts and then returns comment with most karma


################################################################################################################################################
#                                                               Botty Stuff                                                                    #
################################################################################################################################################


subDict = {
    0 : "pics",
    1 : "funny", 
    2 : "gaming",
    3 : "TodayILearned",
    4 : "aww"
    }
index = 0

while True:
    try:
        subreddit = r.get_subreddit(subDict[index])
        for submission in subreddit.get_new(limit=20):
            topcomment = karmaComment(str(submission.permalink))
            with open('testfile.txt','a+') as f:
                if topcomment != None and str(submission.permalink) not in f:
                    submission.add_comment(str(topcomment))
                    print "WORKED! :" + str(topcomment)
                    f.write(str(submission.permalink))
                    f.write('\n')
                else:
                    if topcomment == None:
                        print "comment is None!"
                    if str(submission.permalink) in f:
                        print "submission already commented on!"
    
    
    except UnicodeEncodeError:
        print "Stringify broke :("
        print "Exiting this iteration"
    except praw.errors.RateLimitExceeded:
        print "commenting too fast!"
        print "going to sleep!"
        time.sleep(150)
        print "halfway through!"
        time.sleep(150)
        print "done sleeping"
    except praw.errors.APIException as APIExcept:
        if APIExcept.error_type == u'DELETED_LINK':
            print "Link deleted :((("
        continue
    

    index += 1
    if index >= 5:
        print "scanned all subs"
        print "time to sleep now!"
        time.sleep(500) # TODO : Reduce this, since it's checking all of the diff subreddits, it doesnt need to wait this long
        print "halway through"
        time.sleep(500)
        index = 0