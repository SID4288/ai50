import os
import random
import re
import sys

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
    result = {}
    
    # If page has no outgoing links, choose randomly among all pages
    if len(corpus[page]) == 0:
        for p in corpus:
            result[p] = 1 / len(corpus)
    else:
        # For each page in the corpus
        for p in corpus:
            # Probability from following a link from current page
            if p in corpus[page]:
                link_probability = damping_factor / len(corpus[page])
            else:
                link_probability = 0
            
            # Probability from random page selection
            random_probability = (1 - damping_factor) / len(corpus)
            
            result[p] = link_probability + random_probability
    
    return result


def sample_pagerank(corpus, damping_factor, n):
    counts = {page: 0 for page in corpus}
    pages = list(corpus.keys())

    # First sample is chosen uniformly at random.
    current_page = random.choice(pages)

    for _ in range(n):
        counts[current_page] += 1

        probabilities = transition_model(corpus, current_page, damping_factor)
        current_page = random.choices(
            population=list(probabilities.keys()),
            weights=list(probabilities.values()),
            k=1
        )[0]

    return {page: counts[page] / n for page in counts}


def iterate_pagerank(corpus, damping_factor):
    num_pages = len(corpus)
    pagerank = {page: 1 / num_pages for page in corpus}

    while True:
        new_pagerank = {}
        for page in corpus:
            rank_sum = 0
            for other_page in corpus:
                if page in corpus[other_page]:
                    rank_sum += pagerank[other_page] / len(corpus[other_page])
                elif len(corpus[other_page]) == 0:
                    rank_sum += pagerank[other_page] / num_pages
            
            new_pagerank[page] = (1 - damping_factor) / num_pages + damping_factor * rank_sum
        
        # Check for convergence
        if all(abs(new_pagerank[page] - pagerank[page]) < 0.001 for page in pagerank):
            break
        
        pagerank = new_pagerank

    return pagerank

if __name__ == "__main__":
    main()
