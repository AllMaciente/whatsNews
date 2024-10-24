from watchgod import run_process

from whatsnews.main import main

if __name__ == "__main__":
    run_process(path="whatsnews", target=main)
