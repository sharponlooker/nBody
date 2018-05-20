-- DROP INDEX public.planetsimentry_pid_t_idx;

CREATE UNIQUE INDEX planetsimentry_pid_t_idx
  ON public.planetsimentry
  USING btree
  (pid, t);

-- DROP INDEX public.planetsimentry_planet_t_idx;

CREATE UNIQUE INDEX planetsimentry_planet_t_idx
  ON public.planetsimentry
  USING btree
  (planet, t);

