module default {
    abstract type Post {
        required property content -> str;
        property upvotes -> int16{default := 0; }
        property downvotes -> int16{default := 0; }
        required link author -> User;
        
        multi link upvoters -> User {
            constraint exclusive;
        }
        
        multi link downvoters -> User {
            constraint exclusive;
        }
    }

    type Question extending Post {
        required property title -> str;
        property tags -> array<str>;
        multi link comments -> Comment {
            on target delete allow;
            on source delete delete target;
        }
        multi link answers -> Answer {
            on target delete allow;
            on source delete delete target;
        }
    }

    type Answer extending Post {
        multi link comments -> Comment {
            on target delete allow;
            on source delete delete target;
        }
        property is_accepted -> bool{default := false};
    }

    type Comment extending Post {

    }
}
