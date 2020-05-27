from flask import Flask, render_template, request



app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('start.html')

@app.route('/search', methods=['GET', 'POST'])

def search():
    if request.method == 'POST':
        query = request.form['query']
        import urllib.request
        import json
        import datetime
        import re
        import sentiment_mod as s
        from langdetect import detect
        import html

        TAG_RE = re.compile(r'<[^>]+>')

        def remove_tags(text):
            return TAG_RE.sub('', text)

        myre = re.compile(u'['
                          u'\U0001F300-\U0001F64F'
                          u'\U0001F680-\U0001F6FF'
                          u'\u2600-\u26FF\u2700-\u27BF]+',
                          re.UNICODE)
        videolist = {}
        rank = []
        api_key = 'AIzaSyDdLpCjSPAShuLZMbLW78fsUCJHK6ag9rE'
        # search = str(input("Enter keyword to search for: "))
        query = query.replace(" ", "%25")
        request1 = 'https://www.googleapis.com/youtube/v3/search?part=snippet&order=relevance&type=video&q='
        request1 += query + '&key='
        request1 += api_key + '&maxResults=5'
        response = urllib.request.urlopen(request1)
        content = response.read()
        data = json.loads(content.decode("utf-8"))

        print("Retrieved on => ", str(datetime.datetime.now()))
        print("=" * 80)

        def videoid():
            for make in data['items']:
                try:

                    video_id = (make["id"]["videoId"])
                    yield video_id

                except Exception as e:
                    print(e)

        def bat():
            bitch = set([])
            for boop in videoid():
                bitch.add(boop)
            j = sorted(list(bitch))
            return j

        k = bat()

        # request = 'https://www.googleapis.com/youtube/v3/videos?part=snippet&id='
        # request += k + '&key='
        # request += api_key
        # response = urllib.request.urlopen(request)
        # content = response.read()
        # datas = json.loads(content.decode("utf-8"))
        #
        #
        # def videotitle():
        #     for make in datas['items']:
        #         try:
        #             title = (make["snippet"]["title"])
        #             return title
        #
        #         except Exception as e:
        #             print(e)

        #
        # hah = videotitle()
        print(k)

        def giveallids():

            for nomn in range(0, 5):
                pos_count = 0
                neg_count = 0
                bby = k[nomn]
                print(bby)
                request1 = 'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId='
                request1 += bby + '&key='
                request1 += api_key + '&maxResults=100'
                response = urllib.request.urlopen(request1)
                content = response.read()
                data = json.loads(content.decode("utf-8"))

                # next_pageToken = (data['nextPageToken'])
                # print(next_pageToken)



                def comments_print(pos_count, neg_count):

                    for make in data['items']:
                        comments = (make["snippet"]["topLevelComment"]["snippet"]["textDisplay"])
                        refined_comments = str(remove_tags(comments))
                        refined_comments = html.unescape(refined_comments)
                        refined_comments = myre.sub('', refined_comments)

                        try:

                            k = detect(refined_comments)

                            if k != "en":

                                refined_comments = None
                            else:

                                sentiment_value, confidence = s.sentiment(refined_comments)
                                print(refined_comments, sentiment_value, confidence)
                                if sentiment_value == "pos":
                                    pos_count = pos_count + 1

                                else:
                                    neg_count = neg_count + 1

                        except Exception as e:
                            print("Exception occurred at land detect")

                    return {'pos_count': pos_count, 'neg_count': neg_count}

                def checknextpagetoken():
                    try:
                        next_pagetoken = data['nextPageToken']
                        return next_pagetoken
                    except KeyError:
                        return "The token does not exist"

                print("=" * 40)
                print("Start time", str(datetime.datetime.now()))
                print("=" * 40)

                # comments_print(pos_count, neg_count)

                kia = comments_print(pos_count, neg_count)
                mia = kia['pos_count']
                lea = kia['neg_count']

                token = checknextpagetoken()
                toklist = []
                while token != "The token does not exist":
                    try:
                        token = checknextpagetoken()
                        request1 = 'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&pageToken='
                        request1 += token + '&videoId='
                        request1 += bby + '&key='
                        request1 += api_key + '&maxResults=100'
                        response = urllib.request.urlopen(request1)
                        content = response.read()
                        data = json.loads(content.decode("utf-8"))
                        dis = comments_print(mia, lea)
                        mia = dis['pos_count']
                        lea = dis['neg_count']
                        toklist.append(token)

                    except Exception as e:
                        print("Continuing ....")

                request1 = 'https://www.googleapis.com/youtube/v3/videos?part=statistics&id='
                request1 += bby + '&key='
                request1 += api_key
                response = urllib.request.urlopen(request1)
                content = response.read()
                data = json.loads(content.decode("utf-8"))

                def stats():
                    for make in data['items']:
                        like_count = (make["statistics"]["likeCount"])
                        dislike_count = (make["statistics"]["dislikeCount"])
                        view_count = (make["statistics"]["viewCount"])
                        # print(like_count , dislike_count)
                        return {'like': like_count, 'dislike': dislike_count, 'view': view_count}

                kendra = stats()
                leona = kendra['like']
                deod = kendra['dislike']
                viewc = kendra['view']
                print("Like:- " + leona, "Diskike:-" + deod, "View Count:- " + viewc)
                print(mia, lea)

                totallikes = float(leona) + float(deod)
                print(totallikes)
                totalsent = float(mia) + float(lea)
                print(totalsent)
                likepercent = (float(leona) / totallikes) * 100
                print(likepercent)
                dislikepercent = (float(deod) / totallikes) * 100
                print(dislikepercent)
                psent = (float(mia) / totalsent) * 100
                print(psent)
                nsent = (float(lea) / totalsent) * 100
                print(nsent)
                if (likepercent > dislikepercent):
                    finaltotal = (likepercent * 0.4) + (psent * 0.6)
                    print(finaltotal)

                elif (dislikepercent > likepercent):
                    finaltotal = -(dislikepercent * 0.4 + nsent * 0.6)
                    print(finaltotal)

                try:
                    print(toklist[-1])
                except Exception as e:
                    print("No token")

                videolist[bby] = finaltotal
                print(videolist)

            sortvlist = sorted(videolist, key=videolist.get, reverse=True)
            for r in sortvlist:
                print(r, videolist[r])
                rank.append(r)

            print(rank)
            return rank
            print("End time", str(datetime.datetime.now()))

        rank = giveallids()
















        return render_template('recommend.html', query=rank)
    return render_template('index.html')


if __name__ =="__main__":
    app.run()