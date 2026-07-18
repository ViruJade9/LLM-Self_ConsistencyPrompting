SUMMARY_PROMPT = """
    These are 10 different answers for the same question.

    Summarise the most consistent and accurate final answer (8-10 SENTANCE MAX) 

    Return ONLY valid JSON
    
    {
        "final_answer": "summarised answer here"
    }
"""