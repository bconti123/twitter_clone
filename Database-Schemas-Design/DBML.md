Table Follows {
  followed_user_id integer
  following_user_id integer
}

Table Likes {
  id integer [primary key]
  user_id integer
  message_id integer
}

Table Users {
  id integer [primary key]
  email text
  username text
  image_url text
  header_image_url text
  bio text
  location text
  password text
}

Table Message {
  id integer [primary key]
  text string
  created_at timestamp
  user_id integer
}



Ref: "Likes"."user_id" < "Users"."id"

Ref: "Likes"."message_id" < "Message"."id"

Ref: "Follows"."followed_user_id" < "Users"."id"

Ref: "Follows"."following_user_id" < "Users"."id"