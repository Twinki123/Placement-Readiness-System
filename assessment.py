from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Sequence


QUESTIONS_PER_ASSESSMENT = 8


@dataclass(frozen=True)
class Question:
    prompt: str
    options: tuple[str, ...]
    answer_index: int
    topic: str
    explanation: str


QUIZZES = {
    "DSA": (
        Question(
            "Which data structure gives average O(1) lookup by key?",
            ("A queue", "A hash table", "A binary heap", "A linked list"),
            1,
            "Hashing",
            "A hash table maps a key to a bucket, giving average constant-time lookup when collisions are controlled.",
        ),
        Question(
            "Binary search can be applied directly when the data is:",
            ("Stored in a linked list", "Sorted", "All unique", "Stored in a tree"),
            1,
            "Searching",
            "Binary search repeatedly halves the search interval, which depends on sorted order.",
        ),
        Question(
            "What is the worst-case time complexity of merge sort?",
            ("O(n)", "O(n log n)", "O(log n)", "O(n squared)"),
            1,
            "Sorting",
            "Merge sort splits the input into logarithmically many levels and merges n elements per level.",
        ),
        Question(
            "Which data structure is most suitable for checking balanced parentheses?",
            ("Stack", "Queue", "Min-heap", "Graph"),
            0,
            "Stacks and queues",
            "A stack matches each closing bracket with the most recently opened bracket.",
        ),
        Question(
            "Breadth-first search finds shortest paths in an unweighted graph because it:",
            (
                "Visits vertices level by level",
                "Always chooses the smallest vertex",
                "Uses recursion only",
                "Sorts the adjacency list first",
            ),
            0,
            "Graphs",
            "BFS explores all vertices at distance k before vertices at distance k + 1.",
        ),
        Question(
            "In a singly linked list, inserting a node at the head takes:",
            ("O(1)", "O(log n)", "O(n)", "O(n log n)"),
            0,
            "Linked lists",
            "The new node only needs to point to the current head, then become the head.",
        ),
        Question(
            "What is essential to prevent infinite recursion?",
            ("A sorted input", "A base case", "A global variable", "A loop inside every call"),
            1,
            "Recursion",
            "A base case stops recursive calls once the problem has been reduced far enough.",
        ),
        Question(
            "Which traversal visits a binary search tree's values in sorted order?",
            ("Preorder", "Inorder", "Postorder", "Level order"),
            1,
            "Trees",
            "Inorder traversal visits the left subtree, node, then right subtree.",
        ),
        Question(
            "What is the time complexity of accessing an array element by index?",
            ("O(1)", "O(log n)", "O(n)", "O(n log n)"),
            0,
            "Arrays",
            "An array computes an element's address directly from its index.",
        ),
        Question(
            "A queue follows which processing order?",
            ("Last in, first out", "First in, first out", "Highest priority first", "Sorted order"),
            1,
            "Stacks and queues",
            "A queue removes the element that has been waiting the longest.",
        ),
        Question(
            "What is the search time in a balanced binary search tree?",
            ("O(1)", "O(log n)", "O(n)", "O(n squared)"),
            1,
            "Trees",
            "A balanced tree has logarithmic height, so each comparison removes about half the remaining levels.",
        ),
        Question(
            "Floyd's cycle-detection algorithm uses:",
            ("A queue and a stack", "Two pointers moving at different speeds", "A sorted copy", "A hash table of edges"),
            1,
            "Linked lists",
            "A fast pointer eventually meets a slow pointer if a linked list contains a cycle.",
        ),
        Question(
            "Removing the minimum element from a binary min-heap takes:",
            ("O(1)", "O(log n)", "O(n)", "O(n log n)"),
            1,
            "Heaps",
            "After removing the root, restoring the heap property takes time proportional to the heap height.",
        ),
        Question(
            "What is insertion sort's best-case time on an already sorted array?",
            ("O(1)", "O(log n)", "O(n)", "O(n squared)"),
            2,
            "Sorting",
            "Each element needs only one comparison when the input is already sorted.",
        ),
        Question(
            "Memoization improves a recursive algorithm by:",
            ("Sorting every input first", "Saving results of solved subproblems", "Removing the base case", "Using a wider call stack"),
            1,
            "Dynamic programming",
            "Memoization caches subproblem results so the same work does not need to be repeated.",
        ),
        Question(
            "In a sorted array, which approach can find a pair with a target sum in O(n)?",
            ("Try every pair", "Use two pointers from opposite ends", "Run binary search for every value", "Sort the array again"),
            1,
            "Searching",
            "Moving the left or right pointer based on the sum checks each position at most once.",
        ),
        Question(
            "An adjacency list for a graph with V vertices and E edges uses how much space?",
            ("O(V)", "O(E)", "O(V + E)", "O(V squared + E)"),
            2,
            "Graphs",
            "The list stores one entry per vertex plus entries representing the edges.",
        ),
        Question(
            "A topological ordering exists for which kind of graph?",
            ("Any undirected graph", "A directed acyclic graph", "A complete graph only", "A graph with a cycle"),
            1,
            "Graphs",
            "A topological ordering respects edge direction and is defined for directed acyclic graphs.",
        ),
        Question(
            "Which pair of properties is commonly used in dynamic programming?",
            ("Sorted input and unique values", "Overlapping subproblems and optimal substructure", "Cycles and negative weights", "Constant memory and recursion"),
            1,
            "Dynamic programming",
            "Dynamic programming is useful when subproblems repeat and their solutions compose into an optimal larger solution.",
        ),
        Question(
            "If a recursive function makes one call per level to depth d, its call-stack space is:",
            ("O(1)", "O(log d)", "O(d)", "O(d squared)"),
            2,
            "Recursion",
            "Each active recursive call occupies a stack frame, so d active levels use O(d) space.",
        ),
    ),
    "Aptitude": (
        Question(
            "What is 25% of 240?",
            ("48", "54", "60", "72"),
            2,
            "Percentages",
            "A quarter of 240 is 240 divided by 4, which is 60.",
        ),
        Question(
            "The ratio of two quantities is 3:5 and their total is 64. What is the larger quantity?",
            ("24", "36", "40", "48"),
            2,
            "Ratios",
            "There are 8 total parts, so each part is 64 divided by 8. The larger quantity is 5 times 8.",
        ),
        Question(
            "A can finish a task in 12 days and B in 6 days. Working together, how long will they take?",
            ("3 days", "4 days", "6 days", "9 days"),
            1,
            "Time and work",
            "Their daily rates add to 1/12 + 1/6 = 1/4 of the task per day.",
        ),
        Question(
            "A vehicle travels 150 km in 3 hours. What is its average speed?",
            ("40 km/h", "45 km/h", "50 km/h", "60 km/h"),
            2,
            "Speed and distance",
            "Average speed is distance divided by time: 150 divided by 3 equals 50 km/h.",
        ),
        Question(
            "The average of four numbers is 15. If 25 is added as a fifth number, what is the new average?",
            ("16", "17", "18", "20"),
            1,
            "Averages",
            "The first four total 60; adding 25 gives 85, and 85 divided by 5 is 17.",
        ),
        Question(
            "What number comes next: 2, 6, 12, 20, 30, ...?",
            ("36", "40", "42", "44"),
            2,
            "Number series",
            "The differences are 4, 6, 8, and 10; the next difference is 12, giving 42.",
        ),
        Question(
            "An item priced at 1,500 has a 20% discount. What is the sale price?",
            ("1,050", "1,150", "1,200", "1,250"),
            2,
            "Profit and discount",
            "The discount is 300, so the sale price is 1,500 minus 300 = 1,200.",
        ),
        Question(
            "All analysts at a firm use spreadsheets. Mira is an analyst there. What follows?",
            (
                "Mira manages the firm",
                "Mira uses spreadsheets",
                "Everyone using spreadsheets is an analyst",
                "No conclusion can be drawn",
            ),
            1,
            "Logical reasoning",
            "The statement says every analyst uses spreadsheets, so it applies to Mira.",
        ),
        Question(
            "Solve: 3x + 5 = 26.",
            ("5", "6", "7", "8"),
            2,
            "Algebra",
            "Subtract 5 to get 3x = 21, then divide by 3 to get x = 7.",
        ),
        Question(
            "A fair coin is tossed once. What is the probability of getting heads?",
            ("0", "1/4", "1/2", "1"),
            2,
            "Probability",
            "There is one favorable outcome among two equally likely outcomes.",
        ),
        Question(
            "A 1,000 item receives successive discounts of 10% and 20%. What is the final price?",
            ("700", "720", "750", "800"),
            1,
            "Percentages",
            "After 10% off the price is 900; taking 20% off 900 gives 720.",
        ),
        Question(
            "A 120 m train passes a pole in 6 seconds. What is its speed?",
            ("60 km/h", "72 km/h", "80 km/h", "90 km/h"),
            1,
            "Speed and distance",
            "The speed is 120/6 = 20 m/s; multiplying by 3.6 gives 72 km/h.",
        ),
        Question(
            "A value of 200 increases by 15%. What is the new value?",
            ("215", "225", "230", "240"),
            2,
            "Percentages",
            "Fifteen percent of 200 is 30, so the new value is 230.",
        ),
        Question(
            "How many distinct arrangements can be made from 5 different books on a shelf?",
            ("25", "60", "100", "120"),
            3,
            "Permutations",
            "The books can be arranged in 5! = 5 x 4 x 3 x 2 x 1 = 120 ways.",
        ),
        Question(
            "What is the smaller angle between clock hands at 3:00?",
            ("60 degrees", "90 degrees", "120 degrees", "180 degrees"),
            1,
            "Logical reasoning",
            "At 3:00 the minute hand is at 12 and the hour hand is at 3, a quarter turn apart.",
        ),
        Question(
            "What comes next in the sequence 3, 9, 27, 81, ...?",
            ("162", "216", "243", "324"),
            2,
            "Number series",
            "Each term is multiplied by 3, so 81 x 3 = 243.",
        ),
        Question(
            "If 5 machines make 5 parts in 5 minutes, how long do 100 machines take to make 100 parts?",
            ("5 minutes", "20 minutes", "100 minutes", "500 minutes"),
            0,
            "Time and work",
            "Each machine makes one part in 5 minutes, so 100 machines make 100 parts in 5 minutes.",
        ),
        Question(
            "A bag has 3 red and 2 blue balls. What is the probability of drawing a blue ball?",
            ("1/5", "2/5", "1/2", "3/5"),
            1,
            "Probability",
            "Two of the five equally likely balls are blue.",
        ),
        Question(
            "A person's salary rises from 40,000 to 46,000. What is the percentage increase?",
            ("10%", "12%", "15%", "20%"),
            2,
            "Percentages",
            "The increase is 6,000; 6,000 divided by 40,000 is 15%.",
        ),
        Question(
            "If 4 workers complete a job in 9 days, how many days would 6 workers take at the same rate?",
            ("4 days", "6 days", "9 days", "13.5 days"),
            1,
            "Time and work",
            "The work is 4 x 9 = 36 worker-days; 36 divided by 6 is 6 days.",
        ),
    ),
}


def create_attempt(
    subject: str,
    excluded_question_indices: Iterable[int] = (),
) -> list[dict[str, Any]]:
    if subject not in QUIZZES:
        raise ValueError(f"Unknown assessment subject: {subject}")

    question_bank = QUIZZES[subject]
    excluded = set(excluded_question_indices)
    available = [
        index for index in range(len(question_bank)) if index not in excluded
    ]
    if len(available) < QUESTIONS_PER_ASSESSMENT:
        available = list(range(len(question_bank)))
    if len(available) < QUESTIONS_PER_ASSESSMENT:
        raise ValueError(f"{subject} needs at least {QUESTIONS_PER_ASSESSMENT} questions")

    selected_indices = random.sample(available, k=QUESTIONS_PER_ASSESSMENT)
    return [
        {
            "question_index": question_index,
            "option_order": random.sample(
                range(len(question_bank[question_index].options)),
                k=len(question_bank[question_index].options),
            ),
        }
        for question_index in selected_indices
    ]


def score_assessment(
    subject: str,
    answers: Mapping[int, int],
    question_indices: Sequence[int] | None = None,
) -> dict[str, Any]:
    if subject not in QUIZZES:
        raise ValueError(f"Unknown assessment subject: {subject}")

    question_bank = QUIZZES[subject]
    selected_indices = (
        tuple(range(len(question_bank)))
        if question_indices is None
        else tuple(question_indices)
    )
    if not selected_indices or any(
        index < 0 or index >= len(question_bank) for index in selected_indices
    ):
        raise ValueError("Question indices must refer to questions in the selected subject")
    if len(set(selected_indices)) != len(selected_indices):
        raise ValueError("An assessment cannot contain duplicate questions")
    questions = tuple(question_bank[index] for index in selected_indices)
    topic_scores: dict[str, dict[str, int]] = {}
    review = []
    correct_count = 0

    for question_number, question in enumerate(questions):
        topic = topic_scores.setdefault(question.topic, {"correct": 0, "total": 0})
        topic["total"] += 1
        selected_index = answers.get(question_number)
        is_correct = selected_index == question.answer_index
        if is_correct:
            correct_count += 1
            topic["correct"] += 1
        review.append(
            {
                "question": question.prompt,
                "selected": question.options[selected_index]
                if selected_index is not None and 0 <= selected_index < len(question.options)
                else "Not answered",
                "answer": question.options[question.answer_index],
                "is_correct": is_correct,
                "explanation": question.explanation,
            }
        )

    for topic in topic_scores.values():
        topic["percent"] = round(topic["correct"] / topic["total"] * 100)

    return {
        "subject": subject,
        "correct": correct_count,
        "total": len(questions),
        "score": round(correct_count / len(questions) * 100),
        "topic_scores": topic_scores,
        "review": review,
    }


def build_30_day_plan(
    assessments: Mapping[str, Mapping[str, Any]],
) -> list[dict[str, Any]]:
    subjects = ("DSA", "Aptitude")
    topic_order: dict[str, list[str]] = {}
    subject_scores: dict[str, int] = {}

    for subject in subjects:
        result = assessments.get(subject)
        if result:
            subject_scores[subject] = int(result["score"])
            topic_scores = result["topic_scores"]
            topic_order[subject] = [
                topic
                for topic, _ in sorted(
                    topic_scores.items(), key=lambda item: item[1]["percent"]
                )
            ]
        else:
            subject_scores[subject] = 50
            topic_order[subject] = [question.topic for question in QUIZZES[subject]]
            topic_order[subject] = list(dict.fromkeys(topic_order[subject]))

    weights = {subject: max(10, 100 - subject_scores[subject]) for subject in subjects}
    total_weight = sum(weights.values())
    assigned = {subject: 0 for subject in subjects}
    topic_counts = {subject: 0 for subject in subjects}
    plan = []

    for day in range(1, 31):
        if day <= 7:
            phase, duration = "Build foundations", 25
        elif day <= 14:
            phase, duration = "Guided practice", 35
        elif day <= 21:
            phase, duration = "Timed problem sets", 40
        elif day <= 27:
            phase, duration = "Mixed revision", 45
        elif day == 28:
            phase, duration = "Full-length mock", 60
        elif day == 29:
            phase, duration = "Error analysis", 35
        else:
            phase, duration = "Final simulation", 60

        if day >= 28:
            plan.append(
                {
                    "day": day,
                    "phase": phase,
                    "subject": "DSA + Aptitude",
                    "focus": "Timed placement assessment",
                    "task": {
                        28: "Complete a timed mixed assessment. Mark every guess and question you could not finish.",
                        29: "Rework missed questions without notes and update your personal pattern and formula sheet.",
                        30: "Repeat a final timed set, compare it with your first assessment, and set next-month targets.",
                    }[day],
                    "minutes": duration,
                }
            )
            continue

        subject = max(
            subjects,
            key=lambda item: (day * weights[item] / total_weight) - assigned[item],
        )
        assigned[subject] += 1
        topics = topic_order[subject]
        focus = topics[topic_counts[subject] % len(topics)]
        topic_counts[subject] += 1
        task = {
            "Build foundations": f"Review the core ideas in {focus}; write a short summary and solve 3 introductory questions.",
            "Guided practice": f"Work through 5 {focus} questions. Explain the approach before checking each solution.",
            "Timed problem sets": f"Complete a 20-minute timed set on {focus}; record accuracy and any repeated mistakes.",
            "Mixed revision": f"Mix {focus} with a previously studied topic; solve 6 questions and explain your choices aloud.",
        }[phase]
        plan.append(
            {
                "day": day,
                "phase": phase,
                "subject": subject,
                "focus": focus,
                "task": task,
                "minutes": duration,
            }
        )

    return plan
