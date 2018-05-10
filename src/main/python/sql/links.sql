CREATE TABLE `rhlink`.`sql_true_link` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '',
  `repo_id` INT NOT NULL COMMENT '',
  `sha` VARCHAR(40) NOT NULL COMMENT '',
  `issue_index` VARCHAR(255) NOT NULL COMMENT '',
  PRIMARY KEY (`id`)  COMMENT '');

CREATE TABLE `rhlink`.`sql_false_link` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '',
  `repo_id` INT NOT NULL COMMENT '',
  `sha` VARCHAR(40) NOT NULL COMMENT '',
  `issue_index` VARCHAR(255) NOT NULL COMMENT '',
  PRIMARY KEY (`id`)  COMMENT '');

CREATE TABLE `rhlink`.`sql_unknow_link` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '',
  `repo_id` INT NOT NULL COMMENT '',
  `sha` VARCHAR(40) NOT NULL COMMENT '',
  `issue_index` VARCHAR(255) NOT NULL COMMENT '',
  PRIMARY KEY (`id`)  COMMENT '');
