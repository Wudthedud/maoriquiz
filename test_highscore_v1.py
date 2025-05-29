from score_v2 import HighScore

def main():
    hs = HighScore("highscore.txt")
    print("Current leaderboard:")
    leaderboard = hs.get_leaderboard()
    print(f"{'#':<3}{'Name':<13}{'Score':<7}{'Difficulty':<10}")
    for idx, (score, name, difficulty) in enumerate(leaderboard, 1):
        print(f"{idx:<3}{name[:12]:<13}{score:<7}{difficulty:<10}")
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
    difficulty = input("Enter difficulty (easy/hard): ").strip().lower()
    if difficulty not in ("easy", "hard"):
        print("Difficulty must be 'easy' or 'hard'.")
        return
    hs.update_highscore(score, name, difficulty)
    print("Updated leaderboard:")
    leaderboard = hs.get_leaderboard()
    print(f"{'#':<3}{'Name':<13}{'Score':<7}{'Difficulty':<10}")
    for idx, (score, name, difficulty) in enumerate(leaderboard, 1):
        print(f"{idx:<3}{name[:12]:<13}{score:<7}{difficulty:<10}")

if __name__ == "__main__":
    main()
