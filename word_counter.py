import time
import pymp

def word_counter_dict(target_words, file_names):
    # Obtain list of all words in all documents
    words = []
    for file_name in file_names:
        with open(file_name, 'r') as file:
            data = file.read()
            words += data.split()

    sharedDict = pymp.shared.dict()

    with pymp.Parallel() as p:
        # iterate over the list of items
        for target in p.iterate(target_words):
            sharedDict[target] = 0

            for word in words:
                if word.lower() == target.lower():
                    sharedDict[target] += 1

    return sharedDict


def main():
    # Obtain list of target words
    target_words = ['hate', 'love', 'death', 'night', 'sleep', 'time', 'henry',
        'hamlet', 'you', 'my', 'blood', 'poison', 'macbeth', 'king', 'heart',
        'honest']
    # Obtain list of file names
    file_names = []
    for i in range(1, 9):
        file_names.append('shakespeare' + str(i) + '.txt')

    word_count = word_counter_dict(target_words, file_names)

    print(word_count)


if __name__ == '__main__':
    main()
