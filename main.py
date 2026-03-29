import os
from agents import get_crew

def main():
    print("="*50)
    print("Welcome to the LOCAL Prerequisite & Course Planning Assistant!")
    print("Grounded in USC Computer Science 2024-2025 Catalog.")
    print("Using Local Model: model.gguf")
    print("="*50)
    
    while True:
        query = input("\n[Student] How can I help you? (type 'exit' to quit): ")
        if query.lower() in ['exit', 'quit']:
            break
            
        print("\n[Assistant] Thinking (this may take a moment on local hardware)...\n")
        try:
            crew = get_crew(query)
            result = crew.kickoff()
            
            print("\n" + "="*50)
            print(result)
            print("="*50)
        except Exception as e:
            print(f"\n[Error] Something went wrong: {e}")
            
if __name__ == "__main__":
    if not os.path.exists("model.gguf"):
        print("Error: model.gguf not found in the project root.")
    else:
        main()
