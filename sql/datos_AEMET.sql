CREATE DATABASE datos_AEMET;

CREATE TABLE ubicaciones (
  cod_estacion VARCHAR(10) NOT NULL PRIMARY KEY,
  estacion VARCHAR(100) NOT NULL,
  cod_municipio VARCHAR(10) NOT NULL,
  municipio VARCHAR(100) NOT NULL,
  cod_provincia CHAR(2) NOT NULL,
  provincia VARCHAR(100) NOT NULL,
  cod_com_autonoma CHAR(2) NOT NULL,
  latitud REAL,
  longitud REAL
);


CREATE TABLE temperatura (
  cod_estacion VARCHAR(10) NOT NULL,
  fecha DATE NOT NULL,
  temp_media REAL,
  temp_min REAL,
  hora_temp_min TIME,
  temp_max REAL,
  hora_temp_max TIME,
  PRIMARY KEY (cod_estacion, fecha),
  FOREIGN KEY (cod_estacion) REFERENCES ubicaciones(cod_estacion) ON DELETE CASCADE
);


CREATE TABLE precipitaciones (
  cod_estacion VARCHAR(10) NOT NULL,
  fecha DATE NOT NULL,
  precipitacion REAL,
  PRIMARY KEY (cod_estacion, fecha),
  FOREIGN KEY (cod_estacion) REFERENCES ubicaciones(cod_estacion) ON DELETE CASCADE   
);


CREATE TABLE humedad (
  cod_estacion VARCHAR(10) NOT NULL,
  fecha DATE NOT NULL,
  humedad_max INT,
  hora_hum_max VARCHAR(10),
  humedad_min INT,
  hora_hum_min TIME,
  humedad_media INT,
  PRIMARY KEY (cod_estacion, fecha),
  FOREIGN KEY (cod_estacion) REFERENCES ubicaciones(cod_estacion) ON DELETE CASCADE
);


CREATE TABLE sol (
  cod_estacion VARCHAR(10) NOT NULL,
  fecha DATE NOT NULL,
  horas_sol REAL,
  PRIMARY KEY (cod_estacion, fecha),
  FOREIGN KEY (cod_estacion) REFERENCES ubicaciones(cod_estacion) ON DELETE CASCADE   
);


CREATE TABLE presion (
  cod_estacion VARCHAR(10) NOT NULL,
  fecha DATE NOT NULL,
  presion_max REAL,
  hora_pres_max TIME,
  presion_min REAL,
  hora_pres_min TIME,
  PRIMARY KEY (cod_estacion, fecha),
  FOREIGN KEY (cod_estacion) REFERENCES ubicaciones(cod_estacion) ON DELETE CASCADE
);


CREATE TABLE viento (
  cod_estacion VARCHAR(10) NOT NULL,
  fecha DATE NOT NULL,
  direccion VARCHAR(10),
  velocidad_media REAL,
  racha REAL,
  hora_racha TIME,
  PRIMARY KEY (cod_estacion, fecha),
  FOREIGN KEY (cod_estacion) REFERENCES ubicaciones(cod_estacion) ON DELETE CASCADE
);
