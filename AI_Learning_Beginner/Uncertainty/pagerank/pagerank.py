import os
import random
import re
import sys
import copy 

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    result_dict = {}
    current_links = len(corpus[page])

    if current_links != 0:
        for link in corpus:
            result_dict[link] = (1 - damping_factor) / len(corpus)
        for link in corpus[page]:
            result_dict[link] += damping_factor / current_links
        
    else:
        for link in corpus:
            result_dict[link] = 1/len(corpus)

    return result_dict
    

   
    


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    result_dict = {}
    for page in corpus:
        result_dict[page] = 0
        
    start_point = random.choice(list(corpus.keys()))
    

    for x in range(1,n):
            first_model = transition_model(corpus, start_point, damping_factor)

            for page in result_dict:
                result_dict[page] = (first_model[page] + result_dict[page]*(x-1))/x
            

            start_point = random.choices(list(result_dict.keys()), list(result_dict.values()), k=1)[0]
            

       
    return result_dict
    


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    result_dict = {}
    for page in corpus:
        result_dict[page] = 1/len(corpus)

    difference = True
    while difference:
        difference = False
        temp_dict = copy.deepcopy(result_dict)
        for page in corpus:
            result_dict[page] = ((1-damping_factor)/len(corpus)) + (sum_calc(corpus, page, result_dict, damping_factor))
            difference = False or abs(temp_dict[page] - result_dict[page]) > 0.001


    return result_dict


def sum_calc(corpus, page, result_dict, damping_factor):
    
    i = 0
    for temp_page in corpus:
        if page in corpus[temp_page]:
            i += result_dict[temp_page] / len(corpus[temp_page])

    return i*damping_factor




if __name__ == "__main__":
    main()
