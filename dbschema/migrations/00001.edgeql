CREATE MIGRATION m1af5dm4ynl5f74barqv4vez3xq4c4j5mpnbuvwgarllah734l4diq
    ONTO initial
{
  CREATE FUTURE nonrecursive_access_policies;
  CREATE ABSTRACT TYPE default::Post {
      CREATE REQUIRED PROPERTY content -> std::str;
      CREATE PROPERTY downvote -> std::int16 {
          SET default := 0;
      };
      CREATE PROPERTY upvote -> std::int16 {
          SET default := 0;
      };
  };
  CREATE TYPE default::Answer EXTENDING default::Post;
  CREATE SCALAR TYPE default::Age EXTENDING std::int16 {
      CREATE CONSTRAINT std::max_value(120);
      CREATE CONSTRAINT std::min_value(0);
  };
  CREATE TYPE default::User {
      CREATE MULTI LINK posts -> default::Post;
      CREATE REQUIRED PROPERTY age -> default::Age;
      CREATE REQUIRED PROPERTY first_name -> std::str;
      CREATE REQUIRED PROPERTY last_name -> std::str;
      CREATE REQUIRED PROPERTY username -> std::str {
          CREATE CONSTRAINT std::exclusive;
      };
  };
  ALTER TYPE default::Post {
      CREATE SINGLE LINK author -> default::User;
  };
  CREATE TYPE default::Comment EXTENDING default::Post;
  ALTER TYPE default::Answer {
      CREATE MULTI LINK comments -> default::Comment;
  };
  CREATE TYPE default::Question EXTENDING default::Post {
      CREATE MULTI LINK answer -> default::Answer;
      CREATE MULTI LINK comments -> default::Comment;
      CREATE REQUIRED PROPERTY tags -> array<std::str>;
      CREATE REQUIRED PROPERTY title -> std::str;
  };
};
