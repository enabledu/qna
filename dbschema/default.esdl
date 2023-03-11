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
            #  when the target of a link is deleted, the source is also deleted. This is useful for implementing cascading deletes.
            on target delete allow;
        }
        multi link answer -> Answer {
            #  when the target of a link is deleted, the source is also deleted. This is useful for implementing cascading deletes.
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
