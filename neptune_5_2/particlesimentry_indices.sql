-- DROP INDEX public.particlesimentry_pid_t_idx;

CREATE UNIQUE INDEX particlesimentry_pid_t_idx
  ON public.particlesimentry
  USING btree
  (pid, t);



