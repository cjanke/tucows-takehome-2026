Throughout the project, I used Claude to assist. I started by feeding in the pdf, and approached it like I would pair programming. Broad highlights:

- Used Claude to think through project structure, choice of library, and docker set up.
    - Independently verified that FastAPI, Pydantic, etc. were appropriate choices
  by researching community adoption and use cases before committing to them.
    - Pointed out a redundant `psycopg2` import in `database.py` and removed it.
    - I haven't set up many Docker projects from scratch, so I added comments and took a lot of notes for myself for the future as well.
- Proposed my idea for how to handle the db schema (see below) to Claude before letting Claude write it out.
    - My proposal: "My first thought on how to represent a graph in a db would be like a table where each row represents an edge, column 1 = first point, column2 = 2nd point, and column3 = weight / cost. maybe also a separate table for a complete list of nodes. And then indices for looking up based on first column, etc. what do you think?"
    - Claude also originally proposed having graphs in their own table, which seemed like a good idea at the time - after re-reading the spec later, I realized we didn't need to handle the case where multiple graphs are being uploaded. I decided to leave the table as is since it's more flexible for the future, but removed Claude's unnecessary references to it in the API and later SQL query.
- For each step of coding, I started with Claude writing out the bulk of it before reviewing it thoroughly, adding my own comments, and asking about adding tests. Notable details:
    - Found a bug in `find_all_paths` where it was only returning the first path it found.
        - For Claude's v1, if a path was found and start == end, it called `return [current_path.copy()]`.
        - Changed this to `paths.append(current_path.copy())` instead.
    - I noticed that we weren't checking for multiple from/to tags in the parser and I fixed that.
    - Claude originally had `parse_graph` as one big function, I refactored it and broke it down into `parse_nodes` and `parse_edges` for readability
    - Asked Claude if we should handle errors besides ET parsing error, Claude agreed and said "file not found" is good one to add
    - Claude's first few files didn't have type hints, I added them myself and requested type hinting for future files.
- Testing details
    - Claude initially proposed only `sample/sample_graph.xml`. I requested `simple_graph.xml`, and I added the rest of the sample xmls myself (`invalid_*`, `no_edge_graph*`) because we weren't checking the validation rules provided in the spec.
    - Claude's initial version of test_graph.py had checks like "len of paths == 3" for `find_all_paths`. I changed it to match against the exact output.
        - This does make the tests slightly more brittle for the future, but it also could catch some bugs if the paths don't actually match what's expected.
        - This also makes the tests more helpful as a source of documentation for function outputs.
- Cycle detection SQL
    - I relied on Claude + did a lot of interrogating the solution and asking questions. I hadn't used the RECURSIVE keyword before so it ended up being a good learning opportunity.
    - Claude's first iteration of the SQL query spit out a not-very-readable list of nodes that can eventually lead to a cycle (eg, `a, b, c, d, e` for `sample/sample_graph.xml`)
        - I went back and forth with Claude to create a query that only displays the nodes that are actually part of cycles.
        - I also requested a version that prints the cycle list out for easy reviewing and testing. This led me to realize that we weren't including self loops as a cycle in our check, which was then fixed.
        - The resulting SQL had a lot of redundant lines (we had both a "nodes visited" list and a "cycle path" for the final output) and I streamlined it to just use nodes visited.

This was the final SQL output after iterating with Claude which I think is much nicer:

| start_node | cycle_path |
|------------|------------|
| a | {a,b,e,a} |
| a | {a,a} |
| a | {a,e,a} |
| e | {e,a,c,e} |
| e | {e,a,e} |
| a | {a,c,e,a} |
| e | {e,a,b,e} |
| b | {b,e,a,b} |
| c | {c,e,a,c} |
