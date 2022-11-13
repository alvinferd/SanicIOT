--
-- PostgreSQL database dump
--

-- Dumped from database version 14.5 (Debian 14.5-1.pgdg110+1)
-- Dumped by pg_dump version 14.4 (Ubuntu 14.4-1.pgdg20.04+1)

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: feed; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.feed (
    "time" timestamp without time zone,
    value double precision[10],
    id_node integer NOT NULL
);


ALTER TABLE public.feed OWNER TO postgres;

--
-- Name: hardware; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.hardware (
    id_hardware integer NOT NULL,
    name character varying(255) NOT NULL,
    type character varying(255) NOT NULL,
    description character varying(255) NOT NULL
);


ALTER TABLE public.hardware OWNER TO postgres;

--
-- Name: hardware_id_hardware_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.hardware_id_hardware_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.hardware_id_hardware_seq OWNER TO postgres;

--
-- Name: hardware_id_hardware_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.hardware_id_hardware_seq OWNED BY public.hardware.id_hardware;


--
-- Name: node; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.node (
    id_node integer NOT NULL,
    id_user integer NOT NULL,
    id_hardware_node integer NOT NULL,
    id_hardware_sensor integer[10],    
    name character varying(255) NOT NULL,
    location character varying(255) NOT NULL,
    field_sensor text[10] NOT NULL DEFAULT '{"","","","","","","","","",""}',
    is_public BOOLEAN NOT NULL DEFAULT false
);


ALTER TABLE public.node OWNER TO postgres;

--
-- Name: node_id_node_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.node_id_node_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.node_id_node_seq OWNER TO postgres;

--
-- Name: node_id_node_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.node_id_node_seq OWNED BY public.node.id_node;


--
-- Name: user_person; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_person (
    id_user integer NOT NULL,
    email character varying(255) NOT NULL,
    username character varying(255) NOT NULL,
    password character varying(255) NOT NULL,
    status boolean DEFAULT false NOT NULL,
    isadmin boolean DEFAULT false NOT NULL
);


ALTER TABLE public.user_person OWNER TO postgres;

--
-- Name: user_person_id_user_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_person_id_user_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_person_id_user_seq OWNER TO postgres;

--
-- Name: user_person_id_user_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_person_id_user_seq OWNED BY public.user_person.id_user;


--
-- Name: hardware id_hardware; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hardware ALTER COLUMN id_hardware SET DEFAULT nextval('public.hardware_id_hardware_seq'::regclass);


--
-- Name: node id_node; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.node ALTER COLUMN id_node SET DEFAULT nextval('public.node_id_node_seq'::regclass);


--
-- Name: user_person id_user; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_person ALTER COLUMN id_user SET DEFAULT nextval('public.user_person_id_user_seq'::regclass);


--
-- Data for Name: hardware; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.hardware (id_hardware, name, type, description) FROM stdin;
1	byvr9qgju9	single-board computer	ienk6lw267n87x66prge
2	h5dkzhqg8a	sensor	34l4bhoxbcjd0hw5urnc
3	6vavn1bet8	microcontroller unit	ayvqubykaesjzns38ngy
4	qvopn9wo1e	sensor	o2t10oq162pgletp5y39
5	gcqog78bly	microcontroller unit	48iancaryn58wj94di5t
6	76oer66tkb	sensor	poum1styvp7gp527creq
7	qee93sbd96	single-board computer	x3egb13m8wu84o632nkn
9	9ydbqha0kd	single-board computer	jus20y770o0gbuvbcqru
10	5k748518g3	single-board computer	jwqkvetebx1o7pdy0nbp
11	iwmlmnr594	sensor	i6xnqug0aw3n99dvnxmn
12	xcu27dzi40	sensor	pcw5or8kt90uyylfcdwe
13	klb1hujv0m	microcontroller unit	jmexmd1vohlzc9ydgzru
14	oxoupmvcdr	single-board computer	bs8u7p6pmltshlk8siyx
15	4vlylme6ef	single-board computer	wminei7w124mvs4cdj2w
16	xd0z3fyqsq	microcontroller unit	v0l64rsd7l2ra49hry7y
17	00g0whexqa	single-board computer	mxfnjdtw638tt1wdxkvw
18	9ugdp1ds2d	sensor	w1matkbbyjldx6zx5mif
19	2kuybh3b2z	microcontroller unit	m3jy538ysudoejwqnwrq
20	40torq8tf0	sensor	kdd4800fgfw085t1ougm
21	qqob96ige7	single-board computer	birvtz2s12idz9tspump
22	pap9maaet5	microcontroller unit	11fn6yhxtq6v8bj5nh82
23	72i0iea9nm	microcontroller unit	kebugrs7fuwcdcxzwfon
24	qfui027hwe	single-board computer	re9xip2k5bj5gqqgxo9z
25	smtqq7g4zb	sensor	q2dnkda6ofd31peh0dyb
26	6rmp8flkqj	single-board computer	jwqk2rkbjmel2mppdrr4
27	90whqmm8yb	microcontroller unit	4c9f87ayq4c9huha2nbw
28	zgde7ql15x	single-board computer	6c30j6ikvergsuio5pw0
29	8bjuk4cze5	microcontroller unit	jckjss0guzggmw67tvkb
30	qpdxjifx9l	sensor	bi19enamckh4lshbvipw
31	5vox3y5v0i	single-board computer	w5cg1r705yuem6skhf2q
32	8o9cgqb7pz	sensor	9fd4nn8bpbzolo5l0xyc
33	zwu4zus5nf	single-board computer	sl6c806cm9sirzaf4fm7
34	gudnaffpoe	sensor	1pmik5y4lhrcwc7rjn7p
35	t8e9wls2un	single-board computer	eefz353wzd1rw40cz1nt
36	bkywd3qhbi	sensor	ugqqx29gsonk1gogxe5p
37	vs30kdzqyr	microcontroller unit	sznfifgdia184swe6kou
38	ib5czkwvdt	sensor	ocs9y9jbixhjr4wtua1y
39	urz9y9rmoj	microcontroller unit	yzkewfd5bdmhpvcw72rx
\.



--
-- Data for Name: user_person; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_person (id_user, email, username, password, status, isadmin) FROM stdin;
1	bintangf00code@gmail.com	perftest	3c31bc6fa467cea84245bf86d594f17936880674f320b94b2cef9f73ac71e51f	t	f
2	alvinferd@example.com	perftestadmin	3c31bc6fa467cea84245bf86d594f17936880674f320b94b2cef9f73ac71e51f	t	t
3	f82r40lp1t@example.com	cfa1p4	2d5af08fb2de2eb414a5d3e95de9ecf652c5a9f901c13e87a8839aae6605efaf	t	f
4	tj4tjrgp6p@example.com	288ls4	25fa68bbe2f045ec2630fe0e5f221cd38d943c452d4ed0be93d485853db3a4e2	t	f
5	tskvlwhwh1@example.com	n6lzz8	187b9fb0a496ce2b1cc8ec0bbeb486cba2a94440f6faa6dd2f751cff6a39a8c9	t	f
6	e9a1d6ijwk@example.com	6enrd7	85ee49350b897383d4b1ba4293ae27a2e57180dff02db61af523b7daaae452d5	t	f
7	uawytk885t@example.com	k5emyv	2e788ca5e53d7f92c8841761d04f6821554446ea80e0976521549e07798bc3f8	t	f
8	k9s1i3txub@example.com	73tutm	07a0da4349facc99560df604883b80a749e9c7e2e660ad087a6e83459d40a3dd	t	f
9	0t3fhi6o6x@example.com	f40zqk	050bc973aeec8238b117a08a4a506185818e2bee82b2dc376593334b3e15b4c8	t	f
10	swmmht5khp@example.com	izbrc1	614f2d7f2d39c0e6f516e51b7ea929fd0a67b5e9e43a1f803a678e30bbcd505f	t	t
11	vcmytwpav9@example.com	9mxycf	0420a7721f74e535b642f64d95eee03e425d0d7b9cd315d3bd3c5f60575839f7	t	f
12	xkwu07a3et@example.com	pl2szd	6c704861710b492ae8b797a7f6c198f7669aa47a23ae0d34185f6769a4723175	t	f
13	i2l43hu969@example.com	v2jlvv	abbdd3efc5dd249471a44a0e01cee8e4ff4807646d5e895b90fab5288aa15d1b	t	f
14	t0p5yfgx18@example.com	couxwu	5d141da6ffe0d887b6d75017148df04d92fb5ab9dc06fb834ddb399b933ec8ef	t	f
15	k0zxvj599a@example.com	lx8449	5f08657a7be95fef768c3ab35285377cac2a6af63bd4b368a1e69508c3d1388f	t	f
16	nupabd1itc@example.com	moc49s	2c68f2b2c2f81f470c593ee0852a9f4e1e4ecf1aa4a70fc54c8d82d0719d2848	t	t
17	irl6oce9kg@example.com	zqsg8c	f6bb884a832b795fc21d901fcddbd141ef35260fd721eb7128e06565d8ada03f	t	f
18	cdbtc17i3d@example.com	b7332j	600497b540cfb31e365303252d8c81bf6055cb55fa4cbe7c48170d53b01cfff7	t	f
19	lgrt594pry@example.com	axmun9	b7f0e25f36fc983ab48cd3fb643cd9c4360b4d2120e004496f4626c7eff9911a	t	f
20	plyhvt41v8@example.com	9ajwt5	d9d6108c94f328716b4a5f5ad7c05c20d1c27985a4880f7c1cd4ff557933d8d4	t	f
21	jolv1jxqaf@example.com	4hllgo	600df4337af6f0de80592e756ad008fca1929a2fd7c9049c13109e36aaf4d2e5	t	f
22	3i9mfchui7@example.com	cjkg7j	bb07fb02004acfafc59812961e447f906ecca74dea9073fb3a88fd920def74b3	t	f
23	lm4xoyz0h0@example.com	hrymb9	34166818511f29d68a1e197917fe3b5e994a314fcf06be13673fcfc3e315127f	t	f
24	iutg7a7a5i@example.com	ga9wmz	52c5d587f26b6581b8c53eeb273f910594d1d5c4da6ee3b843d911cd35953e08	t	f
25	jf0jvoy87t@example.com	8rnp8n	a133d2eaaf4a6385275836b5c3b8dfb5a77346964d3d126534c68aaa21041248	t	f
26	48wholdgug@example.com	l51qr2	0a617fd192db4aee179214b23288c77db7a9f9723e11f7ec0af2acd56e30b979	t	t
27	bqbvxtx7nv@example.com	v3eepn	7cf91e4f7044cf988f4f444e710e9c6de756a5132b5451cf45a4b1508a793e75	f	f
28	rpvkotkpr2@example.com	byc2kc	51f3bf45cc6c6a37d0bcd9f2e5b697c13d379569adf8a60628642c69944cbd1c	t	f
29	dylttt9yo0@example.com	1be0e3	f06a4f98fbfaaa1c5baa4756e3dd1a80d315297a00910ebdbc61d712db966d8d	t	f
30	aq27h5hqqp@example.com	eblpta	eb26b5de31702882734e32e1475690e1bb167868e141e677476cf9926e9e0729	f	f
32	ym8xxe4jku@example.com	6giaie	8b39d284ca01b2cb732fc6e6d9fddfbab36ff05031501539d5b4088df43f5f05	t	f
31	utmzkwd7gu@example.com	xtfac8	469569ec0192e0fe0b9d6420fe1606bfab0d040c175bf4e1a52e71822749b537	t	f
34	2hh7488w7y@example.com	cefehs	27a1c425483476b468409d5e11d5a7e508fa2bcb799c81346ae617ec324fde53	f	f
33	9v30wk83f3@example.com	ouzcfw	cc5ca0efccbebe0014ea58888e4f7156a7ddb018971dcba55727962c0990b799	t	f
36	f6erycu5up@example.com	kswd9a	50aff952d5479c19538e3a1982f76aa9f37a733dadec841aa77ab8865f23b2bd	t	f
38	9rf0dnmozq@example.com	wwit6v	a72d5c7b30767e3f33a7abd41665354d972881a3cc08978d2a5c65e82257c6ea	t	t
\.


--
-- Name: hardware_id_hardware_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.hardware_id_hardware_seq', 39, true);


--
-- Name: node_id_node_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.node_id_node_seq', 21, true);



--
-- Name: user_person_id_user_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_person_id_user_seq', 38, true);


--
-- Name: hardware hardware_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hardware
    ADD CONSTRAINT hardware_pkey PRIMARY KEY (id_hardware);


--
-- Name: node node_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.node
    ADD CONSTRAINT node_pkey PRIMARY KEY (id_node);


--
-- Name: user_person user_person_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_person
    ADD CONSTRAINT user_person_pkey PRIMARY KEY (id_user);


--
-- Name: feed feed_id_node_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.feed
    ADD CONSTRAINT feed_id_node_fkey FOREIGN KEY (id_node) REFERENCES public.node(id_node) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: node node_id_hardware_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.node
    ADD CONSTRAINT node_id_hardware_fkey FOREIGN KEY (id_hardware_node) REFERENCES public.hardware(id_hardware) ON UPDATE CASCADE;


--
-- Name: node node_id_user_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.node
    ADD CONSTRAINT node_id_user_fkey FOREIGN KEY (id_user) REFERENCES public.user_person(id_user) ON UPDATE CASCADE;


--
-- Name: sensor sensor_id_hardware_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

--
-- PostgreSQL database dump complete
--

