from src.agent import RAGAgent
import pandas as pd
import os
from tqdm import tqdm
import argparse

def str2bool(v):
    if isinstance(v, bool):
        return v
    v = str(v).strip().lower()
    if v in ("yes", "true", "t", "y", "1"):
        return True
    elif v in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected (True/False).")

parser = argparse.ArgumentParser(description="Run EMIR abbreviation experiment")
parser.add_argument(
    "--question_path",
    type=str,
    required=True,
    help="Path to the CSV file containing questions or abbreviations"
)

parser.add_argument(
    "--output_path",
    type=str,
    required=True,
    help="Path to save the output CSV file"
)

parser.add_argument(
    "--model_core",
    type=str,
    default="meta-llama/Meta-Llama-3-8B-Instruct",
    help="Model core name or identifier"
)
parser.add_argument(
    "--whether_rag",
    type=str2bool,
    default=True,
    help="Whether to use RAG (True or False)"
)

args = parser.parse_args()

def main():
    
    agent = RAGAgent(model_name=args.model_core)
    if (os.path.exists(args.output_path)):
        question_path = args.output_path
    else:
        question_path = args.question_path
    df = pd.read_csv(question_path)
    answers = []
    for _, row in tqdm(df.iterrows(),desc="Processing", total=len(df)):
        if _ == len(df) - 1:
            continue  
        question = str(row.iloc[0])
        
        if question.strip() == "":
            answers.append("None")
            continue
        if args.whether_rag:
            
            answer = agent.answer_with_knowledge("What is " + question + "?")
            
        else:
            answer = agent.direct_answer("What is " + question + "?")
            
        print(f"Question: {question}\n Answer: {answer}")
        answers.append(answer)
    
    answers.append("")
    col_name = f"{args.model_core}_{args.whether_rag}"
    df[col_name] = answers
    df.to_csv(args.output_path, index=False)
    print(f"Saved answered file to {args.output_path}")
    
def evaluate():
    from src.judge import Judge
    judge = Judge()
    df = pd.read_csv(args.output_path)
    correct_count = 0
    total_count = len(df)
    correct_list = []
    for _, row in tqdm(df.iterrows(),desc="Processing", total=len(df)):
        if _ == len(df) - 1:
            continue  
        col_name = f"{args.model_core}_{args.whether_rag}"
        answer = str(row.get(col_name, "")).strip()
        
        groundTrue = str(row.get("answers", "")).strip()
        
        question = "What is " + str(row.get("abbreviations", "")).strip()+ "?"
        
        response = judge.forward(f"Question: {question}\n GroundTrue: {groundTrue}\n Answer: {answer}")
        
        if "incorrect" in response.lower():
            correct_list.append("False")
            
        else:
            correct_list.append("True")
            correct_count += 1
        print(f"Question: {question}\nAnswer: {answer}\nJudge Response: {response}\n")
        
    accuracy = correct_count / total_count
    
    # df["Judge Correct1"] = correct_list
    correct_list.append(accuracy)
    df[f"{args.model_core}_{args.whether_rag}_Judge Correct"] = correct_list
    df.to_csv(args.output_path, index=False)
    print(f"Accuracy: {accuracy:.2f}")
    
if __name__ == "__main__":
    main()
    evaluate()
    
    