-- Add migration script here

CREATE TABLE IF NOT EXISTS public.users
(
    id integer NOT NULL,
    name character varying(256) COLLATE pg_catalog."default" NOT NULL,
    cash integer NOT NULL DEFAULT 0,
    CONSTRAINT users_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.users
    OWNER to postgres;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM users WHERE id = 1) THEN
        INSERT INTO users VALUES (1, 'John', 1000);
    END IF;
END $$;