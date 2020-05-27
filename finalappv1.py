from flask import Flask, render_template
from flask import request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('start.html')


@app.route('/search')


def search():
    return render_template('index.html')


@app.route('/searc', methods=['POST'])

def searc():
    import urllib.request
    from flask import request
    query = request.form['query']
    import sqlite3

    term = query
    term = term.replace(" ", "%25")
    db = sqlite3.connect("data.sqlite")
    mialist = []
    lealist = []
    leonalist = []
    deodlist = []

    cursor = db.cursor()
    cursor.execute("SELECT * FROM videolist WHERE query = ?;",([term]))
    d = cursor.fetchall()
    if d == []:
        print("Null")
        import urllib.request
        import json
        import datetime
        import re
        import sentiment_mod as s
        from langdetect import detect
        import html
        import sqlite3

        TAG_RE = re.compile(r'<[^>]+>')


        def remove_tags(text):
            return TAG_RE.sub('', text)


        myre = re.compile(u'['
                          u'\U0001F300-\U0001F64F'
                          u'\U0001F680-\U0001F6FF'
                          u'\u2600-\u26FF\u2700-\u27BF]+',
                          re.UNICODE)

        videolist = {}
        tokenlist = []
        rank = []
        finaltotallist = []
        lis = []
        api_key = 'AIzaSyDdLpCjSPAShuLZMbLW78fsUCJHK6ag9rE'
        search = term
        request = 'https://www.googleapis.com/youtube/v3/search?part=snippet&order=relevance&type=video&q='
        request += search + '&key='
        request += api_key + '&maxResults=5'
        response = urllib.request.urlopen(request)
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
                request = 'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId='
                request += bby + '&key='
                request += api_key + '&maxResults=100'
                response = urllib.request.urlopen(request)
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
                        request = 'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&pageToken='
                        request += token + '&videoId='
                        request += bby + '&key='
                        request += api_key + '&maxResults=100'
                        response = urllib.request.urlopen(request)
                        content = response.read()
                        data = json.loads(content.decode("utf-8"))
                        dis = comments_print(mia, lea)
                        mia = dis['pos_count']
                        lea = dis['neg_count']
                        toklist.append(token)

                    except Exception as e:
                        print("Continuing ....")

                request = 'https://www.googleapis.com/youtube/v3/videos?part=statistics&id='
                request += bby + '&key='
                request += api_key
                response = urllib.request.urlopen(request)
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
                # list iteration
                mialist.append(mia)
                lealist.append(lea)
                leonalist.append(leona)
                deodlist.append(deod)
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
                    finaltotallist.append(finaltotal)
                    print(finaltotal)

                elif (dislikepercent > likepercent):
                    finaltotal = -(dislikepercent * 0.4 + nsent * 0.6)
                    finaltotallist.append(finaltotal)
                    print(finaltotal)

                try:
                    print(toklist[-1])
                    tokenlist.append(toklist[-1])
                except Exception as e:
                    print("No token")
                    tokenlist.append('No Token')

                videolist[bby] = finaltotal
                print(videolist)

            sortvlist = sorted(videolist, key=videolist.get, reverse=True)
            for r in sortvlist:
                print(r, videolist[r])
                rank.append(r)
                lis.append(videolist[r])
            print("QUERY= ", search)
            print("VIDEOLIST =", k)
            print("MIALIST= ", mialist)
            print("LEALIST= ", lealist)
            print("LEONALIST= ", leonalist)
            print("DEODLIST= ", deodlist)
            print("FINALTOTALLIST= ", finaltotallist)
            print("TOKENLIST= ", tokenlist)
            id1 = k[0]
            print(id1)
            id2 = k[1]
            print(id2)
            id3 = k[2]
            print(id3)
            id4 = k[3]
            print(id4)
            id5 = k[4]
            print(id5)
            mia1 = mialist[0]
            print(mia1)
            mia2 = mialist[1]
            print(mia2)
            mia3 = mialist[2]
            print(mia3)
            mia4 = mialist[3]
            print(mia4)
            mia5 = mialist[4]
            print(mia5)
            lea1 = lealist[0]
            print(lea1)
            lea2 = lealist[1]
            print(lea2)
            lea3 = lealist[2]
            print(lea3)
            lea4 = lealist[3]
            print(lea4)
            lea5 = lealist[4]
            print(lea5)
            leona1 = leonalist[0]
            print(leona1)
            leona2 = leonalist[1]
            print(leona2)
            leona3 = leonalist[2]
            print(leona3)
            leona4 = leonalist[3]
            print(leona4)
            leona5 = leonalist[4]
            print(leona5)
            deod1 = deodlist[0]
            print(deod1)
            deod2 = deodlist[1]
            print(deod2)
            deod3 = deodlist[2]
            print(deod3)
            deod4 = deodlist[3]
            print(deod4)
            deod5 = deodlist[4]
            print(deod5)
            finaltotal1 = finaltotallist[0]
            print(finaltotal1)
            finaltotal2 = finaltotallist[1]
            print(finaltotal2)
            finaltotal3 = finaltotallist[2]
            print(finaltotal3)
            finaltotal4 = finaltotallist[3]
            print(finaltotal4)
            finaltotal5 = finaltotallist[4]
            print(finaltotal5)
            token1 = tokenlist[0]
            print(token1)
            token2 = tokenlist[1]
            print(token2)
            token3 = tokenlist[2]
            print(token3)
            token4 = tokenlist[3]
            print(token4)
            token5 = tokenlist[4]
            print(token5)
            db = sqlite3.connect("data.sqlite")

            db.execute("CREATE TABLE IF NOT EXISTS videolist ( query TEXT, id1 TEXT, id2 TEXT, id3 TEXT, id4 TEXT,"
                       " id5 TEXT, leona1 REAL, deod1 REAL, lea1 REAL, mia1 REAL, "
                       "finaltotal1 REAL, leona2 REAL, deod2 REAL, lea2 REAL, mia2 REAL, "
                       "finaltotal2 REAL, leona3 REAL, deod3 REAL, lea3 REAL, mia3 REAL, "
                       "finaltotal3 REAL, leona4 REAL, deod4 REAL, lea4 REAL, mia4 REAL, "
                       "finaltotal4 REAL, leona5 REAL, deod5 REAL, lea5 REAL, mia5 REAL, "
                       "finaltotal5 REAL, token1 TEXT, token2 TEXT, token3 TEXT, token4 TEXT, token5 TEXT)")
            db.execute(
                "INSERT INTO videolist VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (search, id1, id2, id3, id4, id5, leona1, deod1, lea1, mia1, finaltotal1, leona2, deod2, lea2, mia2,
                 finaltotal2,
                 leona3, deod3, lea3, mia3, finaltotal3, leona4, deod4, lea4, mia4, finaltotal4, leona5, deod5, lea5, mia5,
                 finaltotal5,
                 token1, token2, token3, token4, token5))
            # cursor = db.cursor()
            # cursor.execute("SELECT * FROM videolist")
            # d = cursor.fetchall()
            # if d == []:
            #     print("Null")
            # else:
            #     print("Data found")
            #     print(d)
            # cursor.close()
            db.commit()
            db.close()

            print(mialist[0])
            print(rank)
            return {'ids': rank, 'ranks': lis}

            print("End time", str(datetime.datetime.now()))


        ranks = giveallids()
        ides = ranks['ids']
        nums = ranks['ranks']



    else:
        def hello():
            toklist = []
            liss = []
            print("Data found")
            print(d)
            tok1 = db.execute("SELECT token1 FROM videolist WHERE query = ?;", ([term]))
            tok2 = db.execute("SELECT token2 FROM videolist WHERE query = ?;", ([term]))
            tok3 = db.execute("SELECT token3 FROM videolist WHERE query = ?;", ([term]))
            tok4 = db.execute("SELECT token4 FROM videolist WHERE query = ?;", ([term]))
            tok5 = db.execute("SELECT token5 FROM videolist WHERE query = ?;", ([term]))

            # video 1 retrieval

            id1 = db.execute("SELECT id1 FROM videolist WHERE query = ?;", ([term]))
            leona1 = db.execute("SELECT leona1 FROM videolist WHERE query = ?;", ([term]))
            deod1 = db.execute("SELECT deod1 FROM videolist WHERE query = ?;", ([term]))
            mia1 = db.execute("SELECT mia1 FROM videolist WHERE query = ?;", ([term]))
            lea1 = db.execute("SELECT lea1 FROM videolist WHERE query = ?;", ([term]))
            finaltotal1 = db.execute("SELECT finaltotal1 FROM videolist WHERE query = ?;", ([term]))
            i1 = id1.fetchone()[0]
            i1 = str(i1)
            leo1 = leona1.fetchone()[0]
            leo1 = str(leo1)
            d1 = deod1.fetchone()[0]
            d1 = str(d1)
            m1 = mia1.fetchone()[0]
            m1 = str(m1)
            le1 = lea1.fetchone()[0]
            le1 = str(le1)
            f1 = finaltotal1.fetchone()[0]
            f1 = str(f1)

            print(i1)
            print(leo1)
            print(d1)
            print(m1)
            print(le1)
            print(f1)

            # video 2 retrieval

            id2 = db.execute("SELECT id2 FROM videolist WHERE query = ?;", ([term]))
            leona2 = db.execute("SELECT leona2 FROM videolist WHERE query = ?;", ([term]))
            deod2 = db.execute("SELECT deod2 FROM videolist WHERE query = ?;", ([term]))
            mia2 = db.execute("SELECT mia2 FROM videolist WHERE query = ?;", ([term]))
            lea2 = db.execute("SELECT lea2 FROM videolist WHERE query = ?;", ([term]))
            finaltotal2 = db.execute("SELECT finaltotal2 FROM videolist WHERE query = ?;", ([term]))
            i2 = id2.fetchone()[0]
            i2 = str(i2)
            leo2 = leona2.fetchone()[0]
            leo2 = str(leo2)
            d2 = deod2.fetchone()[0]
            d2 = str(d2)
            m2 = mia2.fetchone()[0]
            m2 = str(m2)
            le2 = lea2.fetchone()[0]
            le2 = str(le2)
            f2 = finaltotal2.fetchone()[0]
            f2 = str(f2)
            print(i2)
            print(leo2)
            print(d2)
            print(m2)
            print(le2)
            print(f2)

            # video 3 retrieval

            id3 = db.execute("SELECT id3 FROM videolist WHERE query = ?;", ([term]))
            leona3 = db.execute("SELECT leona3 FROM videolist WHERE query = ?;", ([term]))
            deod3 = db.execute("SELECT deod3 FROM videolist WHERE query = ?;", ([term]))
            mia3 = db.execute("SELECT mia3 FROM videolist WHERE query = ?;", ([term]))
            lea3 = db.execute("SELECT lea3 FROM videolist WHERE query = ?;", ([term]))
            finaltotal3 = db.execute("SELECT finaltotal3 FROM videolist WHERE query = ?;", ([term]))
            i3 = id3.fetchone()[0]
            i3 = str(i3)
            leo3 = leona3.fetchone()[0]
            leo3 = str(leo3)
            d3 = deod3.fetchone()[0]
            d3 = str(d3)
            m3 = mia3.fetchone()[0]
            m3 = str(m3)
            le3 = lea3.fetchone()[0]
            le3 = str(le3)
            f3 = finaltotal3.fetchone()[0]
            f3 = str(f3)

            print(i3)
            print(leo3)
            print(d3)
            print(m3)
            print(le3)
            print(f3)

            # video 4 retrieval

            id4 = db.execute("SELECT id4 FROM videolist WHERE query = ?;", ([term]))
            leona4 = db.execute("SELECT leona4 FROM videolist WHERE query = ?;", ([term]))
            deod4 = db.execute("SELECT deod4 FROM videolist WHERE query = ?;", ([term]))
            mia4 = db.execute("SELECT mia4 FROM videolist WHERE query = ?;", ([term]))
            lea4 = db.execute("SELECT lea4 FROM videolist WHERE query = ?;", ([term]))
            finaltotal4 = db.execute("SELECT finaltotal4 FROM videolist WHERE query = ?;", ([term]))
            i4 = id4.fetchone()[0]
            i4 = str(i4)
            leo4 = leona4.fetchone()[0]
            leo4 = str(leo4)
            d4 = deod4.fetchone()[0]
            d4 = str(d4)
            m4 = mia4.fetchone()[0]
            m4 = str(m4)
            le4 = lea4.fetchone()[0]
            le4 = str(le4)
            f4 = finaltotal4.fetchone()[0]
            f4 = str(f4)

            print(i4)
            print(leo4)
            print(d4)
            print(m4)
            print(le4)
            print(f4)

            # video 5 retrieval

            id5 = db.execute("SELECT id5 FROM videolist WHERE query = ?;", ([term]))
            leona5 = db.execute("SELECT leona5 FROM videolist WHERE query = ?;", ([term]))
            deod5 = db.execute("SELECT deod5 FROM videolist WHERE query = ?;", ([term]))
            mia5 = db.execute("SELECT mia5 FROM videolist WHERE query = ?;", ([term]))
            lea5 = db.execute("SELECT lea5 FROM videolist WHERE query = ?;", ([term]))
            finaltotal5 = db.execute("SELECT finaltotal5 FROM videolist WHERE query = ?;", ([term]))
            i5 = id5.fetchone()[0]
            i5 = str(i5)
            leo5 = leona5.fetchone()[0]
            leo5 = str(leo5)
            d5 = deod5.fetchone()[0]
            d5 = str(d5)
            m5 = mia5.fetchone()[0]
            m5 = str(m5)
            le5 = lea5.fetchone()[0]
            le5 = str(le5)
            f5 = finaltotal5.fetchone()[0]
            f5 = str(f5)

            print(i5)
            print(leo5)
            print(d5)
            print(m5)
            print(le5)
            print(f5)


            # token retrieval

            t1 = tok1.fetchone()[0]
            t1 = str(t1)
            print(t1)
            toklist.append(t1)
            t2 = tok2.fetchone()[0]
            t2 = str(t2)
            print(t2)
            toklist.append(t2)
            t3 = tok3.fetchone()[0]
            t3 = str(t3)
            print(t3)
            toklist.append(t3)
            t4 = tok4.fetchone()[0]
            t4 = str(t4)
            print(t4)
            toklist.append(t4)
            t5 = tok5.fetchone()[0]
            t5 = str(t5)
            print(t5)
            toklist.append(t5)
            print(toklist)
            vlist = {}
            tolist = []
            rank = []

            # Video 1
            if t1 == "No Token":
                print("No new comments added")
                vlist[i1] = float(f1)
                print(vlist)
                tolist.append(f1)
                mialist.append(m1)
                lealist.append(le1)
                leonalist.append(leo1)
                deodlist.append(d1)
            else:
                print("Retrieving Comments with Token -- ", t1)
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



                def giveallvids():
                    videoid = i1
                    pagetoken = t1
                    api_key = 'AIzaSyDdLpCjSPAShuLZMbLW78fsUCJHK6ag9rE'
                    pos_count = 0
                    neg_count = 0
                    bby = videoid
                    print(bby)
                    request = 'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&pageToken='
                    request += pagetoken +'&videoId='
                    request += bby + '&key='
                    request += api_key + '&maxResults=100'
                    print(request)
                    response = urllib.request.urlopen(request)
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
                            request = 'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&pageToken='
                            request += token + '&videoId='
                            request += bby + '&key='
                            request += api_key + '&maxResults=100'
                            response = urllib.request.urlopen(request)
                            content = response.read()
                            data = json.loads(content.decode("utf-8"))
                            dis = comments_print(mia, lea)
                            mia = dis['pos_count']
                            lea = dis['neg_count']
                            toklist.append(token)

                        except Exception as e:
                            print("Continuing ....")

                    request = 'https://www.googleapis.com/youtube/v3/videos?part=statistics&id='
                    request += bby + '&key='
                    request += api_key
                    response = urllib.request.urlopen(request)
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
                    # add values
                    print("Old likes and dislikes ", leo1, d1)
                    totaloldlikes = float(leo1) + float(d1)
                    print(totaloldlikes)
                    print("Old sentiment analysis values ", m1, le1)
                    totaloldsent = float(m1) +float(le1)
                    print(totaloldsent)
                    # new values
                    newleona = leona
                    print(newleona)
                    print(leona)
                    newmia = float(mia) + float(m1)
                    newlea = float(lea) + float(le1)
                    newdeod = deod
                    mialist.append(str(newmia))
                    lealist.append(str(newlea))
                    leonalist.append(str(newleona))
                    deodlist.append(str(newdeod))
                    print(deod)
                    print(newdeod)
                    print("New values ", newdeod, newlea, newmia, newleona)
                    newtotallikes = float(newleona) + float(newdeod)
                    newtotalsent = float(newmia) + float(newlea)
                    print(newtotalsent)
                    print(newtotallikes)


                    totallikes = float(leona) + float(deod)
                    print(totallikes)
                    totalsent = float(mia) + float(lea)
                    print(totalsent)
                    likepercent = (float(newleona) / newtotallikes) * 100
                    print(likepercent)
                    dislikepercent = (float(newdeod) / newtotallikes) * 100
                    print(dislikepercent)
                    psent = (float(newmia) / newtotalsent) * 100
                    print(psent)
                    nsent = (float(newlea) / newtotalsent) *100
                    print(nsent)
                    if (likepercent > dislikepercent):
                        finaltotal = (likepercent * 0.4) + (psent *0.6)
                        print(finaltotal)

                    elif (dislikepercent > likepercent):
                        finaltotal = -(dislikepercent * 0.4 + nsent *0.6)
                        print(finaltotal)

                    try:
                        print(toklist[-1])

                    except Exception as e:
                        print("No token")

                    tolist.append(finaltotal)
                    vlist[i1] = finaltotal
                    print(vlist)

                    db.execute("UPDATE videolist SET mia1 = ? WHERE query = ?;", ([newmia,term]))
                    db.execute("UPDATE videolist SET lea1 = ? WHERE query = ?;", ([newlea, term]))
                    db.execute("UPDATE videolist SET finaltotal1 = ? WHERE query = ?;", ([finaltotal, term]))
                    db.commit()

                giveallvids()



            # Video 2

            if t2 == "No Token":
                print("No new comments added")
                vlist[i2] = float(f2)
                print(vlist)
                tolist.append(f2)
                mialist.append(m2)
                lealist.append(le2)
                leonalist.append(leo2)
                deodlist.append(d2)
            else:
                print("Retrieving Comments with Token -- ", t2)
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


                def giveallvids():
                    videoid = i2
                    pagetoken = t2
                    api_key = 'AIzaSyDdLpCjSPAShuLZMbLW78fsUCJHK6ag9rE'
                    pos_count = 0
                    neg_count = 0
                    bby = videoid
                    print(bby)
                    request = 'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&pageToken='
                    request += pagetoken + '&videoId='
                    request += bby + '&key='
                    request += api_key + '&maxResults=100'
                    print(request)
                    response = urllib.request.urlopen(request)
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
                            request = 'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&pageToken='
                            request += token + '&videoId='
                            request += bby + '&key='
                            request += api_key + '&maxResults=100'
                            response = urllib.request.urlopen(request)
                            content = response.read()
                            data = json.loads(content.decode("utf-8"))
                            dis = comments_print(mia, lea)
                            mia = dis['pos_count']
                            lea = dis['neg_count']
                            toklist.append(token)

                        except Exception as e:
                            print("Continuing ....")

                    request = 'https://www.googleapis.com/youtube/v3/videos?part=statistics&id='
                    request += bby + '&key='
                    request += api_key
                    response = urllib.request.urlopen(request)
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
                    # add values
                    print("Old likes and dislikes ", leo2, d2)
                    totaloldlikes = float(leo2) + float(d2)
                    print(totaloldlikes)
                    print("Old sentiment analysis values ", m2, le2)
                    totaloldsent = float(m2) + float(le2)
                    print(totaloldsent)
                    # new values
                    newleona = leona
                    print(newleona)
                    print(leona)
                    newmia = float(mia) + float(m2)
                    newlea = float(lea) + float(le2)
                    newdeod = deod
                    print(deod)
                    print(newdeod)
                    mialist.append(str(newmia))
                    lealist.append(str(newlea))
                    leonalist.append(str(newleona))
                    deodlist.append(str(newdeod))
                    print("New values ", newdeod, newlea, newmia, newleona)
                    newtotallikes = float(newleona) + float(newdeod)
                    newtotalsent = float(newmia) + float(newlea)
                    print(newtotalsent)
                    print(newtotallikes)

                    totallikes = float(leona) + float(deod)
                    print(totallikes)
                    totalsent = float(mia) + float(lea)
                    print(totalsent)
                    likepercent = (float(newleona) / newtotallikes) * 100
                    print(likepercent)
                    dislikepercent = (float(newdeod) / newtotallikes) * 100
                    print(dislikepercent)
                    psent = (float(newmia) / newtotalsent) * 100
                    print(psent)
                    nsent = (float(newlea) / newtotalsent) * 100
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

                    tolist.append(finaltotal)
                    vlist[i2] = finaltotal
                    print(vlist)

                    db.execute("UPDATE videolist SET mia2 = ? WHERE query = ?;", ([newmia, term]))
                    db.execute("UPDATE videolist SET lea2 = ? WHERE query = ?;", ([newlea, term]))
                    db.execute("UPDATE videolist SET finaltotal2 = ? WHERE query = ?;", ([finaltotal, term]))
                    db.commit()


                giveallvids()

            # Video 3

            if t3 == "No Token":
                print("No new comments added")
                vlist[i3] = float(f3)
                print(vlist)
                tolist.append(f3)
                mialist.append(m3)
                lealist.append(le3)
                leonalist.append(leo3)
                deodlist.append(d3)
            else:
                print("Retrieving Comments with Token -- ", t3)
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


                def giveallvids():
                    videoid = i3
                    pagetoken = t3
                    api_key = 'AIzaSyDdLpCjSPAShuLZMbLW78fsUCJHK6ag9rE'
                    pos_count = 0
                    neg_count = 0
                    bby = videoid
                    print(bby)
                    request = 'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&pageToken='
                    request += pagetoken + '&videoId='
                    request += bby + '&key='
                    request += api_key + '&maxResults=100'
                    print(request)
                    response = urllib.request.urlopen(request)
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
                            request = 'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&pageToken='
                            request += token + '&videoId='
                            request += bby + '&key='
                            request += api_key + '&maxResults=100'
                            response = urllib.request.urlopen(request)
                            content = response.read()
                            data = json.loads(content.decode("utf-8"))
                            dis = comments_print(mia, lea)
                            mia = dis['pos_count']
                            lea = dis['neg_count']
                            toklist.append(token)

                        except Exception as e:
                            print("Continuing ....")

                    request = 'https://www.googleapis.com/youtube/v3/videos?part=statistics&id='
                    request += bby + '&key='
                    request += api_key
                    response = urllib.request.urlopen(request)
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
                    # add values
                    print("Old likes and dislikes ", leo3, d3)
                    totaloldlikes = float(leo3) + float(d3)
                    print(totaloldlikes)
                    print("Old sentiment analysis values ", m3, le3)
                    totaloldsent = float(m3) + float(le3)
                    print(totaloldsent)
                    # new values
                    newleona = leona
                    print(newleona)
                    print(leona)
                    newmia = float(mia) + float(m3)
                    newlea = float(lea) + float(le3)
                    newdeod = deod
                    print(deod)
                    print(newdeod)
                    mialist.append(str(newmia))
                    lealist.append(str(newlea))
                    leonalist.append(str(newleona))
                    deodlist.append(str(newdeod))
                    print("New values ", newdeod, newlea, newmia, newleona)
                    newtotallikes = float(newleona) + float(newdeod)
                    newtotalsent = float(newmia) + float(newlea)
                    print(newtotalsent)
                    print(newtotallikes)

                    totallikes = float(leona) + float(deod)
                    print(totallikes)
                    totalsent = float(mia) + float(lea)
                    print(totalsent)
                    likepercent = (float(newleona) / newtotallikes) * 100
                    print(likepercent)
                    dislikepercent = (float(newdeod) / newtotallikes) * 100
                    print(dislikepercent)
                    psent = (float(newmia) / newtotalsent) * 100
                    print(psent)
                    nsent = (float(newlea) / newtotalsent) * 100
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

                    tolist.append(finaltotal)
                    vlist[i3] = finaltotal
                    print(vlist)

                    db.execute("UPDATE videolist SET mia3 = ? WHERE query = ?;", ([newmia, term]))
                    db.execute("UPDATE videolist SET lea3 = ? WHERE query = ?;", ([newlea, term]))
                    db.execute("UPDATE videolist SET finaltotal3 = ? WHERE query = ?;", ([finaltotal, term]))
                    db.commit()


                giveallvids()

            # Video 4

            if t4 == "No Token":
                print("No new comments added")
                vlist[i4] = float(f4)
                print(vlist)
                tolist.append(f4)
                mialist.append(m4)
                lealist.append(le4)
                leonalist.append(leo4)
                deodlist.append(d4)
            else:
                print("Retrieving Comments with Token -- ", t4)
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


                def giveallvids():
                    videoid = i4
                    pagetoken = t4
                    api_key = 'AIzaSyDdLpCjSPAShuLZMbLW78fsUCJHK6ag9rE'
                    pos_count = 0
                    neg_count = 0
                    bby = videoid
                    print(bby)
                    request = 'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&pageToken='
                    request += pagetoken + '&videoId='
                    request += bby + '&key='
                    request += api_key + '&maxResults=100'
                    print(request)
                    response = urllib.request.urlopen(request)
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
                            request = 'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&pageToken='
                            request += token + '&videoId='
                            request += bby + '&key='
                            request += api_key + '&maxResults=100'
                            response = urllib.request.urlopen(request)
                            content = response.read()
                            data = json.loads(content.decode("utf-8"))
                            dis = comments_print(mia, lea)
                            mia = dis['pos_count']
                            lea = dis['neg_count']
                            toklist.append(token)

                        except Exception as e:
                            print("Continuing ....")

                    request = 'https://www.googleapis.com/youtube/v3/videos?part=statistics&id='
                    request += bby + '&key='
                    request += api_key
                    response = urllib.request.urlopen(request)
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
                    # add values
                    print("Old likes and dislikes ", leo4, d4)
                    totaloldlikes = float(leo4) + float(d4)
                    print(totaloldlikes)
                    print("Old sentiment analysis values ", m4, le4)
                    totaloldsent = float(m4) + float(le4)
                    print(totaloldsent)
                    # new values
                    newleona = leona
                    print(newleona)
                    print(leona)
                    newmia = float(mia) + float(m4)
                    newlea = float(lea) + float(le4)
                    newdeod = deod
                    print(deod)
                    print(newdeod)
                    mialist.append(str(newmia))
                    lealist.append(str(newlea))
                    leonalist.append(str(newleona))
                    deodlist.append(str(newdeod))
                    print("New values ", newdeod, newlea, newmia, newleona)
                    newtotallikes = float(newleona) + float(newdeod)
                    newtotalsent = float(newmia) + float(newlea)
                    print(newtotalsent)
                    print(newtotallikes)

                    totallikes = float(leona) + float(deod)
                    print(totallikes)
                    totalsent = float(mia) + float(lea)
                    print(totalsent)
                    likepercent = (float(newleona) / newtotallikes) * 100
                    print(likepercent)
                    dislikepercent = (float(newdeod) / newtotallikes) * 100
                    print(dislikepercent)
                    psent = (float(newmia) / newtotalsent) * 100
                    print(psent)
                    nsent = (float(newlea) / newtotalsent) * 100
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

                    tolist.append(finaltotal)
                    vlist[i4] = finaltotal
                    print(vlist)

                    db.execute("UPDATE videolist SET mia4 = ? WHERE query = ?;", ([newmia, term]))
                    db.execute("UPDATE videolist SET lea4 = ? WHERE query = ?;", ([newlea, term]))
                    db.execute("UPDATE videolist SET finaltotal4 = ? WHERE query = ?;", ([finaltotal, term]))
                    db.commit()


                giveallvids()

            # Video 5


            if t5 == "No Token":
                print("No new comments added")
                vlist[i5] = float(f5)
                print(vlist)
                tolist.append(f5)
                mialist.append(m5)
                lealist.append(le5)
                leonalist.append(leo5)
                deodlist.append(d5)
            else:
                print("Retrieving Comments with Token -- ", t5)
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


                def giveallvids():
                    videoid = i5
                    pagetoken = t5
                    api_key = 'AIzaSyDdLpCjSPAShuLZMbLW78fsUCJHK6ag9rE'
                    pos_count = 0
                    neg_count = 0
                    bby = videoid
                    print(bby)
                    request = 'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&pageToken='
                    request += pagetoken + '&videoId='
                    request += bby + '&key='
                    request += api_key + '&maxResults=100'
                    print(request)
                    response = urllib.request.urlopen(request)
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
                            request = 'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&pageToken='
                            request += token + '&videoId='
                            request += bby + '&key='
                            request += api_key + '&maxResults=100'
                            response = urllib.request.urlopen(request)
                            content = response.read()
                            data = json.loads(content.decode("utf-8"))
                            dis = comments_print(mia, lea)
                            mia = dis['pos_count']
                            lea = dis['neg_count']
                            toklist.append(token)

                        except Exception as e:
                            print("Continuing ....")

                    request = 'https://www.googleapis.com/youtube/v3/videos?part=statistics&id='
                    request += bby + '&key='
                    request += api_key
                    response = urllib.request.urlopen(request)
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
                    # add values
                    print("Old likes and dislikes ", leo5, d5)
                    totaloldlikes = float(leo5) + float(d5)
                    print(totaloldlikes)
                    print("Old sentiment analysis values ", m5, le5)
                    totaloldsent = float(m5) + float(le5)
                    print(totaloldsent)
                    # new values
                    newleona = leona
                    print(newleona)
                    print(leona)
                    newmia = float(mia) + float(m5)
                    newlea = float(lea) + float(le5)
                    newdeod = deod
                    print(deod)
                    print(newdeod)
                    mialist.append(str(newmia))
                    lealist.append(str(newlea))
                    leonalist.append(str(newleona))
                    deodlist.append(str(newdeod))
                    print("New values ", newdeod, newlea, newmia, newleona)
                    newtotallikes = float(newleona) + float(newdeod)
                    newtotalsent = float(newmia) + float(newlea)
                    print(newtotalsent)
                    print(newtotallikes)

                    totallikes = float(leona) + float(deod)
                    print(totallikes)
                    totalsent = float(mia) + float(lea)
                    print(totalsent)
                    likepercent = (float(newleona) / newtotallikes) * 100
                    print(likepercent)
                    dislikepercent = (float(newdeod) / newtotallikes) * 100
                    print(dislikepercent)
                    psent = (float(newmia) / newtotalsent) * 100
                    print(psent)
                    nsent = (float(newlea) / newtotalsent) * 100
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

                    tolist.append(finaltotal)
                    vlist[i5] = finaltotal
                    print(vlist)


                    db.execute("UPDATE videolist SET mia5 = ? WHERE query = ?;", ([newmia, term]))
                    db.execute("UPDATE videolist SET lea5 = ? WHERE query = ?;", ([newlea, term]))
                    db.execute("UPDATE videolist SET finaltotal5 = ? WHERE query = ?;", ([finaltotal, term]))
                    db.commit()


                giveallvids()

            sortvlist = sorted(vlist, key=vlist.get, reverse=True)
            for r in sortvlist:
                print(r, vlist[r])
                rank.append(r)
                liss.append(vlist[r])

            return {'ids': rank, 'ran': liss}

        ranks = hello()
        ides = ranks['ids']
        nums = ranks['ran']
        print("Mialist:", mialist)
        print("Lealist:", lealist)
        print("Leonalist:", leonalist)
        print("Deodlist:", deodlist)

    cursor.close()
    db.close()
    return render_template('recommend.html', query=ides, number=nums, like=leonalist, dislike=deodlist, pos=mialist, neg=lealist)


if __name__ =="__main__":
    app.run()
