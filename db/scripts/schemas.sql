DROP TABLE IF EXISTS public.variants;
DROP TABLE IF EXISTS public.calls;

CREATE TABLE public.variants (
    id SERIAL NOT NULL PRIMARY KEY,
    chromosome character varying(2) NOT NULL,
    variant_id text,
    reference text NOT NULL,
    alternate text NOT NULL,
    start integer NOT NULL,
    "end" integer,
    gene character varying(15),
    AF numeric

);

CREATE TABLE public.calls (
	variant_id int NOT NULL REFERENCES variants(id),
	sample_id text NOT NULL,
	call text NOT NULL,
	PRIMARY KEY (variant_id, sample_id)
);
