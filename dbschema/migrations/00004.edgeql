CREATE MIGRATION m1dersmzcm5uroanbdipwzwv36cxhchgrl44bkdw57eh64kc6kxina
    ONTO m1qptkik76z54exuhizo5tx62pozk6dard3jz35wz5h3hvaqaf7duq
{
  CREATE TYPE default::EdgeAccessTokenUser {
      CREATE REQUIRED PROPERTY created_at -> std::datetime {
          SET default := (std::datetime_current());
      };
      CREATE REQUIRED PROPERTY token -> std::str {
          CREATE CONSTRAINT std::exclusive;
      };
  };
  ALTER TYPE default::User {
      CREATE MULTI LINK access_tokens -> default::EdgeAccessTokenUser {
          ON SOURCE DELETE DELETE TARGET;
          CREATE CONSTRAINT std::exclusive;
      };
  };
  CREATE TYPE default::OAuthUser {
      CREATE REQUIRED PROPERTY access_token -> std::str;
      CREATE REQUIRED PROPERTY account_email -> std::str {
          CREATE CONSTRAINT std::regexp(r'^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$');
      };
      CREATE REQUIRED PROPERTY account_id -> std::str;
      CREATE PROPERTY expires_at -> std::int32;
      CREATE REQUIRED PROPERTY oauth_name -> std::str;
      CREATE PROPERTY refresh_token -> std::str;
  };
  ALTER TYPE default::User {
      CREATE MULTI LINK oauth_accounts -> default::OAuthUser {
          ON SOURCE DELETE DELETE TARGET;
          CREATE CONSTRAINT std::exclusive;
      };
  };
};
