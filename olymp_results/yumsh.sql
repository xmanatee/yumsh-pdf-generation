DROP TABLE IF EXISTS `<prefix>marks`;
DROP TABLE IF EXISTS `<prefix>pupils`;

CREATE TABLE `<prefix>pupils` (
  `id_pupil`    int(11)  NOT NULL,
  `family`      char(64) NOT NULL,
  `name`        char(64) NOT NULL,
  `paral`       int(11)  NOT NULL,
  `year`        int(11)  NOT NULL,
  `school_name` char(254) NOT NULL,
  `district`    char(254) NOT NULL,
  `sum`         char(64) NOT NULL,
  `result`      char(64) NOT NULL,
  `seen`        int(11)  NOT NULL DEFAULT 0,
  -- UNIQUE (LOWER(family), LOWER(name), paral, year, LOWER(school_name)),
  PRIMARY KEY (`id_pupil`, `year`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `<prefix>marks` (
  `id_pupil` int(11)  NOT NULL,
  `year`     int(11)  NOT NULL,
  `z_num`    char(16) NOT NULL,
  `mark`     int(11)  NOT NULL,
  FOREIGN KEY(`id_pupil`, `year`) REFERENCES <prefix>pupils(`id_pupil`, `year`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

