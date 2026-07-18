from models.generator import generate_answer
from models.summarizer import summarizer_answers

def main():
    user_query = input(
        "Hello user 😊 \n\nEnter your query >>>"
    )

    if user_query.lower() in ["exit", "stop"]:
        print("Exiting...")
        return

    answers = generate_answer(user_query)
    final_answer = summarizer_answers(answers)

    print("\n" + "#"  * 60)
    print(final_answer)
    print("#"  * 60)

if __name__ == "__main__":
        main()