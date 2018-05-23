CREATE TABLE `rhlink`.`heal_true_link` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '',
  `repo_id` INT NOT NULL COMMENT '',
  `sha` VARCHAR(40) NOT NULL COMMENT '',
  `issue_index` VARCHAR(255) NOT NULL COMMENT '',
  PRIMARY KEY (`id`)  COMMENT '');

CREATE TABLE `rhlink`.`heal_false_link` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '',
  `repo_id` INT NOT NULL COMMENT '',
  `sha` VARCHAR(40) NOT NULL COMMENT '',
  `issue_index` VARCHAR(255) NOT NULL COMMENT '',
  PRIMARY KEY (`id`)  COMMENT '');

CREATE TABLE `rhlink`.`heal_unknow_link` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '',
  `repo_id` INT NOT NULL COMMENT '',
  `sha` VARCHAR(40) NOT NULL COMMENT '',
  `issue_index` VARCHAR(255) NOT NULL COMMENT '',
  PRIMARY KEY (`id`)  COMMENT '');
