# Meta Learner: intelligent bookmark manager
A proof of concept (done in a short hackaton) of a bookmark and learning manager to structure your anti library. The main idea is to:

1. Import a large amount of unmanageable bookmarks
2. Crawl their web pages and download raw text data
3. Save the data into a database and then mine for patterns with **ML**.
4. Display the results in a frontend (build in `Flask)`.
5. Extract captions from the `youtube` bookmarks, in order to be able to find useful information from courses, presentations.
