import pprint as pp
from collections import defaultdict

# SessionID TimePassed TypeOfAction QueryID RegionID ListOfURLs
# SessionID TimePassed TypeOfAction URLID

def parse_log_data(log_file):
    session_data = defaultdict(lambda: defaultdict(list))
    clicks_per_session = defaultdict(list)

    with open(log_file, 'r') as in_file:
        session_id = 0
        for line in in_file:
            line = line.split()
            if line[2] == "C":
                clicks_per_session[session_id-1].append(line[3])    #clicked query_id
            if line[2] == "Q":
                ranked_docs = line[5:]
                rank_count = 0 
                session_data[session_id]['query_id'].append(line[3]) #query id
                for doc in ranked_docs:
                    session_data[session_id]['doc_ids'].append(doc) #doc id
                    rank_count += 1
                session_id += 1

    return session_data, clicks_per_session



if __name__ == "__main__":
    log_file = "test.txt"
    session_data, clicks_per_session = parse_log_data(log_file)
    
    pp.pprint(session_data)
    pp.pprint(clicks_per_session)