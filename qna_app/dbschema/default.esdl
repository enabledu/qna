module default {
    type User {
        required property first_name -> str;
        required property last_name -> str;
        required property username -> str {
            constraint exclusive;
        }
        required property age -> Age;
        multi link posts -> Post;

    }

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
            on target delete delete source;
        }
        multi link answer -> Answer {
            #  when the target of a link is deleted, the source is also deleted. This is useful for implementing cascading deletes.
            on target delete delete source;
        }
    }

    type Answer extending Post {
        multi link comments -> Comment;
        property is_accepted -> bool{default := false};
    }

    type Comment extending Post {

    }

    scalar type Age extending int16{
        constraint max_value(110);
        constraint min_value(0);
    }
}
