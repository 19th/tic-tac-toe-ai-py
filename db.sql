-- Main game data
CREATE TABLE IF NOT EXISTS game (
    game_id INT AUTO_INCREMENT PRIMARY KEY,  -- Unique identifier for each game
    player_x VARCHAR(255) NOT NULL,          -- Player X (empty, username or 'AI' for AI player)
    player_o VARCHAR(255) NOT NULL,          -- Player O (empty, username or 'AI' for AI player)
    winner VARCHAR(10) DEFAULT NULL,         -- Stores winner name ('X', 'O', 'Draw', or NULL if ongoing)
    is_finished BOOLEAN                      -- Game status (ongoing or finished)
);

-- Game scores
CREATE TABLE IF NOT EXISTS game_score (
    score_id INT AUTO_INCREMENT PRIMARY KEY,  -- Unique identifier for each score
    game_id INT,                              -- Foreign key to the game table
    player VARCHAR(255) NOT NULL,             -- Player whose score is recorded (e.g., 'X', 'O', or 'AI')
    score INT NOT NULL,                       -- Score value (0 or more)
    FOREIGN KEY (game_id) REFERENCES game(game_id) ON DELETE CASCADE
);

-- Game steps
CREATE TABLE IF NOT EXISTS game_step (
    step_id INT AUTO_INCREMENT PRIMARY KEY,   -- Unique identifier for each step
    game_id INT,                              -- Foreign key to the game table
    player VARCHAR(255) NOT NULL,             -- Player who made the move ('X', 'O', or 'AI')
    step_number INT NOT NULL,                 -- The step number in sequence
    position INT NOT NULL CHECK (position BETWEEN 1 AND 9),  -- Board position (1 to 9 for 3x3 grid)
    FOREIGN KEY (game_id) REFERENCES game(game_id) ON DELETE CASCADE
);