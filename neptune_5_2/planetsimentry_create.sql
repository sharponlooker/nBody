-- DROP TABLE public.planetsimentry;

CREATE TABLE public.planetsimentry
(
  id integer NOT NULL DEFAULT nextval('planetsimentry_id_seq'::regclass),
  t bigint,
  pid bigint,
  planet smallint,
  x double precision,
  y double precision,
  z double precision,
  vx double precision,
  vy double precision,
  vz double precision,
  a double precision,
  e double precision,
  i double precision,
  ascendingnode double precision,
  omega double precision,
  pomega double precision,
  l double precision,
  CONSTRAINT planetsimentry_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.planetsimentry
  OWNER TO postgres;
GRANT ALL ON TABLE public.planetsimentry TO postgres;
--GRANT ALL ON TABLE public.planetsimentry TO dbUser;
