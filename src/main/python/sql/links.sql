CREATE TABLE `rhlink`.`true_link_27729926` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '',
  `repo_id` INT NOT NULL COMMENT '',
  `sha` VARCHAR(40) NOT NULL COMMENT '',
  `issue_index` VARCHAR(255) NOT NULL COMMENT '',
  PRIMARY KEY (`id`)  COMMENT '');

CREATE TABLE `rhlink`.`false_link_27729926` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '',
  `repo_id` INT NOT NULL COMMENT '',
  `sha` VARCHAR(40) NOT NULL COMMENT '',
  `issue_index` VARCHAR(255) NOT NULL COMMENT '',
  PRIMARY KEY (`id`)  COMMENT '');

CREATE TABLE `rhlink`.`unknow_link_27729926` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '',
  `repo_id` INT NOT NULL COMMENT '',
  `sha` VARCHAR(40) NOT NULL COMMENT '',
  `issue_index` VARCHAR(255) NOT NULL COMMENT '',
  PRIMARY KEY (`id`)  COMMENT '');
