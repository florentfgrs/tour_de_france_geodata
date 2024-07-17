LOAD SPATIAL ;

DROP TABLE IF EXISTS tour_de_france_{0} ;

CREATE TABLE tour_de_france_{0} (
    numero INTEGER NOT NULL,
    date DATE,
    depart VARCHAR,
    arrivee VARCHAR,
    long FLOAT,
    denivele FLOAT,
    type VARCHAR,
    wiki VARCHAR,
    geom GEOMETRY
) ;
