import aihelper
import pandas as pd
import argparse


def main():
    parser = argparse.ArgumentParser(description='Send a string to Ollama and get a response.')
    parser.add_argument('prompt', type=str, help='The prompt to send to Ollama.')
    args = parser.parse_args()
    
    df = pd.read_csv('rnr.csv')
    records = df.to_dict('records')

    response = aihelper.completeChat(args.prompt, "llama3",records)
    print(response)

if __name__ == '__main__':
    main()