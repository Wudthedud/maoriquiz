from score_v2 import HighScore

def main():
    hs = HighScore("highscore.txt")
    print(f"Current high score: {hs.get_highscore()} by {hs.get_highscore_name()}")
    try:
        score = int(input("Enter your score: "))
    except ValueError:
        print("Invalid score. Please enter a number.")
        return
    name = input("Enter your name (max 12 chars): ").strip()
    if not name:
        print("Name cannot be empty.")
        return
    if len(name) > 12:
        print("Name must be 12 characters or less.")
        return
    hs.update_highscore(score, name)
    print(f"Updated high score: {hs.get_highscore()} by {hs.get_highscore_name()}")

if __name__ == "__main__":
    main()
