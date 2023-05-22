module default {
    abstract type Post {
        required property content -> str;
        property upvotes := (select count(.upvoters));
        property downvotes := (select count(.downvoters));
        required link author -> User;

        property date_created -> datetime {
            readonly := True;
            default := (datetime_of_statement());
        }

        property date_modified -> datetime;
        
        multi link upvoters -> User;
        multi link downvoters -> User;
    }

    type Question extending Post {
        required property title -> str;
        property tags -> array<str>;
        property views -> int16 {default := 0};
        multi link comments -> Comment {
            constraint exclusive;
            on target delete allow;
            on source delete delete target;
        }
        multi link answers -> Answer {
            constraint exclusive;
            on target delete allow;
            on source delete delete target;
        }
    }

    type Answer extending Post {
        multi link comments -> Comment {
            constraint exclusive;
            on target delete allow;
            on source delete delete target;
        }
        property is_accepted -> bool{default := false};
    }

    type Comment extending Post {

    }
}
