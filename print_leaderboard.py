from score_v3 import HighScore

def print_leaderboard():
    highscore_manager = HighScore()
    leaderboard = highscore_manager.get_leaderboard()
    print("Leaderboard (Top 10):")
    print(f"{'#':<3}{'Name':<13}{'Score':<7}{'Difficulty':<10}")
    for idx, (score, name, difficulty) in enumerate(leaderboard, 1):
        print(f"{idx:<3}{name[:12]:<13}{score:<7}{difficulty:<10}")

if __name__ == "__main__":
    print_leaderboard()
