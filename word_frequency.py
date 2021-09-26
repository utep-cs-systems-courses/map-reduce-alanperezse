import time
import pymp


# Given a list of file names, it returns a 2D array of words that were found in
# the documents (SERIAL)
def load_docs_words(file_names):
    rtn = []
    for file_name in file_names:
        with open(file_name, 'r') as file:
            data = file.read()
            data = data.split()
            rtn.append(data)

    return rtn


# Returns the frequency of some target words in a list of words (SERIAL)
def word_frequency(target, words):
    rtn = 0
    for word in words:
        if target.lower() in word.lower():
            rtn += 1

    return rtn


# Returns a dictionary containing the frequency of the given words in the given
# documents (PARALLEL)
# This algorithm distributes the documents among processes
def targets_frequency_in_docs2(target_words, file_names):
    # Get 2D array of words per document
    content_docs = load_docs_words(file_names)

    # Set up shared dictionary
    shared_dict = pymp.shared.dict()

    with pymp.Parallel() as p:
        dict_lock = p.lock
        # Update shared dictionary
        for i in p.range(len(target_words)):
            shared_dict[target_words[i]] = 0

        # Iterate over documents
        for content_doc in p.iterate(content_docs):
            print(f'Thread [{p.thread_num} of {p.num_threads}] is evaluating document starting with {content_doc[0]}')

            private_dict = dict()

            # Update private dictionary with frequency of target words in document
            for target in target_words:
                private_dict[target] = word_frequency(target, content_doc)

            # Reduce
            dict_lock.acquire()
            for target, freq in private_dict.items():
                shared_dict[target] += freq
            dict_lock.release()

    return shared_dict


# Returns a dictionary containing the frequency of the given words in the given
# documents (PARALLEL)
# This algorithm distributes the words among processes
def targets_frequency_in_docs(target_words, file_names):
    # Obtain single list of all words in all documents
    words = []
    for file_name in file_names:
        with open(file_name, 'r') as file:
            data = file.read()
            words += data.split()

    shared_dict = pymp.shared.dict()

    with pymp.Parallel() as p:
        # Each processor gets its own target word
        for target in p.iterate(target_words):
            print(f'Thread [{p.thread_num} of {p.num_threads}] is evaluating word \'{target}\'')
            # Check for target word in the list of all words in all documents
            shared_dict[target] = word_frequency(target, words)

    return shared_dict


def main():
    # Obtain list of target words
    target_words = ['hate', 'love', 'death', 'night', 'sleep', 'time', 'henry',
        'hamlet', 'you', 'my', 'blood', 'poison', 'macbeth', 'king', 'heart',
        'honest']

    # Obtain list of file names
    file_names = []
    for i in range(1, 9):
        file_names.append('shakespeare' + str(i) + '.txt')


    # Time of algorithm 1
    print('Performing algorithm 1 where target words are divided among processes')
    alg1_t0 = time.clock_gettime(time.CLOCK_MONOTONIC_RAW)
    word_count1 = targets_frequency_in_docs(target_words, file_names)
    alg1_t1 = time.clock_gettime(time.CLOCK_MONOTONIC_RAW)
    print()

    # Time of algorithm 2
    print('Performing algorithm 2 where documents are divided among processes')
    alg2_t0 = time.clock_gettime(time.CLOCK_MONOTONIC_RAW)
    word_count2 = targets_frequency_in_docs2(target_words, file_names)
    alg2_t1 = time.clock_gettime(time.CLOCK_MONOTONIC_RAW)
    print()

    # Test results match from algorithm to algorithm and print
    print('Target words frequency:')
    for word, freq in word_count1.items():
        assert(freq == word_count2[word])   # Assertion Test
        print(f'\t{word} - {freq}')

    print('All tests passed')
    print('Time taken to search word frequency by algorithm 1: {:.4}'.format(alg1_t1 - alg1_t0))
    print('Time taken to search word frequency by algorithm 2: {:.4}'.format(alg2_t1 - alg2_t0))


if __name__ == '__main__':
    main()
