--
-- PostgreSQL database dump
--

-- Dumped from database version 15.5
-- Dumped by pg_dump version 16.0

-- Started on 2024-04-29 15:27:47

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;
SET search_path TO app, public;


CREATE EXTENSION IF NOT EXISTS "uuid-ossp";



CREATE schema app;
--
-- TOC entry 7 (class 2615 OID 16425)
-- Name: app; Type: SCHEMA; Schema: -; Owner: admin
--

-- FUNCTION: public.nanoid(integer, text)
-- DROP FUNCTION IF EXISTS public.nanoid(integer, text);
CREATE OR REPLACE FUNCTION public.nanoid(
	size integer DEFAULT 21,
	alphabet text DEFAULT '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'::text)
    RETURNS text
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
DECLARE
    idBuilder text := '';
    i int := 0;
    bytes bytea;
    alphabetIndex int;
    mask int;
    step int;
BEGIN
    mask := (2 << cast(floor(log(length(alphabet) - 1) / log(2)) as int)) - 1;
    step := cast(ceil(1.6 * mask * size / length(alphabet)) AS int);
    while true
        loop
            bytes := gen_random_bytes(size);
            while i < size
                loop
                    alphabetIndex := (get_byte(bytes, i) & mask) + 1;
                    if alphabetIndex <= length(alphabet) then
                        idBuilder := idBuilder || substr(alphabet, alphabetIndex, 1);
                        if length(idBuilder) = size then
                            return idBuilder;
                        end if;
                    end if;
                    i = i + 1;
                end loop;
            i := 0;
        end loop;
END
$BODY$;
ALTER FUNCTION public.nanoid(integer, text)
    OWNER TO admin;




ALTER SCHEMA app OWNER TO admin;


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 217 (class 1259 OID 16476)
-- Name: api_keys; Type: TABLE; Schema: app; Owner: admin
--

CREATE TABLE app.api_keys (
    key_id character(16) DEFAULT public.nanoid(16) NOT NULL,
    api_key uuid DEFAULT public.uuid_generate_v4(),
    description text NOT NULL,
    user_id character(16) NOT NULL,
    team_id character(16),
    created timestamp without time zone DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'::text) NOT NULL,
    expires timestamp without time zone,
    revoked boolean DEFAULT false NOT NULL,
    deleted boolean DEFAULT false NOT NULL,
    type text DEFAULT 'app-source'::text NOT NULL
);


ALTER TABLE app.api_keys OWNER TO admin;
