from utils.api import get_watcher
from rank.views import rank
from django.shortcuts import render, HttpResponseRedirect
from utils.constants import ErrorList
from rank.views import get_vector, get_score

import operator

def index(request):
    return render(request, "index.html", locals())
def about(request):
    return render(request, "about.html", locals())

def result(request):
    return render(request, "result.html", locals())
def transition(request):
    return render(request, "transition.html", locals())

def testing(request):
    return render(request, "testing.html", locals())

def summoner(request):
    print "returning result"
    if request.is_ajax():
        #deal with the user input here.
        # rank(user)
        # redirect to result display page
        return render(request, "result.html", locals())
    return render(request, "search.html", locals())

def search(request):
    if request.is_ajax():
        if not 'name' in request.POST:
            return render(request, "search.html", locals())

        name = request.POST.get('name')

        try:
            me = get_watcher().get_summoner(name=name)
        except:
            error_code = ErrorList.USER_NOT_FOUND
            return render(request, "search.html", locals())
        match = get_watcher().get_match_list(me['id'],'na')
        match_id_list = [i['matchId'] for i in match['matches'] if i['queue'] == 'TEAM_BUILDER_DRAFT_RANKED_5x5'][:9]
        match_details = []
        all_players_id = dict()

        for match_id in match_id_list:
            match_detail = get_watcher().get_match(match_id)
            match_details.append(match_detail)
            for data in match_detail['participantIdentities']:
                if data['player']['summonerId'] in all_players_id:
                    all_players_id[data['player']['summonerId']].append([match_detail, data['participantId']])
                else:
                    all_players_id[data['player']['summonerId']] = [[match_detail, data['participantId']]]

        friends_id = [key for key, value in all_players_id.items() if len(value) > 1]


        scores = []
        for fid in friends_id:
            if fid == me['id']:
                continue

            data = get_vector(fid, all_players_id)
            score = get_score(data)
            scores.append(score)
            sorted(scores)
            print ("final scores")
            print(scores)

        return render(request, "result.html", locals())
    return render(request, "search.html", locals())
        



                



 
