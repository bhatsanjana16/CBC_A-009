from main import run_assistant

if __name__ == "__main__":
    try:
        run_assistant()
    except KeyboardInterrupt:
        print("\nUser interrupted. Exiting...")
