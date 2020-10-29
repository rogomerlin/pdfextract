import collections
import numpy as np
import spacy
import json
from spacy.matcher import Matcher
nlp = spacy.load('en')

def get_det_dict():
    dict = collections.defaultdict(list)
    matcher = Matcher(nlp.vocab)
    # name matcher
    name = [{"ORTH": "Name"}, {"ORTH": ":"}, {"POS": "PROPN"}]
    # NDIS id matcher
    id = [{"ORTH": "Number"}, {"ORTH": ":"}, {"IS_DIGIT": True}]
    start_date = [{"ORTH": "start"}, {"ORTH": "date"}, {"ORTH": ":"}, {"IS_DIGIT": True}, {"IS_ALPHA": True}, {"IS_DIGIT": True}]
    review_date = [{"ORTH": "review"}, {"ORTH": "due"}, {"ORTH": "date"}, {"ORTH": ":"}, {"IS_DIGIT": True}, {"IS_ALPHA": True}, {"IS_DIGIT": True}]
    dob = [{"ORTH": "Date"}, {"ORTH": "of"}, {"ORTH": "birth"}, {"IS_DIGIT": True}, {"IS_ALPHA": True}, {"IS_DIGIT": True}]
    mob = [{"ORTH": "Mobile"}, {"ORTH": ":"}, {"IS_DIGIT": True}]
    matcher.add("0", None, name)
    matcher.add("1", None, id)
    matcher.add("2", None, start_date)
    matcher.add("3", None, review_date)
    matcher.add("4", None, dob)
    matcher.add("5", None, mob)
    matches = matcher(doc)
    for match_id, start, end in matches:
        string_id = doc.vocab.strings[match_id]
        switcher = {
            0: 'NDIS id',
            1: 'Full Name',
            2: 'NDIS plan start date',
            3: 'NDIS plan review due date',
            4: 'Date of birth',
            5: 'Mobile id',
        }
        i = 0
        while i <= 6:
            if string_id == str(i):
                dict[switcher.get(i)].append(start)
            i += 1
    return dict

def get_sup_dict():
    dict = collections.defaultdict(list)
    m_supCat = Matcher(nlp.vocab)
    p0 = [{"ORTH": "Total"}, {"ORTH": "Core"}, {"ORTH": "Supports"}]
    m_supCat.add("0", None, p0)
    p1 = [{"ORTH": "Total"}, {"ORTH": "Capacity"}, {"ORTH": "Building"}, {"ORTH": "Supports"}]
    m_supCat.add("1", None, p1)
    p2 = [{"ORTH": "Total"}, {"ORTH": "Capital"}, {"ORTH": "Supports"}]
    m_supCat.add("2", None, p2)
    p3 = [{"ORTH": "My"}, {"ORTH": "Core"}, {"ORTH": "Supports"}]
    m_supCat.add("3", None, p3)
    p4 = [{"ORTH": "Consumables"}]
    m_supCat.add("4", None, p4)
    p5 = [{"ORTH": "Daily"}, {"ORTH": "Activities"}]
    m_supCat.add("5", None, p5)
    p6 = [{"ORTH": "Assistance"}, {"ORTH": "with"}, {"ORTH": "Social"}, {"ORTH": "and"}, {"ORTH": "Community"}, {"ORTH": "Participation"}]
    m_supCat.add("6", None, p6)
    p7 = [{"ORTH": "Transport"}]
    m_supCat.add("7", None, p7)
    p8 = [{"ORTH": "Support"}, {"ORTH": "Coordination"}]
    m_supCat.add("8", None, p8)
    p9 = [{"ORTH": "CB"}, {"ORTH": "Home"}, {"ORTH": "Living"}]
    m_supCat.add("9", None, p9)
    p10 = [{"ORTH": "CB"}, {"ORTH": "Social"}]
    m_supCat.add("10", None, p10)
    p11 = [{"ORTH": "CB"}, {"ORTH": "Employment"}]
    m_supCat.add("11", None, p11)
    p12 = [{"ORTH": "CB"}, {"ORTH": "Relationships"}]
    m_supCat.add("12", None, p12)
    p13 = [{"ORTH": "CB"}, {"ORTH": "Health"}, {"ORTH": "and"}, {"ORTH": "Wellbeing"}]
    m_supCat.add("13", None, p13)
    p14 = [{"ORTH": "CB"}, {"ORTH": "Lifelong"}, {"ORTH": "Learning"}]
    m_supCat.add("14", None, p14)
    p15 = [{"ORTH": "CB"}, {"ORTH": "Choice"}, {"ORTH": "and"}, {"ORTH": "Control"}]
    m_supCat.add("15", None, p15)
    p16 = [{"ORTH": "CB"}, {"ORTH": "Daily"}, {"ORTH": "Activity"}]
    m_supCat.add("16", None, p16)
    p17 = [{"ORTH": "Assistive"}, {"ORTH": "Technology"}]
    m_supCat.add("17", None, p17)
    p18 = [{"ORTH": "Home"}, {"ORTH": "Modifications"}]
    m_supCat.add("18", None, p18)
    matches = m_supCat(doc)
    for match_id, start, end in matches:
        sid = doc.vocab.strings[match_id]
        switcher = {
            0: 'Total Core Supports',
            1: 'Total Capacity Building Supports',
            2: 'Total Capital Supports',
            3: 'My Core Supports',
            4: 'Consumables',
            5: 'Daily Activities',
            6: 'Assistance with Social and Community Participation',
            7: 'Transport',
            8: 'Support Coordination',
            9: 'Improved Living Arrangements (CB Home Living)',
            10: 'Increased Social & Community Participation (CB Social Community and Civic Participation)',
            11: 'Finding & Keeping a Job (CB Employment)',
            12: 'Improved Relationships (CB Relationships)',
            13: 'Improved Health and Wellbeing (CB Health and Wellbeing)',
            14: 'Improved Learning (CB Lifelong Learning)',
            15: 'Improved Life Choices (CB Choice and Control)',
            16: 'Improved Daily Living (CB Daily Activity)',
            17: 'Assistive Technology',
            18: 'Home Modifications'
        }
        i = 0
        while i <= 19:
            if sid == str(i):
                dict[switcher.get(i)].append(end)
            i += 1
    return dict

def get_goal_dict():
    dict = collections.defaultdict(list)
    matcher_goal = Matcher(nlp.vocab)
    pattern1 = [{"LOWER": "short"}, {"IS_PUNCT": True},{"LOWER": "term"}, {"LOWER": "goal"}]
    matcher_goal.add("short", None, pattern1)
    pattern2 = [{"LOWER": "long"}, {"IS_PUNCT": True}, {"LOWER": "term"}, {"LOWER": "goal"}]
    matcher_goal.add("long", None, pattern2)
    matches = matcher_goal(doc)
    for match_id, start, end in matches:
        string_id = doc.vocab.strings[match_id]
        if string_id == "short":
            dict["short"].append(start)
        elif string_id == "long":
            dict["long"].append(start)
    return dict

def get_mon_arr():
    monList = []
    for token in doc:
        if token.tag_ == '$':
            monList.append(token.i)
    arr = np.array(monList)
    if len(arr) != 0:
        return arr
    else:
        return "no $ index found"

def get_budget(supArr, monArr):
    diffs = []
    i = 0
    while i <= (len(supArr)-1):
        diff = abs(supArr[i]-monArr)
        diffs.append(diff)
        i += 1
    diffsArr = np.array(diffs)
    minDiff = diffsArr.min()
    numIndex = np.where(diffsArr == minDiff)
    i = 0
    while i <= (len(supArr)-1): 
        monIndex = numIndex[1][i]
        docIndex = monArr[monIndex]
        i += 1
        for token in doc:
            if doc[docIndex].tag_ == '$':
                budget = '$' + doc[docIndex + 1].text
                return budget
    pass

def get_part_arr():
    pronList = []
    for token in doc:
        if token.text == 'to':
            pronList.append(token.i)
    arr = np.array(pronList)
    if len(arr) != 0:
        return arr
    else:
        return "no \'to\' found"

def get_goal_phrase(goalArr, partArr):
    i = 0
    docIndexes = []
    while i <= (len(goalArr)-1):
        diff = partArr-goalArr[i]
        negDiff = [j for j, x in enumerate(diff) if x < 0]
        posDiff = np.delete(diff, negDiff)
        # correct
        abDiffIndex = np.where(diff == posDiff[0])
        # correct
        partIndex = partArr[abDiffIndex]
        # partIndex test works but part array not meaningful data
        docIndex = partIndex[0]
        docIndexes.append(docIndex)
        i += 1
    phrases = []    
    for token in doc:
        if token.i in docIndexes:
            phrase = token.text
            j=1
            while doc[token.i+j].text != '.' :
                phrase = phrase + ' ' + doc[token.i+j].text
                j += 1
            phrases.append(phrase)
    return phrases

def get_det_category(indexes):
    catList = []
    switcher = {
        0: 'NDIS id',
        1: 'Full Name',
        2: 'NDIS plan start date',
        3: 'NDIS plan review due date',
        4: 'Date of birth',
        5: 'Mobile id'
    }
    for i in indexes:
        catList.append(switcher.get(i))
    return catList

def get_sup_category(indexes):
    catList = []
    switcher = {
            0: 'Total Core Supports',
            1: 'Total Capacity Building Supports',
            2: 'Total Capital Supports',
            3: 'My Core Supports',
            4: 'Consumables',
            5: 'Daily Activities',
            6: 'Assistance with Social and Community Participation',
            7: 'Transport',
            8: 'Support Coordination',
            9: 'Improved Living Arrangements (CB Home Living)',
            10: 'Increased Social & Community Participation (CB Social Community and Civic Participation)',
            11: 'Finding & Keeping a Job (CB Employment)',
            12: 'Improved Relationships (CB Relationships)',
            13: 'Improved Health and Wellbeing (CB Health and Wellbeing)',
            14: 'Improved Learning (CB Lifelong Learning)',
            15: 'Improved Life Choices (CB Choice and Control)',
            16: 'Improved Daily Living (CB Daily Activity)',
            17: 'Assistive Technology',
            18: 'Home Modifications'
        }
    for i in indexes:
        catList.append(switcher.get(i))
    return catList

def print_phrases(phrases):
    for i in phrases:
        print(i)
    return '-processing-'

def write_json(data, filename='data.json'):
    with open("data.json", "a+") as f:
        json.dump(data, f)

def save_all_to_json():
    data = {}
    supDict = get_sup_dict()
    monArr = get_mon_arr()
    supType = get_sup_category([*range(0,19,1)])
    sKeys = list(supDict.keys())
    sVals = list(supDict.values())
    detDict = get_det_dict()
    detType = get_det_category([*range(0,6,1)])
    dKeys = list(detDict.keys())
    dVals = list(detDict.values())
    partArr = get_part_arr()
    goalDict = get_goal_dict()
    gKeys = list(goalDict.keys())
    gVals = list(goalDict.values())
    dIndex = dVals[3][0]
    idNum = doc[dIndex + 2].text
    data[idNum] = []
    temp = data[idNum]
    x = {}
    i = 0
    while i <= (len(detDict)-1):
        if dKeys[i] == 'Full Name':
            dIndex = dVals[i][0]
            j = 2
            while j <= 5 and doc[dIndex + j].pos_ == 'PROPN' and doc[dIndex + j].text != 'Page':
                name = ''
                name += doc[dIndex + j].text.capitalize() + ' '
                j += 1
                y = {dKeys[i]: name}
                x.update(y)
        elif dKeys[i] == 'NDIS plan start date':
            dIndex = dVals[i][0]
            sDate = doc[dIndex + 3].text + ' ' + doc[dIndex + 4].text + ' ' + doc[dIndex + 5].text
            y = {dKeys[i]: sDate}
            x.update(y)
        elif dKeys[i] == 'NDIS plan review due date':
            dIndex = dVals[i][0]
            rDate = doc[dIndex + 4].text + ' ' + doc[dIndex + 5].text + ' ' + doc[dIndex + 6].text
            y = {dKeys[i]: rDate}
            x.update(y)
        elif dKeys[i] == 'Date of birth':
            dIndex = dVals[i][0]
            dob = doc[dIndex + 3].text + ' ' + doc[dIndex + 4].text + ' ' + doc[dIndex + 5].text
            y = {dKeys[i]: dob}
            x.update(y)
        elif dKeys[i] == 'Mobile id':
            dIndex = dVals[i][0]
            mob = doc[dIndex + 2].text
            y = {dKeys[i]: mob}
            x.update(y)
        i += 1
    temp.append(x)
    x = {}
    i = 0
    while i <= (len(supDict)-1):
        if sKeys[i] in supType:
            supList = sVals[i]
            supArr = np.array(supList)
            budget_val = get_budget(supArr, monArr)
            y = {sKeys[i]: budget_val}
            x.update(y)
        i += 1
    temp.append(x)
    x = {}
    i = 0
    while i <= (len(goalDict)-1):  
        goalList = gVals[i]
        goalArr = np.array(goalList)
        key = gKeys[i].capitalize() + " Term Goals: "
        phraseArr = get_goal_phrase(goalArr, partArr)
        y = {key: phraseArr}
        x.update(y)
        i += 1
    temp.append(x)
    write_json(data)

save_all_to_json()
# main executable
exit()