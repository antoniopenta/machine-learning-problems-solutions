import networkx as nx

#this script is used to explore the graph of citations in Gelphi

if __name__ == "__main__":

    path_citation_network = '../data/author_cite_top_author.txt'
    path_tot_citation = '../data/author_total_citations.txt'
    path_out = '../data/influence_analysis.txt'
    path_graph = '../data/author_cite_top_author.gexf'

    with open(path_citation_network, 'r') as f:
        l = [item.split(',') for item in f.readlines()[1:]]

    with open(path_tot_citation, 'r') as f:
        citation_dictionary = {item.split(',')[0]: int(item.split(',')[2].strip()) for item in f.readlines()[1:]}

    G = nx.DiGraph()

    for author_id, author_name, top_author_id, top_author_name, number_citation in l:
        if author_id in citation_dictionary:
            G.add_node(author_id, name=author_name, top=False, tot_ci=citation_dictionary[author_id])

        G.add_node(top_author_id, name=top_author_name, top=True, tot_ci=citation_dictionary[top_author_id])
        G.add_edge(author_id, top_author_id, num_cit=int(number_citation.strip()))
        # let us color the nodes of the top author in red
        G.node[top_author_id]['viz'] = {'color': {'r': 255, 'g': 0, 'b': 0, 'a': 0}}

    nx.write_gexf(G, path_graph)


