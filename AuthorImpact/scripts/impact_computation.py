
# this script is used to compute the impact on fellows according to the approach described in the paper



if __name__ == "__main__":

    path_file = '../data/co_authors_citations.csv'
    path_out = '../data/impact_analysis.txt'
    with open(path_file,'r') as f:
        l = [item.split(',') for item in f.readlines()[1:]]
        data_fellow = {}
        data_top_author = {}
        data_co_author = {}
        for top_author_id, top_author_name, citations_top_author,\
            fellow_author_id, fellow_author_name, citations_fellow_author,\
            id_paper, paper_citations in l:
                if top_author_id not in data_top_author:
                    data_top_author[top_author_id] = [top_author_name, int(citations_top_author.strip())]
                if fellow_author_id not in data_fellow:
                    data_fellow[fellow_author_id] = [fellow_author_name, int(citations_fellow_author.strip())]
                if top_author_id not in data_co_author:
                    data_co_author.setdefault(top_author_id, [])
                data_co_author[top_author_id].append((fellow_author_id, id_paper, paper_citations))
        impact_result = {}
        for top_author_id in data_top_author:
            top_author_name, citations_top_author = data_top_author[top_author_id]
            co_citation = {}
            for fellow_author_id, id_paper, paper_citations in data_co_author[top_author_id]:
                if fellow_author_id not in co_citation:
                    co_citation[fellow_author_id] = int(paper_citations.strip())
                else:
                    co_citation[fellow_author_id] += int(paper_citations.strip())
            impact = 0
            for fellow_author_id in co_citation:
                fellow_author_name, citations_fellow_author = data_fellow[fellow_author_id]
                assert (co_citation[fellow_author_id] <= citations_fellow_author)
                impact += co_citation[fellow_author_id]/citations_fellow_author
            normalized_impact = impact/len(co_citation)
            impact_result[top_author_id] = [top_author_name, citations_top_author, normalized_impact]

    with open(path_out,'w') as fout:
        for top_author_id in impact_result:
            top_author_name, citations_top_author, normalized_impact = impact_result[top_author_id]
            fout.write('%s,%d,%0.4f\n'%(top_author_name, citations_top_author, normalized_impact))