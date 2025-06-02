graph TD
    A[Start Application: FINAL_main.py] --> B{Initialize GUI Class};

    subgraph GUI_Initialization [GUI Initialization]
        direction LR
        B --> B1[Set Appearance Mode & Theme];
        B1 --> B2[Create Root Window];
        B2 --> B3{Files Exist?};
        B3 -- Missing --> B4[Show Missing Files Error];
        B4 -- OK --> B5[Exit App];
        B3 -- Present --> B6[Set Window Icon];
        B6 --> B7[Init HighScore Manager];
        B7 --> B8[Init Questions Engine];
        B8 --> B9["Init Score Manager (initial)"];
        B9 --> B10[Create & Display Start Screen];
    end

    B10 --> SS_DISPLAY_NODE

    SS_DISPLAY_NODE[Start Screen Displayed] --> Start_Screen_Subgraph;

    subgraph Start_Screen_Subgraph [Start Screen Interaction]
        direction LR
        SS_WELCOME[Welcome, Leaderboard, Difficulty, Start Button] --> SS_CLICK_START{User Clicks Start?};
        SS_CLICK_START -- Yes --> SS_GET_DIFF[Get Selected Difficulty];
        SS_GET_DIFF --> TRIGGER_GAME_SCREEN[Call GUI.show_game_screen];
    end

    TRIGGER_GAME_SCREEN --> GS_INIT1[Destroy Start Screen Frame];
    GS_INIT1 --> GS_INIT2["Reset/Init ScoreManager for New Game"];
    GS_INIT2 --> GS_INIT3["Reset/Init QuestionsEngine (load/shuffle)"];
    GS_INIT3 --> GS_INIT4["Shuffle Questions List"];
    GS_INIT4 --> Q_SHOW_FIRST["Call GUI.show_question (correct_last=null)"];

    Q_SHOW_FIRST --> Q_CHECK_LAST_ANSWER{Correct Last Answer?};

    subgraph Game_Question_Cycle [Game Question Cycle]
        direction TB
        Q_CHECK_LAST_ANSWER -- Yes --> Q_EVAL_CORRECT{correct_last == True?};
        Q_EVAL_CORRECT -- True --> Q_INC_SCORE[Increment Score];
        Q_EVAL_CORRECT -- False --> Q_LOSE_LIFE[Lose Life];
        Q_INC_SCORE --> Q_CHECK_ALIVE;
        Q_LOSE_LIFE --> Q_CHECK_ALIVE;
        Q_CHECK_LAST_ANSWER -- No (First Question) --> Q_CHECK_ALIVE;

        Q_CHECK_ALIVE --> Q_IS_ALIVE{Player Still Alive?};
        Q_IS_ALIVE -- No --> TRIGGER_FINAL_SCORE[Call GUI.show_final_score];
        Q_IS_ALIVE -- Yes --> Q_QUESTIONS_LEFT{Questions in Current List?};
        Q_QUESTIONS_LEFT -- No --> Q_RELOAD_QUESTIONS[Reload & Shuffle All Questions];
        Q_RELOAD_QUESTIONS --> Q_STILL_NO_QUESTIONS{Still No Questions?};
        Q_STILL_NO_QUESTIONS -- Yes (e.g. empty file) --> TRIGGER_FINAL_SCORE;
        Q_STILL_NO_QUESTIONS -- No --> Q_GET_NEXT;
        Q_QUESTIONS_LEFT -- Yes --> Q_GET_NEXT;

        Q_GET_NEXT[Pop Next Question Data];
        Q_GET_NEXT --> Q_PREP_HEARTS[Prepare Heart Images];
        Q_PREP_HEARTS --> Q_DISPLAY_GAME_GUI[Create & Display GameGUI Screen];
        Q_DISPLAY_GAME_GUI --> Q_MODE_CHOICE{Mode == 'easy'?};

        subgraph Easy_Mode_Answer [Easy Mode]
            direction LR
            Q_MODE_CHOICE -- Yes --> EM_USER_CHOICE[User Clicks Choice Button];
            EM_USER_CHOICE --> EM_CHECK_ANSWER[GameGUI.check_answer];
            EM_CHECK_ANSWER --> EM_UPDATE_UI[Update Button Colors, Disable Choices];
            EM_UPDATE_UI --> EM_SET_FLAG[Set selected_correct flag];
            EM_SET_FLAG --> SHOW_NEXT_BTN_COMMON;
        end

        subgraph Hard_Mode_Answer [Hard Mode]
            direction LR
            Q_MODE_CHOICE -- No (Hard) --> HM_USER_INPUT[User Types Answer & Submits];
            HM_USER_INPUT --> HM_CHECK_TEXT_ANSWER[GameGUI.check_text_answer];
            HM_CHECK_TEXT_ANSWER --> HM_INPUT_EMPTY{Input Empty?};
            HM_INPUT_EMPTY -- Yes --> HM_SHOW_ERROR["Show 'Please enter answer' Error"];
            HM_SHOW_ERROR --> HM_USER_INPUT;
            HM_INPUT_EMPTY -- No --> HM_EVAL_ANSWER["Normalize & Compare Input"];
            HM_EVAL_ANSWER --> HM_FEEDBACK["Display 'Correct!' or 'Incorrect...'"];
            HM_FEEDBACK --> HM_SET_FLAG[Set selected_correct flag];
            HM_SET_FLAG --> HM_DISABLE_INPUT[Disable Entry/Submit];
            HM_DISABLE_INPUT --> SHOW_NEXT_BTN_COMMON;
        end

        SHOW_NEXT_BTN_COMMON["Show 'Next' Button in GameGUI"];
        SHOW_NEXT_BTN_COMMON --> USER_CLICKS_GAME_NEXT{"User Clicks 'Next' in GameGUI?"};
        USER_CLICKS_GAME_NEXT -- Yes --> NEXT_QUESTION_CALLBACK[Call GUI._on_next_question];
        NEXT_QUESTION_CALLBACK --> STORE_USER_ANSWER[Store User's Answer for Results];
        STORE_USER_ANSWER --> Q_CHECK_LAST_ANSWER;
    end


    TRIGGER_FINAL_SCORE --> FS_DESTROY_GAME_GUI["Destroy GameGUI Frame"];
    FS_DESTROY_GAME_GUI --> FS_DISPLAY_GAMEOVER["Display 'Game Over! Your Score: ...'"];
    FS_DISPLAY_GAMEOVER --> FS_DISPLAY_LEADERBOARD[Display Leaderboard];
    FS_DISPLAY_LEADERBOARD --> FS_NEW_HIGHSCORE_CHECK{New High Score Achieved?};

    subgraph High_Score_Entry ["High Score Entry (if applicable)"]
        direction TB
        FS_NEW_HIGHSCORE_CHECK -- Yes --> FS_SHOW_NAME_ENTRY[Display Name Entry & Save Button];
        FS_SHOW_NAME_ENTRY --> FS_USER_SAVES_HS{User Enters Name & Clicks Save?};
        FS_USER_SAVES_HS -- Yes --> FS_VALIDATE_NAME[Validate Name];
        FS_VALIDATE_NAME -- Valid --> FS_UPDATE_HS_MANAGER["Update HighScore Manager & File"];
        FS_UPDATE_HS_MANAGER --> FS_SHOW_HS_SAVED_MSG["Show 'High Score Saved!' & Update Leaderboard"];
        FS_SHOW_HS_SAVED_MSG --> FS_DISABLE_SAVE_UI[Disable Save Button/Entry];
        FS_DISABLE_SAVE_UI --> FS_SHOW_ACTION_BUTTONS;
        FS_VALIDATE_NAME -- Invalid --> FS_SHOW_NAME_ERROR[Show Name Error Message];
        FS_SHOW_NAME_ERROR --> FS_USER_SAVES_HS;
    end
    FS_NEW_HIGHSCORE_CHECK -- No --> FS_SHOW_ACTION_BUTTONS;
    FS_USER_SAVES_HS -- No (User does something else before saving) --> FS_SHOW_ACTION_BUTTONS;


    FS_SHOW_ACTION_BUTTONS["Display 'Restart', 'Quit', 'Export', 'View Results' Buttons"];
    FS_SHOW_ACTION_BUTTONS --> FS_USER_ACTION_CHOICE{User Clicks Action Button?};

    subgraph Final_Screen_Actions [Final Screen Actions]
        direction LR
        FS_USER_ACTION_CHOICE -- "Restart" --> FS_CALL_RESTART["Call GUI._restart_quiz"];
        FS_CALL_RESTART --> TRIGGER_GAME_SCREEN

        FS_USER_ACTION_CHOICE -- "Quit" --> B5;

        FS_USER_ACTION_CHOICE -- "Export Results" --> FS_CALL_EXPORT[Call GUI.export_results];
        FS_CALL_EXPORT --> FS_WRITE_EXPORT_FILE["Write Results to quiz_results.txt"];
        FS_WRITE_EXPORT_FILE --> FS_SHOW_EXPORT_MSG["Show 'Results Exported' Message + Open Buttons"];
        FS_SHOW_EXPORT_MSG --> FS_SHOW_ACTION_BUTTONS;

        FS_USER_ACTION_CHOICE -- "View Results" --> FS_CALL_VIEW[Call GUI.view_results];
        FS_CALL_VIEW --> FS_SHOW_VIEW_POPUP[Display Results in Pop-up];
        FS_SHOW_VIEW_POPUP -- User Closes Pop-up --> FS_SHOW_ACTION_BUTTONS;
    end

    B10 --> LAUNCH_MAIN_LOOP["Start Main Event Loop (root.mainloop())"];
    LAUNCH_MAIN_LOOP --> APP_RUNNING((Application Running - Event Driven Until Quit));