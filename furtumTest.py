import praw
import kdapi
import time
import requests
from operator import itemgetter

r = praw.Reddit(user_agent='Test Script by u/{}'.format(INSERT USERNAME))

r.login('USERNAME','PASSWORD')


########################################################################################################################
#                                                Top comment grabber                                                   #
########################################################################################################################

def karmacomment(link):
    assert isinstance(link, str), "The karmaLink needs to be a string"
    sourcesubmission = r.get_submission(submission_id=link.split("/")[6])
    karmalist = []
    for item in kdapi.check(link):
        if item.score is None:
            print "Score is none!"
            continue
        elif item.score == "None":
            print "Score is None(type)"
            continue
        elif sourcesubmission.short_link.split('/')[3] == item.link.split("/")[6]: # grabs ID's and compares them
            print "ID is same!"
            continue
        else:
            karmaid = item.link.split("/")[6]  # KarmaBLANK is just the stuff from karmadecay
            karmasubmission = r.get_submission(submission_id=karmaid, comment_limit=0)  # Submits OBJ for KD
            karmasubmission.replace_more_comments(limit=0, threshold=0)  # Messing with morecomments is dumb, this works
            # TODO : Figure out why the hell this ^^^ works

            for karmaComment in karmasubmission.comments:  # goes through comments and adds score and text body
                if karmaComment.body == "None" or karmaComment.body is None:
                    print "Body has nothing!"
                    continue
                elif "(/" in karmaComment.body:
                    print "Body has weird text"
                    continue
                elif karmaComment.body == "[deleted]":
                    print "Deleted comment :("
                    continue
                elif not karmaComment.is_root:
                    print "Not root!"
                    continue
                else:
                    commenttuple = [karmaComment.body, karmaComment.score]
                    karmalist.append(commenttuple)  # adds them to karmalist to be sorted later

    if not karmalist:
        return None
    else:
        return sorted(karmalist, key=itemgetter(1))[-1][0] # Sorts and then returns comment with most karma



########################################################################################################################
#                                                  Botty Stuff                                                         #
########################################################################################################################

# establishes which subs to scan through. To add your own, just add another number that's higher, along with the sub
subDict = {
    0: "pics",
    1: "funny", 
    2: "TodayILearned",
    3: "aww"
    }
index = 0

while True:
    try:
        subreddit = r.get_subreddit(subDict[index])
        for submission in subreddit.get_new(limit=20):
            topcomment = karmacomment(str(submission.permalink))
            file = open('testfile.txt')
            if topcomment == None:
                print "Comment is empty/Doesnt exist!"
            elif file.read().find(str(topcomment)) != -1:  # find returns -1 when not found
                print "submission already commented on!"
                file.close
            else:
                file = open('testfile.txt', 'a')
                file.write(str(submission.permalink))
                file.write('\n')
                submission.add_comment(str(topcomment))
                print "WORKED! :" + str(topcomment)
                file.close

    except UnicodeEncodeError:
        print "Stringify broke :("
        print "Exiting this iteration"
        continue
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
    except requests.exceptions.HTTPError as err:
        if err.response.status_code in [502, 503, 504]:
            # these errors may only be temporary
            print "reddit seems to be down. sleeping for 30 secs"
            time.sleep(30)
        else:
            # assume other errors are fatal
            print "fatal HTTPError. printing and then sleeping for an hour"
            print str(err)
            time.sleep(3600)
    except requests.exceptions.ConnectionError:
        print "what is this lol time to sleep"
        time.sleep(30)

    # Checks for comment with score below 0 and deletes it if it is.
    user = r.get_redditor('furtum')
    for comment in user.get_comments(limit=None):
        if comment.score < 0.0:
            comment.delete()

    index += 1
    if index >= 4:
        print "scanned all subs"
        print "time to sleep now!"
        time.sleep(300) # TODO : Reduce this to a reasonable number
        print "halway through"
        time.sleep(300)
