import praw
import kdapi

r = praw.Reddit(user_agent='Test Script by u/{}'.format(INSERT USERNAME)

r.login('BOTUSERNAME','PASSWORD')

def karmaCommentOBJ(submission,link):
    for item in kdapi.check(link):
        if item.score != "None" and item.score >= 500 and submission.short_link.split('/')[3] != item.link.split("/")[6]:
            # ^^^ Check for if a) has score b) is greater than 500 and c) is not the same thing that we are looking for
            karmaID = item.link.split("/")[6]  # Karma{} is just the stuff i have stolen.
            karmasubmission = r.get_submission(submission_id = karmaID,comment_limit = 10)  # Submis OBJ for KD

            karmasubmission.replace_more_comments(limit=0, threshold=0)  # Messing with morecomments is dumb, this works

            for karmacomment in karmasubmission.comments:  # iterates through top 10 comments and grabs top
                if karmacomment.body != "None" and "(/" not in karmacomment.body and karmacomment.body != "[deleted]":
                    finalComment = karmacomment.body
                    break
                else:
                    finalComment = "None - Failed all"
    print finalComment
    return finalComment

def karmaCommentLink(karmaLink):
    assert isinstance(karmaLink, str), "The karmaLink needs to be a string"
    submission = r.get_submission(submission_id = karmaLink.split("/")[6])
    return karmaCommentOBJ(submission,karmaLink)


print karmaCommentLink("http://www.reddit.com/r/SwiggitySwootyGifs/comments/36bq7f/swiggity_swooty/")



