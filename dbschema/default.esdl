module default {
    abstract type Post {
        required property content -> str;
        property upvote -> int16{default := 0; }
        property downvote -> int16{default := 0; }
        required link author -> User;
    }

    type Question extending Post {
        required property title -> str;
        property tags -> array<str>;
        multi link comments -> Comment {
            on target delete allow;
        }
        multi link answers -> Answer {
            on target delete allow;
        }
    }

    type Answer extending Post {
        multi link comments -> Comment;
        property is_accepted -> bool{default := false};
    }

    type Comment extending Post {

    }
}
