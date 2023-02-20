CREATE MIGRATION m1qptkik76z54exuhizo5tx62pozk6dard3jz35wz5h3hvaqaf7duq
    ONTO m1hse75luapi5rkvbzajeyvwhjbd642w73f5hpgj2xadvhmax4wbaq
{
  ALTER TYPE default::Post {
      ALTER LINK author {
          RESET CARDINALITY;
          SET REQUIRED USING (SELECT
              default::User 
          LIMIT
              1
          );
      };
  };
  ALTER TYPE default::Question {
      ALTER LINK answer {
          ON TARGET DELETE DELETE SOURCE;
      };
  };
  ALTER TYPE default::Question {
      ALTER LINK comments {
          ON TARGET DELETE DELETE SOURCE;
      };
  };
  ALTER TYPE default::Question {
      ALTER PROPERTY tags {
          RESET OPTIONALITY;
      };
  };
  ALTER TYPE default::User {
      CREATE REQUIRED PROPERTY email -> std::str {
          SET REQUIRED USING ('');
          CREATE CONSTRAINT std::exclusive;
          CREATE CONSTRAINT std::regexp(r'^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$');
      };
      CREATE REQUIRED PROPERTY hashed_password -> std::str {
          SET REQUIRED USING ('');
      };
      CREATE REQUIRED PROPERTY is_active -> std::bool {
          SET REQUIRED USING (false);
      };
      CREATE REQUIRED PROPERTY is_superuser -> std::bool {
          SET REQUIRED USING (false);
      };
      CREATE REQUIRED PROPERTY is_verified -> std::bool {
          SET REQUIRED USING (false);
      };
  };
};
