CREATE MIGRATION m1hse75luapi5rkvbzajeyvwhjbd642w73f5hpgj2xadvhmax4wbaq
    ONTO m1af5dm4ynl5f74barqv4vez3xq4c4j5mpnbuvwgarllah734l4diq
{
  ALTER TYPE default::Answer {
      CREATE PROPERTY is_accepted -> std::bool {
          SET default := false;
      };
  };
  ALTER SCALAR TYPE default::Age {
      CREATE CONSTRAINT std::max_value(110);
  };
  ALTER SCALAR TYPE default::Age {
      DROP CONSTRAINT std::max_value(120);
  };
};
