-- DROP TABLE public.particlesimentry;

CREATE TABLE public.particlesimentry
(
  id SERIAL,
  t bigint,
  pid bigint,
  a double precision,
  e double precision,
  i double precision,
  ascendingnode double precision,
  omega double precision,
  pomega double precision,
  l double precision,
  f double precision,
  resonantangle double precision
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.particlesimentry
  OWNER TO postgres;
GRANT ALL ON TABLE public.particlesimentry TO postgres;
--GRANT ALL ON TABLE public.particlesimentry TO dbUser;
