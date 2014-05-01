import json
import urllib
import re
import math

def scalescore(rawscore):
    scaledscore = ((rawscore*10)+10)/2
    return math.floor(scaledscore)

def getscaledscore(pos,neg):
    for item in pos:
        rawscore = pos[item]
        scaledscore = scalescore(rawscore)
        pos[item] = scaledscore
    for item in neg:
        rawscore = neg[item]
        scaledscore = scalescore(-1 * rawscore)
        neg[item] = scaledscore
    return pos,neg

def getFeatures(inputdata,moviename):
    acting = []
    direction = []
    url = "http://www.omdbapi.com/?t="+moviename
    content = json.loads(urllib.urlopen(url).read())
    if content["Response"] == "True":
        if content.has_key("Actors"):
            actorunicodelist = content["Actors"]
            actorlist = actorunicodelist.encode('utf-8').lower()
            acting = re.findall("\w+",actorlist)
        if content.has_key("Director"):
            directorunicidelist = content["Director"]
            directorlist = directorunicidelist.encode('utf-8').lower()
            direction = re.findall("\w+",directorlist)
    if not acting:    
        acting = ['tom', 'cruise', 'tomcruise', 'leonardo', 'dicaprio', 'leodicaprio', 'johnny', 'depp', 'johnnydepp', 'brad', 'pitt', 'bradpitt', 'matt', 'damon', 'mattdamon', 'adam', 'sandler', 'adamsandler', 'dwayne', 'johnson', 'dwanejohnson2', 'dwanejohnson', 'rock', 'ben', 'stiller', 'benstiller', 'redhourben', 'benstiller', 'sacha', 'baron', 'cohen', 'sachabaron', 'sachabaroncohen', 'will', 'smith', 'willsmith', 'mark', 'wahlberg', 'mark_wahlberg', 'markwahlberg', 'robert', 'pattinson', 'robertpattinson', 'taylorlautner', 'taylor', 'lautner', 'jude', 'law', 'judehlaw', 'bradley', 'cooper', 'bradleycooper', 'tom', 'hanks', 'tomhanks', 'chris', 'evans', 'chrisevans', 'sebastian', 'stan', 'sebastianstan', 'theo', 'james', 'theojames', 'sylvesterstallone', 'sylvester', 'stallone', 'theslystallone', 'jason', 'statham', 'jasonstatham', 'jet', 'li', 'jetli', 'russell', 'crowe', 'russellcrowe', 'anthony', 'hopkins', 'anthonyhopkins', 'patrickstewart', 'patrick', 'stewart', 'sirpatstew', 'ian', 'mckellen', 'ianmckellen', 'hugh', 'jackman', 'hugh', 'jackman', 'realhughjackman', 'ralph', 'fiennes', 'ralphfiennes', 'f. murray abraham', 'mathieu', 'amalric', 'mathieuamalric', 'andrew', 'garfield', 'andrewgarfield', 'emma', 'stone', 'emmastone', 'jamie', 'foxx', 'jamiefoxx', 'kellan', 'lutz', 'kellanlutz', 'gaia,weiss', 'gaiaweiss_', 'scott,adkins', 'thescottadkins', 'analeigh', 'tipton', 'ohanaleigh', 'morganfreeman', 'morganfreeman', 'aaron', 'paul', 'aaronpaul_8', 'jesse', 'eisenberg', 'jesseeisenberg', 'jemaine', 'clement', 'jemaineclement', 'amir', 'khan', 'amirkhan', 'salmankhan', 'salman', 'beingsalmankhan', 'shahrukhkhan', 'shahrukh', 'iamsrk', 'hrithik', 'roshan', 'ihrithik', 'abhishek', 'bacchan', 'juniorbachchan', 'ranbir', 'kapoor', 'ranbirkapoor', 'ranveer', 'singh', 'ranveerofficial', 'shahid', 'kapoor', 'shahidkapoor', 'imrankhan', 'imran', 'akshay', 'kumar', 'akshaykumar', 'ajaydevgan', 'ajay', 'devgan', 'imran', 'hashmi', 'imranhashmi', 'amitabh', 'bacchan', 'srbachchan', 'sanjay', 'dutt', 'duttsanjay', 'john', 'abraham', 'thejohnabraham', 'saif', 'ali', 'khan', 'saifalikhan', 'angelina', 'jolie', 'angelinajolie', 'juliaroberts', 'julia', 'roberts', 'jenniferlawrence', 'jennifer', 'lawrence', 'nicole', 'kidman', 'nicolekidman', 'milakunis', 'milakunis', 'jennifer', 'aniston', 'jenniferaniston', 'cameron', 'diaz', 'camerondiaz', 'anne', 'hathaway', 'annehathaway', 'scarlett', 'johansson', 'scarlettjohansson', 'jessica', 'alba', 'jessicaalba', 'kristen', 'stewart', 'kristenstewart', 'emmastone', 'emma', 'stone', 'charlize', 'theron', 'charlizetheron', 'sandrabullock', 'sandra', 'bullock', 'natalieportman', 'natalie', 'portman', 'marion', 'cotillard', 'marioncotillard', 'shailene', 'woodley', 'shailenewoodley', 'kate', 'winslet', 'katewinslet', 'jenniferconnelly', 'jenniferconnelly', 'megan', 'fox', 'meganfox', 'deepika', 'padukone', 'deepikapadukone', 'katrinakaif', 'katrina', 'kaif', 'vidhyabalan', 'vidhyabalan', 'priyanka', 'chopra', 'priyankachopra', 'parineeti', 'chopra', 'parineetichopra', 'kangana', 'ranaut', 'kanganaranaut', 'nargis', 'fakhri', 'nargisfakhri', 'shraddha', 'kapoor', 'shraddhakapoor', 'sonakshi', 'sinha', 'sonakshisinha', 'kareenakapoor', 'kareena', 'kapoor', 'alia', 'bhatt', 'aliabhatt', 'alia08', 'acting', 'act', 'actor', 'actress', 'acted', 'performance']
    else:
        acting.append('acting');
        acting.append('act');
        acting.append('actor');
        acting.append('actress');
        acting.append('acted');
        acting.append('performance');    
    if not direction:
        direction = ["direction","director","cinematography","edit","editing"]
    else:
        direction.append("direction")
        direction.append("director")
        direction.append("cinematography")
        direction.append("edit")
        direction.append("editing")
    music = ["music","songs","song","lyrics"]
    story = ["story","script","plot"]
    movie = ["movie",moviename]
    counttable = {}
    posoutput={}
    negoutput = {}
    posfeatures={}
    negfeatures={}
    for key in inputdata:
            if key in acting:
                valuelist = inputdata[key]
                
                counttable.setdefault("posacting",0)
                counttable["posacting"] += 1
                posoutput.setdefault("acting",0)
                posoutput["acting"] += valuelist[0]
                
                counttable.setdefault("negacting",0)
                counttable["negacting"] += 1
                negoutput.setdefault("acting",0)
                negoutput["acting"] += valuelist[1]
            if key in music:
                valuelist = inputdata[key]
                
                counttable.setdefault("posmusic",0)
                counttable["posmusic"] += 1
                posoutput.setdefault("music",0)
                posoutput["music"] += valuelist[0]
                
                counttable.setdefault("negmusic",0)
                counttable["negmusic"] += 1
                negoutput.setdefault("music",0)
                negoutput["music"] += valuelist[1]
            if key in story:
                valuelist = inputdata[key]
                
                counttable.setdefault("posstory",0)
                counttable["posstory"] += 1
                posoutput.setdefault("story",0)
                posoutput["story"] += valuelist[0]
                
                counttable.setdefault("negstory",0)
                counttable["negstory"] += 1
                negoutput.setdefault("story",0)
                negoutput["story"] += valuelist[1]
            if key in direction:
                valuelist = inputdata[key]
                
                counttable.setdefault("posdirection",0)
                counttable["posdirection"] += 1
                posoutput.setdefault("direction",0)
                posoutput["direction"] += valuelist[0]
                
                counttable.setdefault("negdirection",0)
                counttable["negdirection"] += 1
                negoutput.setdefault("direction",0)
                negoutput["direction"] += valuelist[1]
            if key in movie:
                valuelist = inputdata[key]
                
                counttable.setdefault("posmovie",0)
                counttable["posmovie"] += 1
                posoutput.setdefault("movie",0)
                posoutput["movie"] += valuelist[0]
                
                counttable.setdefault("negmovie",0)
                counttable["negmovie"] += 1
                negoutput.setdefault("movie",0)
                negoutput["movie"] += valuelist[1]
    for key in posoutput:
        if key is "acting":
            posoutput["acting"] = posoutput["acting"] / counttable["posacting"]
        if key is "music":
            posoutput["music"] = posoutput["music"] / counttable["posmusic"]
        if key is "story":
            posoutput["story"] = posoutput["story"] / counttable["posstory"]
        if key is "direction":
            posoutput["direction"] = posoutput["direction"] / counttable["posdirection"]
        if key is "movie":
            posoutput["movie"] = posoutput["movie"] / counttable["posmovie"]
    for key in negoutput:
        if key is "acting":
            negoutput["acting"] = negoutput["acting"] / counttable["negacting"]
        if key is "music":
            negoutput["music"] = negoutput["music"] / counttable["negmusic"]
        if key is "story":
            negoutput["story"] = negoutput["story"] / counttable["negstory"]
        if key is "direction":
            negoutput["direction"] = negoutput["direction"] / counttable["negdirection"]
        if key is "movie":
            negoutput["movie"] = negoutput["movie"] / counttable["negmovie"]
           
    features = ["acting","music","story","direction","movie"]
    for item in features:
        if posoutput.has_key(item) and negoutput.has_key(item):
            if posoutput[item] > negoutput[item]:
                    posfeatures.setdefault(item)
                    posfeatures[item] = posoutput[item]
            else:
                    negfeatures.setdefault(item)
                    negfeatures[item]=negoutput[item]
        else:
            if posoutput.has_key(item):
                posfeatures.setdefault(item)
                posfeatures[item] = posoutput[item]
            if negoutput.has_key(item):
                negfeatures.setdefault(item)
                negfeatures[item]=negoutput[item]
    posn,negn = getscaledscore(posfeatures,negfeatures)
    return posn,negn

#pos,neg = getFeatures(inputdata,movie)
#inputdata = {"bale":[0.9,-0.2],"music":[0.8,-0.3],"songs":[0.7,-0.2],"Randeep":[0.7,-0.2],"script":[0.2,-0.8],"direction":[0.4,-0.7],"movie":[0.7,-0.2]}
#inputdata = {'versaemerge': (0.41836303231652067, 0.5816369676834794), 'wannna': (0.4389887640449438, 0.5610112359550562), 'actress': (0.4271822126199778, 0.5061511207133554), 'directi': (0.4042133520074696, 0.5957866479925303), 'dirge': (0.3759765625, 0.6240234375), 'rts': (0.40902777777777777, 0.5909722222222222), 'follow': (0.5410390786749482, 0.4589609213250519), 'susielouuu': (0.4424776290101368, 0.5575223709898632), 'wed': (0.5031746031746032, 0.49682539682539684), 'smith': (0.5010962566844921, 0.498903743315508), 'li': (0.456901371659775, 0.543098628340225), 'amaze': (0.4103896103896104, 0.44675324675324674), 'aaron': (0.565758547008547, 0.43424145299145295), 'gts': (0.4244791666666667, 0.5755208333333334), 'starter': (0.4260551948051948, 0.5739448051948052), 'th': (0.5, 0.5), 'flabbergast': (0.5, 0.5), 'overcome': (0.44263565891472867, 0.5573643410852713), 'divergent': (0.6041666666666666, 0.3958333333333333), 'song': (0.4125615763546798, 0.5874384236453203), 'de': (0.5636363636363637, 0.43636363636363634), 'da': (0.6092592592592593, 0.3907407407407407), 'rns': (0.5535714285714286, 0.44642857142857145), 'd': (0.5720238095238095, 0.4279761904761905), 'emma': (0.4554383116883117, 0.5445616883116883), 'thrill': (0.5, 0.5), 'edit': (0.5365101911976912, 0.4634898088023088), 'patrick': (0.5011995173285496, 0.4988004826714504), 'p': 0, 't': (0.44364832889677613, 0.5563516711032239), 'rock': (0.48811069882498453, 0.5118893011750154), 'x': (0.3640625, 0.5109375), 'sooodehmansooori': (0.46875, 0.28125), 'gottta': (0.54749000999001, 0.45250999000999), 'freeze': (0.49196428571428574, 0.5080357142857143), 'anyways': (0.5803571428571429, 0.41964285714285715), 'bore': (0.5502854988149105, 0.4497145011850895), 'saturday': (0.3873015873015873, 0.6126984126984127), 'troll': (0.48063675230857894, 0.5193632476914211), 'ohfatima': (0.5090029761904762, 0.4909970238095238), 'sorta': (0.47036706349206353, 0.5296329365079365), 'movie': (0.49908111814609474, 0.5009188818539052), 'please': (0.47638888888888886, 0.5236111111111111), 'theojames': (0.3817460317460318, 0.6182539682539682), 'wmazboa': (0.5122252747252747, 0.48777472527472526), 'ginevraweasly': (0.5512755102040817, 0.44872448979591834), 'rianalikesyou': (0.541005291005291, 0.458994708994709), 'heatherdj': (0.40902777777777777, 0.5909722222222222), 'plot': (0.48149801587301594, 0.5185019841269841), 'friday': (0.4895833333333333, 0.5104166666666666), 'elizabethahaha': (0.41203703703703703, 0.5879629629629629), 'amped': (0.49296875, 0.50703125), 'oh': (0.1935483870967742, 0.8064516129032259), 'o': (0.517867183985605, 0.482132816014395), 'rebecccaaa': (0.5964285714285714, 0.4035714285714286), 'act': (0.6350537634408602, 0.36494623655913977), 'dont': (0.40902777777777777, 0.5909722222222222), 'evans': (0.35416666666666663, 0.6458333333333333), 'scene': (0.625, 0.375), 'rofl': 0, 'termino': (0.5, 0.5), 'spanish': (0.41761363636363635, 0.5823863636363636), 'gosh': (0.3467741935483871, 0.653225806451613), 'wan': (0.5375, 0.4625), 'lol': (0.44974612441130296, 0.5502538755886971), 'music': (0.5536507936507937, 0.44634920634920644), 'coarse': (0.5989583333333334, 0.4010416666666667), 'tom': (0.4296753246753247, 0.5703246753246753), 'john': (0.42646885521885525, 0.5735311447811448), 'asbxo': (0.5896427266081872, 0.4103572733918128), 'direction': (0.5208333333333334, 0.4791666666666667), 'folllowmecam': (0.47638888888888886, 0.5236111111111111), 'excite': (0.5242774403958614, 0.47572255960413856), 'megan': (0.51875, 0.48125), 'glad': (0.5476470588235294, 0.45235294117647057), 'meeeraaaziz': 0, 'ben': (0.47063492063492063, 0.5293650793650794), 'dauntlesssfans': (0.54875, 0.45125000000000004), 'will': (0.5207142857142857, 0.47928571428571426), 'cam': (0.45, 0.5499999999999999), 'personality': (0.48375807709447416, 0.5162419229055258), 'oxfordscommmas': (0.5273053769147519, 0.4726946230852481), 'awesome': (0.5, 0.5), 'al': (0.5045403783208661, 0.49545962167913393), 'cant': (0.500925925925926, 0.499074074074074), 'leeerlo': (0.5, 0.5), 'uae': (0.4042133520074696, 0.5957866479925303), 'tvdplllezria': (0.6170250896057348, 0.38297491039426523), 'awkward': (0.5, 0.5), 'ascii': (0.15625, 0.84375), 'actor': (0.7102272727272727, 0.2897727272727273), 'sunday': (0.4765476190476191, 0.5234523809523809), 'boooj': (0.5357142857142857, 0.46428571428571425), 'disappoint': (0.5, 0.5), 'fools': (0.5, 0.5), 'intend': (0.4157800430778372, 0.5842199569221628), 'monday': (0.5921875, 0.4078125), 'funny': (0.5701058201058202, 0.4298941798941799), 'june': (0.5416666666666666, 0.4583333333333333), 'chris': (0.4300810300810301, 0.56991896991897), 'america': (0.4033333333333333, 0.5966666666666667), 'a': (0.6875, 0.3125), 'don': (0.47681159420289854, 0.5231884057971014), 'artistiq': (0.3733796296296296, 0.6266203703703703), 'i': (0.4237359550561798, 0.5762640449438202), 'camp': (0.34540343915343913, 0.6545965608465608), 'm': (0.5217261904761905, 0.47827380952380955), 'loztaylz': (0.5, 0.5), 'mogggyishere': (0.5, 0.5), 'u': (0.4734375, 0.5265625), 'yell': (0.5111018270944742, 0.48889817290552584), 'blend': (0.5174603174603174, 0.4825396825396826), 'bcs': (0.4375, 0.5625)}
#inputdata = {'arjun': (0.5309995112414467, 0.46900048875855327), 'fabulous': (0.5189393939393939, 0.481060606060606), 'supriya': (0.6142494658119658, 0.3857505341880341), 'saturday': (0.5618675595238095, 0.4381324404761905), 'khan': (0.4088905885780886, 0.5911094114219114), 'illogical': (0.5, 0.5), 'script': (0.5, 0.5), 'movie': (0.55125, 0.44875), 'actor': (0.5, 0.5), 'sonakshisinha': (0.5506350267379679, 0.4493649732620321), 'music': (0.48501602564102564, 0.5149839743589744), 'meinterahero': (0.55125, 0.44875), 'ass': (0.5581080491019936, 0.4418919508980063), 'song': (0.4442857142857143, 0.5557142857142857), 'sexy': (0.6132721445221446, 0.38672785547785543), 'e': (0.5581080491019936, 0.4418919508980063), 'varun': (0.6173109010011124, 0.38268909899888764), 'i': (0.5178565957633053, 0.48214340423669466), 'nargisfakhri': (0.46875, 0.53125), 'm': (0.5178565957633053, 0.48214340423669466), 'o': (0.575, 0.425), 'n': (0.5714285714285715, 0.42857142857142855), 'r': (0.4536681572395858, 0.5463318427604141), 'u': (0.45577415009233185, 0.5442258499076681), 'act': (0.44176339533482384, 0.558236604665176), 'dhawan': (0.4083333333333334, 0.5916666666666667)}
#inputdata = {'story': (0.6697916666666667, 0.3302083333333333), 'song': (0.6205357142857143, 0.3794642857142857), 'edit': (0.40282407407407406, 0.5971759259259259), 'ranbir': (0.40282407407407406, 0.5971759259259259), 'act': (0.7010416666666667, 0.2989583333333333), 'songs': (0.5, 0.5)}
#movie = 'rockstar'
#pos,neg = getFeatures(inputdata, movie)
#print pos
#print neg

