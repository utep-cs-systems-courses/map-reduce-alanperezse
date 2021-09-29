# Report:
    Student: Alan Perez
    CS 4175 12PM TR

### Intructions:
The word_frequency.py may be used as a script or as a module. The problem of
finding the target words in all the Shakespeare documents is done by running the
script. The problem is solved by both algorithms implemented in the script.

You may run the script without passing any flags to the interpreter, such as:

    python3 word_frequency.py

If the file is used as a module, there exists only two important methods,
called targets_frequency_in_docs(target_words, file_names), and
targets_frequency_in_docs(target_words, file_names). target_words must be a
list of strings that will be searched on the documents. file_names must be a
list of strings representing the names of the documents to open.

### Issues:
The main issue I had at the beginning was with errors regarding loading the
contents of the docs in a parallel fashion for the first algorithm. I stopped
trying to do so after a few attempts.

One issue is that the number of 'you' words in the document differs; My
algorithms count 2 less instances of the word in total. I attempted doing this
algorithm linearly in a past iteration, and I was getting the same issue. Thus,
it is not a race condition, and it is most likely due to the way I am comparing
the words to the target words.

### Time:
Algorithm 1 was done in less than one hours. Generating algorithm 2 took less
than two hours. There was a lot of time spent trying to make everything clean
and easy to understand.

### Performance measurements:
The following measurements are an average of running the script 5 times for
each of the below number of threads

            Algorithm 1         Algorithm 2

1 thread:   5.6102 seconds      5.5728 seconds

2 threads:  5.6224 seconds      5.5934 seconds

4 threads:  3.218 seconds       2.8538 seconds

8 threads:  3.6164 seconds      2.98 seconds

### Analysis:
The run with 4 threads seems to be the quickest. The CPU of my computer is
capable of running 4 threads, so that would explain why even though we have 8
or more processes in either algorithm, it is not as fast or efficient as using
the exact number of available threads. There is also a thread that seems to
remain unused (for instance, when running 4 threads, thread 0 is never used),
which could be related to why going from 1 to 2 threads makes the program
slower. This can be verified by simply running the script, as the algorithm
will inform the user how the jobs are separated between threads, and which
thread is doing what.

### Observations:
Algorithm 2 is consistently faster than the first algorithm. This is most
likely due to the fact that this algorithm loads documents in the parallel part
whenever they are needed, as opposed to the algorithm 1 which loads all the
documents at the beginning linearly.

There is also an interesting thing I found out while updating the dictionary.
One of the first iterations of algorithm 1 would update the dictionary at every
comparison. Once I implemented the word_frequency method and proceeded to
update the dictionary once per target word, the algorithm went from taking over
15 second to less than 5. The hypothesis being that either accessing or
updating an element in a dictionary is an expensive operation that should be
done as few times as possible.

### Output from cpuInfoDump program:
model name      : Intel(R) Core(TM) i5-7200U CPU @ 2.50GHz

      4      36     216
