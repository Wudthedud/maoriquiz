class ScoreLives:
    """Score system for infinite questions with 3 lives (hearts)."""
    def __init__(self, max_lives=3):
        """Initializes the score and lives."""
        self.score = 0
        self.max_lives = max_lives
        self.lives = max_lives

    def increment_score(self):
        """Increments the score by 1."""
        self.score += 1

    def lose_life(self):
        """Decrements lives by 1 if possible."""
        if self.lives > 0:
            self.lives -= 1

    def is_alive(self):
        """Returns True if the player still has lives left."""
        return self.lives > 0

    def get_score(self):
        """Returns the current score."""
        return self.score

    def get_lives(self):
        """Returns the current number of lives."""
        return self.lives

    def reset(self):
        """Resets the score and lives to initial values."""
        self.score = 0
        self.lives = self.max_lives

    def get_hearts(self):
        """Returns a list of heart image filenames representing current lives."""
        hearts = []
        for i in range(self.max_lives):
            if i < self.lives:
                hearts.append("heart.png")
            else:
                hearts.append("empty_heart.png")
        return hearts
