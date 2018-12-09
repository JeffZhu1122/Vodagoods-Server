CREATE TABLE IF NOT EXISTS `app_user`(
   `user_id` INT(10),
   `user_name` VARCHAR(400),
   `user_passwd` VARCHAR(400),
   `user_email` VARCHAR(400),
   `user_phone` VARCHAR(400),
   `user_fight` INT(10),
   `user_group` INT(10),
   `submission_date` DATE,
   `user_team` INT(10),
   `wallet` FLOAT(10,3),
   PRIMARY KEY ( `user_id` )
);

CREATE TABLE IF NOT EXISTS `app_group`(
   `group_id` INT(10),
   `group_name` VARCHAR(400),
   `group_owner_id` INT(10),
   `group_fight` INT(10),
   `group_rank` INT(10),
   `group_max_mbr` INT(10),
   `group_now_mbr` INT(10),
   `group_submission_date` DATE,
   `group_intro` VARCHAR(400),
   PRIMARY KEY ( `group_id` )
);

CREATE TABLE IF NOT EXISTS `app_team`(
   `team_id` INT(10),
   `team_name` VARCHAR(400),
   `team_type` VARCHAR(400),
   `team_owner_id` INT(10),
   `team_fight` INT(10),
   `team_rank` INT(10),
   `team_max_mbr` INT(10),
   `team_now_mbr` INT(10),
   `team_submission_date` DATE,
   `team_intro` VARCHAR(400),
   PRIMARY KEY ( `team_id` )
);

CREATE TABLE IF NOT EXISTS `app_stock`(
   `stock_id` INT(10),
   `stock_name` VARCHAR(400),
   `stock_image_url` VARCHAR(400),
   `stock_price` FLOAT(10,3),
   `stock_number` INT(10),
   `stock_submission_date` DATE,
   PRIMARY KEY ( `stock_id` )
);

CREATE TABLE IF NOT EXISTS `app_order`(
   `order_id` INT(10),
   `order_user_name` VARCHAR(400),
   `order_user_seat` VARCHAR(400),
   `order_name` VARCHAR(400),
   `order_number` INT(10),
   `order_submission_date` DATE,
   PRIMARY KEY ( `order_id` )
);

CREATE TABLE IF NOT EXISTS `app_video`(
   `video_id` INT(10),
   `video_name` VARCHAR(400),
   `video_url` VARCHAR(400),
   `video_image_url` VARCHAR(400),
   `video_submission_date` DATE,
   PRIMARY KEY ( `video_id` )
);

CREATE TABLE IF NOT EXISTS `app_card`(
   `card_id` INT(10),
   `card_number` VARCHAR(400),
   `card_passwd` VARCHAR(400),
   `card_price` INT(10),
   `card_submission_date` DATE,
   `card_use_date` DATE,
   `card_user_name` VARCHAR(400),
   `card_used` INT(10),
   PRIMARY KEY ( `card_id` )
);

CREATE TABLE IF NOT EXISTS `app_netkey`(
   `netkey_id` INT(10),
   `netkey_number` VARCHAR(400),
   `netkey_price` INT(10),
   `netkey_submission_date` DATE,
   `netkey_sold_date` DATE,
   `netkey_sold_name` VARCHAR(400),
   `netkey_sold` INT(10),
   PRIMARY KEY ( `netkey_id` )
);