from votesmart import votesmart, VotesmartApiError
import os
from numpy import random
import math
import json

votesmart.apikey = '11ddf9f9f231897cb3eb84ff5f7e9fd4'

OFFICEID_senator = 6

TESTLIMIT = 4

nonstate_ids = ['AS', 'DC', 'GU', 'NA', 'PR', 'VI']

vote_val = {'yea':1, 'nay':-1}

pathname = os.path.dirname(os.path.realpath(__file__))
filename = os.path.join(pathname, "voteInput.txt")
fileOut=open(filename, "w")

def stateIdsToNames():
    stateids = {}
    for st in votesmart.state.getStateIDs():
        if st.stateId not in nonstate_ids:
            stateids[st.stateId] = st.name
    return stateids
    

def senatorIdsToNames(stateids):
    sen_ids = {}
    for stid in sorted(stateids):
        for official in votesmart.officials.getByOfficeState(OFFICEID_senator, stid):
            cand_id = official.candidateId
            cand_name = str(official)
            sen_ids[cand_id] = cand_name
    return sen_ids


def billIdsToTitles(year):
    bill_ids = {}
    for bill in votesmart.votes.getBillsByYearState(2011):
        bill_id = bill.billId
        bill_title = bill.title          # could also use bill.officialTitle
        bill_ids[bill_id] = bill_title
    return bill_ids


def senatorVotes(bill_action, senator_ids):
    votes = []
    vcount = 0
    for sen in senator_ids:
        vval = 0
        try:
            vote = votesmart.votes.getBillActionVoteByOfficial(bill_action.actionId, sen).action
            vval = vote_val.get(vote.lower(), 0)
        except VotesmartApiError:
            pass
        vcount += abs(vval)
        votes += [vval]
    if vcount > 0:
        return votes
    return None


    
#------------------------------------------

def main():
    state_dict = stateIdsToNames()
    senator_dict = senatorIdsToNames(state_dict.keys())
    bill_dict = billIdsToTitles(2012)

    sens = senator_dict.keys()[:TESTLIMIT]
    print 'Senators:', [senator_dict[s].replace('Senator ', '') for s in sens]
    
    for bill_id in bill_dict.keys():
        try:
            actions = votesmart.votes.getBill(bill_id).actions
            print bill_id, bill_dict[bill_id]
            for action in actions:
                votes = senatorVotes(action, sens)
                if votes:
                    print '\t', action, votes
                    outString = json.dumps([bill_id, bill_dict[bill_id], votes]) + "\n"
                    fileOut.write(outString)
                else:
                    print '\t', action, "No votes data"
        except:
            print "\t pass"
            pass
            

        
if __name__ == '__main__':
    main()
