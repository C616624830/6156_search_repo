create database searchbase;
use searchbase;

Drop table if exists catInfo;
Drop table if exists breederInfo;

CREATE TABLE `breederInfo` (
  `id` varchar(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `organization` varchar(100) NOT NULL,
  `phone` varchar(100) NOT NULL,
  `address` varchar(200) NOT NULL,
  `website` varchar(100) NOT NULL,
  `rating` decimal(2,1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
);


CREATE TABLE `catInfo` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `race` varchar(100) NOT NULL,
  `color` varchar(45) NOT NULL,
  `dob` datetime NOT NULL,
  `father` int DEFAULT NULL,
  `mother` int DEFAULT NULL,
  `breeder` varchar(100) NOT NULL,
  `listing_price` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idCat_UNIQUE` (`id`),
  CONSTRAINT FK_breeder FOREIGN KEY (breeder) REFERENCES breederInfo(id) ON DELETE CASCADE,
  CONSTRAINT FK_father FOREIGN KEY (father) REFERENCES catInfo(id) ON DELETE SET NULL,
  CONSTRAINT FK_mother FOREIGN KEY (mother) REFERENCES catInfo(id) ON DELETE SET NULL
);

INSERT INTO breederInfo ( id, name, organization, phone, email, address, website, rating) VALUES ('sw@qq.com','Tom Hanks','TICA','+19176211078','33 brooklyn steet, New York City','www.tomcat.com', 5 );
INSERT INTO catInfo ( id, name, race, color, dob, father, mother, breeder, listing_price) VALUES ( 1,'Alpha','Rugdoll','bicolor','2021-02-03','0', '0','sw@qq.com', 500);