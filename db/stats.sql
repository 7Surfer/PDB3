-- Table: public.stats

-- DROP TABLE IF EXISTS public.stats;

CREATE TABLE IF NOT EXISTS public.stats
(
    "dbKey" bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    rank integer,
    score bigint,
    "researchRank" integer,
    "researchScore" bigint,
    "buildingRank" integer,
    "buildingScore" bigint,
    "defensiveRank" integer,
    "defensiveScore" bigint,
    "fleetRank" integer,
    "fleetScore" bigint,
    "battlesWon" bigint,
    "battlesLost" bigint,
    "battlesDraw" bigint,
    "debrisMetal" bigint,
    "debrisCrystal" bigint,
    "unitsDestroyed" bigint,
    "unitsLost" bigint,
    "playerId" integer NOT NULL,
    "timestamp" timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    "realDebrisMetal" bigint,
    "realDebrisCrystal" bigint,
    "realUnitsDestroyed" bigint,
    "realUnitsLost" bigint,
    CONSTRAINT stats_pkey PRIMARY KEY ("dbKey")
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.stats
    OWNER to poll;

GRANT TRUNCATE, TRIGGER ON TABLE public.stats TO "pdb-admin";

GRANT DELETE ON TABLE public.stats TO "pdb-overquota";

GRANT SELECT ON TABLE public.stats TO "pdb-ro";

GRANT UPDATE, DELETE, INSERT, REFERENCES ON TABLE public.stats TO "pdb-rw";

GRANT ALL ON TABLE public.stats TO poll;