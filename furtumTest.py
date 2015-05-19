import praw
import kdapi

r = praw.Reddit(user_agent='Test Script by u/{}'.format('INSERT USERNAME'))

r.login('BOTUSERNAME','PASSWORD')

def karmaCommentOBJ(submission,link):
    karmalist = []
    for item in kdapi.check(link):
        finalComment = "broken :((((("
        # print item.title
        # print str(item.score) + " score" 
        if item.score != None and item.score != "None" and item.score >= 500 and submission.short_link.split('/')[3] != item.link.split("/")[6]:
            # ^^^ Check for if a) has score b) is greater than 500 and c) is not the same thing that we are looking for
            karmaID = item.link.split("/")[6]  # Karma{} is just the stuff i have stolen.
            karmasubmission = r.get_submission(submission_id = karmaID,comment_limit = 0)  # Submis OBJ for KD

            karmasubmission.replace_more_comments(limit=0, threshold=0)  # Messing with morecomments is dumb, this works


            karmalist = []
            for karmacomment in karmasubmission.comments:  # iterates through top 10 comments and grabs top
                if karmacomment.body != "None" and "(/" not in karmacomment.body and karmacomment.body != "[deleted]" and karmacomment.is_root:
                    tuplelist = [karmacomment.body,karmacomment.score]
                    karmalist.append(tuplelist)
                    finalComment = "Did pass " + str(karmacomment.body)
                else:
                    finalComment = "None - Failed all"
        else:
            if item.score == "None":
                print "itmescore is none"
            if item.score <= 500:
                print "itemscore too low"
            if submission.short_link.split('/')[3] == item.link.split("/")[6]:
                print "same thing"
            print "did not pass"
    return karmalist

def karmaCommentLink(karmaLink):
    assert isinstance(karmaLink, str), "The karmaLink needs to be a string"
    submission = r.get_submission(submission_id = karmaLink.split("/")[6])
    karmalist = karmaCommentOBJ(submission,karmaLink)
    if not karmalist:
        return None
    else:
        return sorted(karmalist,key=lambda x: x[1])[0][0]


print karmaCommentLink("http://www.reddit.com/r/pics/comments/2z0lm7/miss_america_1924/")