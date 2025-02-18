create table public.comunidades_autonomas (
  id bigint not null,
  nombre text null,
  codigo text null,
  constraint comunidades_autonomas_pkey primary key (id)
) TABLESPACE pg_default;

create table public.provincias (
  id bigint not null,
  nombre text null,
  com_auto_id bigint null,
  constraint provincias_pkey primary key (id),
  constraint provincias_provincia_id_key unique (id),
  constraint provincias_com_auto_id_fkey foreign KEY (com_auto_id) references comunidades_autonomas (id)
) TABLESPACE pg_default;

create table public.municipios (
  id text not null,
  provincia_id bigint null,
  cod_mun bigint null,
  nombre text null,
  altitud bigint null,
  latitud double precision null,
  longitud double precision null,
  num_hab bigint null,
  zona_comarcal bigint null,
  destacada boolean null,
  url text null,
  constraint municipios_pkey primary key (id),
  constraint municipios_provincia_id_fkey foreign KEY (provincia_id) references provincias (id)
) TABLESPACE pg_default;

create table public.estaciones (
  idema text not null,
  nombre text null,
  provincia_id bigint null,
  latitud double precision null,
  longitud double precision null,
  altitud bigint null,
  constraint estaciones_pkey primary key (idema),
  constraint estaciones_provincia_id_fkey foreign KEY (provincia_id) references provincias (id)
) TABLESPACE pg_default;

create table public.humedad_historico (
  uuid uuid not null default gen_random_uuid (),
  fecha date null,
  idema text null,
  "hrMax" smallint null,
  "horaHrMax" time without time zone null,
  "hrMin" smallint null,
  "horaHrMin" time without time zone null,
  "hrMedia" smallint null,
  extracted timestamp with time zone null,
  constraint humedad_historico_pkey primary key (uuid),
  constraint humedad_historico_idema_fkey foreign KEY (idema) references estaciones (idema)
) TABLESPACE pg_default;

create table public.lluvias_historico (
  uuid uuid not null default gen_random_uuid (),
  fecha date null,
  idema text null,
  prec text null,
  extracted timestamp with time zone null,
  constraint lluvias_historico_pkey primary key (uuid),
  constraint lluvias_historico_idema_fkey foreign KEY (idema) references estaciones (idema)
) TABLESPACE pg_default;

create table public.temperatura_historico (
  uuid uuid not null default gen_random_uuid (),
  fecha date null,
  idema text null,
  tmed real null,
  tmin real null,
  horatmin time without time zone null,
  tmax real null,
  horatmax time without time zone null,
  extracted timestamp with time zone null,
  constraint temperatura_historico_pkey primary key (uuid),
  constraint temperatura_historico_idema_fkey foreign KEY (idema) references estaciones (idema)
) TABLESPACE pg_default;

create table public.viento_historico (
  uuid uuid not null default gen_random_uuid (),
  fecha date null,
  idema text null,
  dir smallint null,
  velmedia real null,
  racha real null,
  horaracha time without time zone null,
  extracted timestamp with time zone null,
  constraint viento_historico_pkey primary key (uuid),
  constraint viento_historico_idema_fkey foreign KEY (idema) references estaciones (idema)
) TABLESPACE pg_default;
