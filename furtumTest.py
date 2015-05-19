    import praw
import kdapi
import time
import linecache
from operator import itemgetter

r = praw.Reddit(user_agent='Test Script by u/{}'.format(INSERT USERNAME))

r.login('USERNAME','PASSWORD')

################################################################################################################################################
#                                                         Top comment grabber                                                                  #
################################################################################################################################################


def karmaCommentOBJ(submission,link):
    karmalist = []
    for item in kdapi.check(link):
        if item.score != None and item.score != "None" and submission.short_link.split('/')[3] != item.link.split("/")[6]:

            # ^^^ Check for if a) has score b) is greater than 500 and c) is not the same thing that we are looking for
            karmaID = item.link.split("/")[6]  # Karma{} is just the stuff i have stolen.
            karmasubmission = r.get_submission(submission_id = karmaID,comment_limit = 10)  # Submis OBJ for KD
            karmasubmission.replace_more_comments(limit=0, threshold=0)  # Messing with morecomments is dumb, this works
            karmalist = []
            for karmacomment in karmasubmission.comments:  # iterates through top 10 comments and grabs top
                if karmacomment.body != "None" and "(/" not in karmacomment.body and karmacomment.body != "[deleted]" and karmacomment.is_root:
                    tuplelist = [karmacomment.body,karmacomment.score]
                    karmalist.append(tuplelist)
    return karmalist

def karmaCommentLink(karmaLink):
    assert isinstance(karmaLink, str), "The karmaLink needs to be a string"
    submission = r.get_submission(submission_id = karmaLink.split("/")[6])
    karmalist = karmaCommentOBJ(submission,karmaLink)
    if not karmalist:
        return None
    else:
        return sorted(karmalist,key=itemgetter(1))[-1][0]

################################################################################################################################################
#                                                               Botty Stuff                                                                    #
################################################################################################################################################

already_done = []
while True:
    subreddit = r.get_subreddit('all')
    for submission in subreddit.get_new(limit=20):
        print submission
        try:
            topComment = karmaCommentLink(str(submission.permalink))
        except UnicodeEncodeError:
            continue
        if topComment != None and topComment not in already_done:
            print "worked: " + topComment
            
            with open("testfile.txt","a") as f:
                try:
                    f.write(str([topComment,submission.permalink]))
                    f.write("\n")
                    submission.add_comment(str(topComment))
                except UnicodeEncodeError:
                    f.write("['String broke :(((']")
                    f.write(',')
                    f.write("\n")
                    continue
                except praw.errors.RateLimitExceeded:
                    print "commenting too fast!"
                    print "going to sleep!"
                    time.sleep(150)
                    print "halfway through!"
                    time.sleep(150)
                    print "done sleeping"
                    try:
                        submission.add_comment(str(topComment))
                    except UnicodeEncodeError:
                        f.write("['String broke :(((']")
                        f.write(',')
                        f.write("\n")
                        continue
        else:
            print "failed :("
    print "sleeping!"
    time.sleep(120)


