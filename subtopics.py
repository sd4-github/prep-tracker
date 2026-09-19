"""
Sub-topic classifier
====================
The JSON only says which *topic* a problem belongs to (e.g. "Arrays & Hashing").
Some topics are huge, so this module splits them into sub-topics at load time.
The JSON file itself is never modified.

How it works, in order:
  1. PINNED   – an exact problem-id -> sub-topic override (highest priority)
  2. RULES    – the first regex (matched against the title) that hits wins
  3. FALLBACK – whatever is left goes to the topic's catch-all bucket

Topics that are not listed in RULES simply get no sub-topic chips.

To fix a misplaced problem, add it to PINNED. To tune a whole group,
edit the regex in RULES. The order of the RULES list is the order the chips
are shown in the UI.
"""

import re

# ─────────────────────────────────────────────
# 1. PINNED: problem id -> sub-topic
#    (only needed where a title regex can't tell)
# ─────────────────────────────────────────────
PINNED: dict[int, str] = {
    # Arrays & Hashing → Two Pointers (classics whose titles don't give it away)
    75: "Two Pointers",     # Sort Colors
    88: "Two Pointers",     # Merge Sorted Array
    283: "Two Pointers",    # Move Zeroes
    905: "Two Pointers",    # Sort Array By Parity
    922: "Two Pointers",    # Sort Array By Parity II
    977: "Two Pointers",    # Squares of a Sorted Array
    # Trees → Segment Tree & BIT
    307: "Segment Tree & BIT", 308: "Segment Tree & BIT", 315: "Segment Tree & BIT",
    699: "Segment Tree & BIT", 850: "Segment Tree & BIT", 1157: "Segment Tree & BIT",
    1649: "Segment Tree & BIT", 2158: "Segment Tree & BIT", 2179: "Segment Tree & BIT",
    2213: "Segment Tree & BIT", 2286: "Segment Tree & BIT", 2407: "Segment Tree & BIT",
    2426: "Segment Tree & BIT", 2569: "Segment Tree & BIT", 2907: "Segment Tree & BIT",
    2921: "Segment Tree & BIT", 2926: "Segment Tree & BIT", 3161: "Segment Tree & BIT",
    3165: "Segment Tree & BIT", 3187: "Segment Tree & BIT", 3935: "Segment Tree & BIT",
    # Graphs → Union Find
    305: "Union Find",
}

# ─────────────────────────────────────────────
# 2. RULES: topic -> ordered [(sub-topic, title regex)]
# ─────────────────────────────────────────────
RULES: dict[str, list[tuple[str, str]]] = {

    "Arrays & Hashing": [
        ("Design", r"^Design |Data structure design|Iterator|Logger|Hit Counter|Snapshot Array|GetRandom|"
                   r"Circular (Queue|Deque)|Leaderboard|Tracker|Authentication Manager|Allocator|Spreadsheet|"
                   r"Data Stream|My Calendar|Range Module|TinyURL|Underground System|Browser History|"
                   r"Ordered Stream|Order Management|Exam Scores|Last K Numbers|Fancy Sequence|RLE Iterator|"
                   r"Recent Calls|O`one|Web Crawler|Throne Inheritance|Parking System|Simple Bank|"
                   r"Discount Every|Tweet Counts|Finding Pairs With|Range Frequency Queries|"
                   r"Subrectangle Queries|Sparse Vectors|Moving Average|Encrypt and Decrypt|"
                   r"Unique Word Abbreviation|First Unique Number|Uploaded Prefix|Operations on Tree"),
        ("Two Pointers", r"Two Sum II|3Sum|4Sum(?! II)|Two Sum Less|Sorted Array( II)?$|Remove Element|"
                         r"Reverse String$|Reverse Vowels|Valid Palindrome|Container With|Trapping Rain|"
                         r"Two Furthest|Long Pressed|Backspace String|Reverse Only Letters|Duplicate Zeros|"
                         r"Reverse Prefix|Count Pairs Whose Sum|K-Sum Pairs|Three Sorted Arrays|"
                         r"Merge Strings Alternately|Move Pieces|Rearrange Array Elements by Sign|"
                         r"Partition Array According|Shortest Word Distance"),
        ("Prefix Sum", r"Subarray Sum|Range Sum|Prefix Sum|Running Sum|Pivot Index|Except Self|"
                       r"Contiguous Array|Continuous Subarray Sum|Subarray Sums|Odd Length Subarrays|"
                       r"Range Addition|Flight Bookings|Matrix Block Sum|Submatrices|Make Sum Divisible|"
                       r"Middle Index|Left and Right Sum|Plates Between|Ways to Split|Split Array|"
                       r"Into Three Parts|Non-Overlapping Subarrays|Ways to Partition|Describe the Painting|"
                       r"Brightest Position|Sum of Distances|Equal Sum Grid|Count Partitions|"
                       r"Sum of Variable|Score of All Prefixes|Widest Pair|Prefix Common|Zero-Filled"),
        ("Matrix & Grid", r"Matrix|Grid|Diagonal|Board|Rotate Image|Spiral|Sudoku|Tic-Tac-Toe|"
                          r"Game of Life|Toeplitz|Image|Battleships|Lonely Pixel|Skyline|Crossword|"
                          r"Farmland|Chessboard|Snake in|Magic Square|Rhombus|Snakes and Ladders|"
                          r"Brick Wall|Cells|Rook|Queens That Can|Rotating the Box|Black Blocks"),
        ("Hash Map & Set", r"^Two Sum$|Anagram|Duplicate|Longest Consecutive|Frequen|Isomorphic|"
                           r"Word Pattern|Ransom|Majority|Group|Unique|Distinct|Pairs|Occurrence|"
                           r"Jewels|Disappeared|Set Mismatch|Common|Missing|Bulls|Difference of Two Arrays|"
                           r"Counting Elements|Lucky|Repeated|Most Common|Uncommon|Degree of an Array|"
                           r"Harmonious|Boomerangs|4Sum II|K-diff|Palindrome Permutation|Palindrome Pairs|"
                           r"Happy|Sentence Similarity|Intersection|Consistent|Balloons|Symmetric|"
                           r"Equal Row|Equivalent|Twice|Tuple|Winner|Losses|Destination City|Town Judge"),
        ("Strings", r"String|Substring|Word|Palindrom|Character|Letter|Sentence|Vowel|Text|Capital|"
                    r"Abbreviation|Email|IP |Version|Parenthes|Roman|Decode|Encode|Case|Alphabet|Keyboard|"
                    r"Typewriter|Concatenat|Lowercase|Bold|Tag|Comments|Password|Date|Caesar|Cipher|"
                    r"Prefix|Suffix|Camelcase|Balanced|Zigzag Conversion|Justification|Hexspeak|"
                    r"Reformat|Compress|Acronym|Spam|Digit"),
        ("Sorting & Ordering", r"Sort|Rank|Relative|Largest Number|Order|Maximum Gap|Height Checker|"
                               r"Permutation|Median|Third Maximum|Kth|Largest|Smallest|Minimum Absolute"),
        ("Subarrays & Sequences", r"Subarray|Consecutive|Increasing|Decreasing|Monotonic|Mountain|Turbulent|"
                                  r"Zigzag|Alternating|Arithmetic|Longest|Triplet|Sequence|Streak|"
                                  r"Non-decreasing|Special Array|Peaks|Hills"),
        ("Simulation", r"Robot|Simulation|Game|Candy Crush|Pour Water|Lemonade|Watering|Waiting|Cleaning|"
                       r"Collisions|Time|Ball|Ants|Chairs|Traffic|Push Dominoes|Moving Stones|Bank|Cooking"),
        ("Counting & Math", r"Count|Number of|Sum|Maximum|Minimum|Average|Difference|Pairs|Quadruplets|"
                            r"Divisible|Product|Poker|Calculate|Find the"),
    ],

    "Greedy": [
        ("Intervals & Scheduling", r"Interval|Meeting|Arrows|Overlapping|Schedul|Free Time|Video Stitching|"
                                   r"Taps|Car Pooling|Chain|Tasks|Time to|Ranges|Events|Non Intersect|"
                                   r"Earliest|Latest"),
        ("Strings & Subsequences", r"String|Substring|Subsequence|Palindrom|Lexicograph|Letters|Characters|"
                                   r"Parenthes|Digits?|Word|Anti-palindrome|Caption|Binary Number|Typing"),
        ("Jump & Reach", r"Jump|Gas Station|Candy|Buy and Sell|Reach|Hopping|Frog|Sideway|Coins|Buildings"),
        ("Operations & Swaps", r"^Minimum .*(Operations|Moves|Swaps|Changes|Flips|Deletions|Increments|"
                               r"Replacements|Cost)|^Make |^Maximum .*(Operations|OR|Subarrays)|Swaps|"
                               r"Flips|Increment"),
        ("Pairing & Sorting", r"Pair|Assign|Boats|Cookies|Cards|Advantage|Tokens|Seat|Rearrang|Minimize|"
                              r"Maximize|Maximum Number|Maximum Sum|Maximum Score|Group|Split|Partition|"
                              r"Distribute|Sets|Array"),
    ],

    "Math & Geometry": [
        ("Random & Simulation", r"Random|Rand|Pick|Simulation|Days?|Date|Clock|Chess|Game|Robot|Round|"
                                r"Pillow|Ball|Bulb|Escape|Circle|Water|Rabbits|Handshakes|Egg|Nim|Passing"),
        ("Matrix Operations", r"Matrix|Spiral|Rotate Image|Transpose|Grid|Chessboard|Board"),
        ("Geometry", r"Point|Line|Rectangle|Triangle|Circle|Area|Square|Polygon|Fence|Angle|Distance|"
                     r"Perimeter|Trapezoid|Boomerang|Overlap|Convex|Surface|Projection|Lattice|Darts|"
                     r"Segment|Kill|Visible|Cover|Manhattan"),
        ("Number Theory", r"Prime|GCD|Divisor|Factor|Pow|Modular|Perfect|Ugly|Happy|Multiple|Coprime|"
                          r"Divisible|Divide|Fraction|Division|Factorial|Harshad|Armstrong|Even|Odd"),
        ("Digits & Bases", r"Digit|Base|Integer|Number|Binary|Roman|Excel|Palindrom|Reverse|Add |Plus|"
                           r"Multiply|Hexa|Negabinary|Decimal|Sum of"),
        ("Counting & Combinatorics", r"Ways|Count|Arrays|Combination|Permutation|Subsequence|Sequence|"
                                     r"Probability|Distribute|Derangement|Anagrams"),
    ],

    "Trees": [
        ("Segment Tree & BIT", r"^$"),  # populated through PINNED
        ("Tries", r"Trie|Prefix|Dictionary|Autocomplete|Suggestions|Stream of Characters|Folders|"
                  r"Encoding of Words|Maximum XOR|Suffix|Replace Words|Map Sum|Word Search II|"
                  r"Longest Word|Design Add and Search|Substring|Index Pairs|Common Prefix|Search Words"),
        ("Binary Search Trees", r"Binary Search Tree|\bBST\b|Trim a Binary|Validate Binary Search"),
        ("Ancestors & Distance", r"Ancestor|Distance K|Distance in a Binary|Cousins|Nearest Right"),
        ("Traversal & Views", r"Traversal|Level|Order|View|Zigzag|Vertical|Boundary|Right Side|"
                              r"Leaf-Similar|Leaves|Print"),
        ("Construct & Serialize", r"Construct|Serialize|Deserialize|Build|Create Binary Tree|Convert|"
                                  r"Clone|Flatten|Merge|Recover|Inserter|Invert|Restore|Expression Tree"),
        ("N-ary & General Trees", r"N-ary|N-Ary|in a Tree|in Tree|of a Tree|Tree Node|Edge|Rooted|"
                                  r"Root Equals|Apples|Collect Coins"),
        ("Depth, Path & Sum", r"Depth|Path|Sum|Diameter|Height|Width|Tilt|Univalue|Longest|Subtree|"
                              r"Good Nodes|Leaf|Leaves|Same Tree|Symmetric|Balanced|Duplicate Subtrees|"
                              r"Pruning|Cameras|Coins|Maximum|Minimum"),
    ],

    "Graphs": [
        ("Topological Sort", r"Course|Alien|Sequence Reconstruction|Sort Items|Conditions|Recipes|"
                             r"Ancestors of a Node|Minimum Height Trees|Safe States|Parallel Courses"),
        ("Union Find", r"Connected Components|Provinces|Redundant Connection|Accounts Merge|Valid Tree|"
                       r"Similar String Groups|Smallest String With Swaps|Equations|Stones Removed|"
                       r"Earliest Moment|Largest Component|Graph Connectivity|Connecting Cities|"
                       r"Remove Max Number of Edges|Make Network Connected|Malware|Hamming|"
                       r"Friend Requests|Good Paths|Couples|Groups of Strings|Equivalent String|"
                       r"Complete Components|Unreachable Pairs|Lexicographically Smallest String"),
        ("Grid & Islands", r"Island|Grid|Matrix|Maze|Flood|Rotting|Oranges|Land|Regions|Enclaves|"
                           r"Minesweeper|Walls|Fish|Bricks|Slashes|Water Flow|Puzzle|Lock|Cells|Golf|"
                           r"Bridge|Fire|Box|Border|Exit|Food|Keys|Cross|Door|Chessboard"),
        ("Shortest Path", r"Shortest|Cheapest|Network Delay|Path With|Effort|Swim|Bus Routes|Word Ladder|"
                          r"Jump|Cost|Minimum Time|Distance|Minimum Moves|Delay|Safest|Probability|"
                          r"Weighted|Obstacle|Reach|Smallest Number of Neighbors|Frog|Flights|"
                          r"Ways to Arrive|Restricted Paths|Time"),
        ("Bipartite & Coloring", r"Bipartite|Bipartition|Coloring|Flower Planting|Invitations|Cat and Mouse"),
        ("Spanning Trees & Edges", r"Spanning|Critical|Edge|Water Distribution|Reorder Routes|Network Rank|"
                                   r"Degrees"),
        ("Trees & Rooted Graphs", r"Tree|Diameter|Root|Employee|Kill Process|Star|Center|Cycle|Champion"),
    ],

    "1-D Dynamic Programming": [
        ("Linear & Stairs", r"Climbing|Fibonacci|Tribonacci|House Robber|Stairs|Delete and Earn|Jump|"
                            r"Tickets|Maximum Subarray|Product Subarray|Sub-arrays|Alternating|Arithmetic Slices"),
        ("Knapsack & Coin Change", r"Coin|Knapsack|Partition Equal|Combination Sum|Perfect Squares|Target|"
                                   r"Subset|Profit|Reward|Job Scheduling|Earnings|Budget|Purchase|Coins|"
                                   r"Damage|Schedul"),
        ("Strings & Partitions", r"String|Palindrom|Decode|Word|Partition|Split|Text|Substring|Digit|"
                                 r"Sentence|Characters|Caption|Typed|Separate|Anagram"),
        ("Subsequences", r"Subsequence|Increasing|Chain|Divisible Subset|Subarray|Longest|Sequence|"
                         r"Non-decreasing|Stepping|Ideal"),
        ("Counting", r"Count|Number of|Ways|Permutation|Beautiful|Integers"),
    ],

    "2-D Dynamic Programming": [
        ("Stock & Games", r"Best Time|Stone Game|Predict|Can I Win|Guess Number|Game|Race|Win"),
        ("Interval DP", r"Burst|Remove Boxes|Merge Stones|Cut a Stick|Strange Printer|Palindrome Partitioning|"
                        r"Palindrome Removal|Cutting|Scramble|Balloon"),
        ("Grid Paths", r"Path|Grid|Matrix|Falling|Triangle|Cherry|Dungeon|Chessboard|Knight|Square|"
                       r"Rectangles|Submatrices|Pizza|Moves|Land|Pyramids|Line|Board"),
        ("Strings (LCS & Edit)", r"Subsequence|Palindrom|String|Edit|Common|Interleaving|Regular|Wildcard|"
                                 r"Word|Lines|Distinct|Delete Operation|Stickers|Supersequence|Subarray|Convert"),
        ("Knapsack & Counting", r"Ways|Knapsack|Coin|Target Sum|Ones and Zeroes|Number of|Count|Dice|"
                                r"Paint|Partition|Jump|Sum|Permutations|Inverse|Score"),
    ],

    "Binary Search": [
        ("Rotated & Peak", r"Rotated|Peak|Mountain|Pivot|Fixed Point|Single Element"),
        ("Search on Answer", r"Minimum|Maximum|Minimize|Maximize|Capacity|Koko|Speed|Split Array|Divisor|"
                             r"Magnetic|Days|Time|Kth|K-th|Ugly|Magical|Divide|Cutting|Heaters|Ribbons|"
                             r"Allocated|Trips|Repair|Tastiness|Font|Sqrt|Perfect Square|Earliest|Latest"),
    ],

    "Database / SQL": [
        ("Pandas", r"DataFrame|Reshape|Select Data|Change Data|Fill Missing|Display the First|Size of a"),
        ("Ranking & Windows", r"Rank|Highest|Nth|Second|Top|Median|Cumulative|Consecutive|Streak|Rolling|"
                              r"Growth|Most Recent|Latest|Last Person|Third|Largest|Running"),
        ("Analytics & Aggregation", r"Sales|Analysis|Transactions|Percentage|Average|Count|Number of|"
                                    r"Activity|Rate|Monthly|Article|Game Play|Users|Products|Revenue|"
                                    r"Total|Queries|Customers|Ads|Performance"),
    ],
}

# Catch-all bucket per topic (shown last). Topics not listed here fall back to "Other".
FALLBACK: dict[str, str] = {
    "Arrays & Hashing": "Arrays (General)",
    "Greedy": "Greedy (General)",
    "Math & Geometry": "Math (General)",
    "Trees": "Binary Trees (General)",
    "Graphs": "General Graphs",
    "1-D Dynamic Programming": "Optimization (General)",
    "2-D Dynamic Programming": "2-D DP (General)",
    "Binary Search": "Sorted Array Search",
    "Database / SQL": "Joins & Filters",
}

# ─────────────────────────────────────────────
# Compile once at import time
# ─────────────────────────────────────────────
_COMPILED = {
    topic: [(name, re.compile(pattern, re.I)) for name, pattern in rules]
    for topic, rules in RULES.items()
}


def classify(topic: str, problem: dict) -> str | None:
    """Return the sub-topic for a problem, or None if this topic isn't split."""
    if topic not in _COMPILED:
        return None
    pinned = PINNED.get(problem["id"])
    if pinned:
        return pinned
    title = problem["title"]
    for name, rx in _COMPILED[topic]:
        if rx.search(title):
            return name
    return FALLBACK.get(topic, "Other")


def sub_order(topic: str) -> list[str]:
    """Display order of a topic's sub-topics (rules first, catch-all last)."""
    if topic not in RULES:
        return []
    return [name for name, _ in RULES[topic]] + [FALLBACK.get(topic, "Other")]
