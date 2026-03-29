import os
import json
from agents import get_crew

TEST_QUERIES = [
    # 10 Prerequisite Checks
    "Can I take CSCI 104L if I've taken CSCI 103L with a B?",
    "Can I take CSCI 201L if I've taken CSCI 104L with a C-?",
    "Can I take CSCI 270 if I've taken CSCI 104L and CSCI 170 both with a B?",
    "Do I meet the prerequisites for Software Engineering (CSCI 310)?",
    "Can I enroll in CSCI 103L without taking CSCI 102L?",
    "I took CSCI 102L, 103L, and 104L with Bs. Am I eligible for CSCI 356?",
    "Can I take Computer Graphics (CSCI 420) if I have taken CSCI 104L but not Linear Algebra?",
    "Is co-requisite for CSCI 103L required concurrently or can it be completed earlier?",
    "I have CSCI 104L (B) and MATH 125 (A). Can I take CSCI 170?",
    "What do I need before enrolling in Database Systems (assuming CSCI 4XX_1)?",
    
    # 5 Prerequisite Chain Questions
    "I've only taken CSCI 102L. What is the full chain of courses I need to take before I can enroll in Operating Systems (CSCI 350)?",
    "What are all the prereqs (including their own prereqs) for CSCI 201L?",
    "I want to take CSCI 353 (Internetworking), but I've only finished CSCI 104L. What intermediate courses am I missing?",
    "List the path from CSCI 102L to CSCI 401 (Capstone).",
    "What math courses must I complete before I can take CSCI 270 (Algorithms)?",

    # 5 Program Requirement Questions
    "How many units are required to graduate with a BS in Computer Science at USC?",
    "What are the minimum grade requirements for core CSCI courses?",
    "Can I take 20 units in my first semester?",
    "What is the policy for repeating a course if I get a D?",
    "Do I need to take writing courses for a CSCI degree? If so, which ones?",

    # 5 "Not in Docs" / Trick Questions
    "Is CSCI 201L offered in the Fall 2024 semester?",
    "Who is the professor teaching CSCI 104L this term?",
    "What is the average GPA of students in the Computer Science program?",
    "Can I get instructor consent to skip the prereq for CSCI 270?",
    "Where is the CS department office located on campus?"
]

def run_evaluation():
    results = []
    print(f"Starting evaluation of {len(TEST_QUERIES)} queries...")
    for i, query in enumerate(TEST_QUERIES):
        print(f"\n[{i+1}/25] Query: {query}")
        try:
            crew = get_crew(query)
            result = crew.kickoff()
            results.append({
                "query": query,
                "response": str(result)
            })
        except Exception as e:
            print(f"Error in query {i+1}: {e}")
            results.append({
                "query": query,
                "error": str(e)
            })
    
    with open("eval_results.json", "w", encoding='utf-8') as f:
        json.dump(results, f, indent=4)
        
    print("\nEvaluation complete. Results saved to eval_results.json")

if __name__ == "__main__":
    run_evaluation()
