PGDMP      6                 }            Performance Management System    14.13    16.4 O    X           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            Y           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            Z           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            [           1262    24875    Performance Management System    DATABASE     �   CREATE DATABASE "Performance Management System" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Chinese (Simplified)_China.936';
 /   DROP DATABASE "Performance Management System";
                postgres    false                        2615    2200    public    SCHEMA     2   -- *not* creating schema, since initdb creates it
 2   -- *not* dropping schema, since initdb creates it
                postgres    false            \           0    0    SCHEMA public    ACL     Q   REVOKE USAGE ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO PUBLIC;
                   postgres    false    4            G           1247    24877    gender_type    TYPE     E   CREATE TYPE public.gender_type AS ENUM (
    'male',
    'female'
);
    DROP TYPE public.gender_type;
       public          postgres    false    4            M           1247    24888    order_status    TYPE     X   CREATE TYPE public.order_status AS ENUM (
    'pending',
    'paid',
    'cancelled'
);
    DROP TYPE public.order_status;
       public          postgres    false    4            J           1247    24882    ticket_class    TYPE     D   CREATE TYPE public.ticket_class AS ENUM (
    'VIP',
    'Basic'
);
    DROP TYPE public.ticket_class;
       public          postgres    false    4            �            1259    24896    actors    TABLE     �   CREATE TABLE public.actors (
    actor_id integer NOT NULL,
    actor_name character varying(50) NOT NULL,
    gender public.gender_type NOT NULL,
    birthday date NOT NULL,
    biography text
);
    DROP TABLE public.actors;
       public         heap    postgres    false    839    4            �            1259    24895    actors_actor_id_seq    SEQUENCE     �   CREATE SEQUENCE public.actors_actor_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.actors_actor_id_seq;
       public          postgres    false    210    4            ]           0    0    actors_actor_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.actors_actor_id_seq OWNED BY public.actors.actor_id;
          public          postgres    false    209            �            1259    24915    dramas    TABLE     �   CREATE TABLE public.dramas (
    drama_id integer NOT NULL,
    drama_name character varying(50) NOT NULL,
    description text NOT NULL,
    duration integer NOT NULL,
    CONSTRAINT dramas_duration_check CHECK ((duration > 0))
);
    DROP TABLE public.dramas;
       public         heap    postgres    false    4            �            1259    24914    dramas_drama_id_seq    SEQUENCE     �   CREATE SEQUENCE public.dramas_drama_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.dramas_drama_id_seq;
       public          postgres    false    4    214            ^           0    0    dramas_drama_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.dramas_drama_id_seq OWNED BY public.dramas.drama_id;
          public          postgres    false    213            �            1259    24992    orders    TABLE     �   CREATE TABLE public.orders (
    order_id integer NOT NULL,
    user_id integer NOT NULL,
    ticket_id integer NOT NULL,
    seat_id character varying(3) NOT NULL,
    status public.order_status DEFAULT 'pending'::public.order_status
);
    DROP TABLE public.orders;
       public         heap    postgres    false    845    4    845            �            1259    24991    orders_order_id_seq    SEQUENCE     �   CREATE SEQUENCE public.orders_order_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.orders_order_id_seq;
       public          postgres    false    4    224            _           0    0    orders_order_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.orders_order_id_seq OWNED BY public.orders.order_id;
          public          postgres    false    223            �            1259    24941    performance_actors    TABLE     �   CREATE TABLE public.performance_actors (
    performance_id integer NOT NULL,
    role character varying(50) NOT NULL,
    actor_id integer NOT NULL
);
 &   DROP TABLE public.performance_actors;
       public         heap    postgres    false    4            �            1259    24925    performances    TABLE     �   CREATE TABLE public.performances (
    performance_id integer NOT NULL,
    drama_id integer NOT NULL,
    theater_id integer NOT NULL
);
     DROP TABLE public.performances;
       public         heap    postgres    false    4            �            1259    24924    performances_performance_id_seq    SEQUENCE     �   CREATE SEQUENCE public.performances_performance_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 6   DROP SEQUENCE public.performances_performance_id_seq;
       public          postgres    false    216    4            `           0    0    performances_performance_id_seq    SEQUENCE OWNED BY     c   ALTER SEQUENCE public.performances_performance_id_seq OWNED BY public.performances.performance_id;
          public          postgres    false    215            �            1259    24954 	   schedules    TABLE       CREATE TABLE public.schedules (
    theater_id integer NOT NULL,
    performance_id integer NOT NULL,
    start_time timestamp without time zone NOT NULL,
    end_time timestamp without time zone NOT NULL,
    CONSTRAINT schedules_check CHECK ((start_time < end_time))
);
    DROP TABLE public.schedules;
       public         heap    postgres    false    4            �            1259    25010    staff    TABLE     �   CREATE TABLE public.staff (
    work_id integer NOT NULL,
    work_name character varying(50) NOT NULL,
    password character varying(255) NOT NULL
);
    DROP TABLE public.staff;
       public         heap    postgres    false    4            �            1259    25009    staff_work_id_seq    SEQUENCE     �   CREATE SEQUENCE public.staff_work_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.staff_work_id_seq;
       public          postgres    false    226    4            a           0    0    staff_work_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.staff_work_id_seq OWNED BY public.staff.work_id;
          public          postgres    false    225            �            1259    24905    theaters    TABLE     &  CREATE TABLE public.theaters (
    theater_id integer NOT NULL,
    theater_name character varying(255) NOT NULL,
    address character varying(255) NOT NULL,
    seats integer NOT NULL,
    contact_num character varying(20) NOT NULL,
    CONSTRAINT theaters_seats_check CHECK ((seats > 0))
);
    DROP TABLE public.theaters;
       public         heap    postgres    false    4            �            1259    24904    theaters_theater_id_seq    SEQUENCE     �   CREATE SEQUENCE public.theaters_theater_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.theaters_theater_id_seq;
       public          postgres    false    4    212            b           0    0    theaters_theater_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.theaters_theater_id_seq OWNED BY public.theaters.theater_id;
          public          postgres    false    211            �            1259    24971    tickets    TABLE     \  CREATE TABLE public.tickets (
    ticket_id integer NOT NULL,
    performance_id integer NOT NULL,
    price numeric(10,2) NOT NULL,
    left_tickets integer NOT NULL,
    class public.ticket_class NOT NULL,
    CONSTRAINT tickets_left_tickets_check CHECK ((left_tickets >= 0)),
    CONSTRAINT tickets_price_check CHECK ((price > (0)::numeric))
);
    DROP TABLE public.tickets;
       public         heap    postgres    false    842    4            �            1259    24970    tickets_ticket_id_seq    SEQUENCE     �   CREATE SEQUENCE public.tickets_ticket_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ,   DROP SEQUENCE public.tickets_ticket_id_seq;
       public          postgres    false    4    220            c           0    0    tickets_ticket_id_seq    SEQUENCE OWNED BY     O   ALTER SEQUENCE public.tickets_ticket_id_seq OWNED BY public.tickets.ticket_id;
          public          postgres    false    219            �            1259    24985    users    TABLE       CREATE TABLE public.users (
    user_id integer NOT NULL,
    user_name character varying(50) NOT NULL,
    gender public.gender_type NOT NULL,
    birthday date NOT NULL,
    country character varying(50) NOT NULL,
    password character varying(255) NOT NULL
);
    DROP TABLE public.users;
       public         heap    postgres    false    4    839            �            1259    24984    users_user_id_seq    SEQUENCE     �   CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.users_user_id_seq;
       public          postgres    false    222    4            d           0    0    users_user_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;
          public          postgres    false    221            �           2604    24899    actors actor_id    DEFAULT     r   ALTER TABLE ONLY public.actors ALTER COLUMN actor_id SET DEFAULT nextval('public.actors_actor_id_seq'::regclass);
 >   ALTER TABLE public.actors ALTER COLUMN actor_id DROP DEFAULT;
       public          postgres    false    210    209    210            �           2604    24918    dramas drama_id    DEFAULT     r   ALTER TABLE ONLY public.dramas ALTER COLUMN drama_id SET DEFAULT nextval('public.dramas_drama_id_seq'::regclass);
 >   ALTER TABLE public.dramas ALTER COLUMN drama_id DROP DEFAULT;
       public          postgres    false    214    213    214            �           2604    24995    orders order_id    DEFAULT     r   ALTER TABLE ONLY public.orders ALTER COLUMN order_id SET DEFAULT nextval('public.orders_order_id_seq'::regclass);
 >   ALTER TABLE public.orders ALTER COLUMN order_id DROP DEFAULT;
       public          postgres    false    223    224    224            �           2604    24928    performances performance_id    DEFAULT     �   ALTER TABLE ONLY public.performances ALTER COLUMN performance_id SET DEFAULT nextval('public.performances_performance_id_seq'::regclass);
 J   ALTER TABLE public.performances ALTER COLUMN performance_id DROP DEFAULT;
       public          postgres    false    215    216    216            �           2604    25013    staff work_id    DEFAULT     n   ALTER TABLE ONLY public.staff ALTER COLUMN work_id SET DEFAULT nextval('public.staff_work_id_seq'::regclass);
 <   ALTER TABLE public.staff ALTER COLUMN work_id DROP DEFAULT;
       public          postgres    false    226    225    226            �           2604    24908    theaters theater_id    DEFAULT     z   ALTER TABLE ONLY public.theaters ALTER COLUMN theater_id SET DEFAULT nextval('public.theaters_theater_id_seq'::regclass);
 B   ALTER TABLE public.theaters ALTER COLUMN theater_id DROP DEFAULT;
       public          postgres    false    211    212    212            �           2604    24974    tickets ticket_id    DEFAULT     v   ALTER TABLE ONLY public.tickets ALTER COLUMN ticket_id SET DEFAULT nextval('public.tickets_ticket_id_seq'::regclass);
 @   ALTER TABLE public.tickets ALTER COLUMN ticket_id DROP DEFAULT;
       public          postgres    false    220    219    220            �           2604    24988    users user_id    DEFAULT     n   ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);
 <   ALTER TABLE public.users ALTER COLUMN user_id DROP DEFAULT;
       public          postgres    false    222    221    222            E          0    24896    actors 
   TABLE DATA           S   COPY public.actors (actor_id, actor_name, gender, birthday, biography) FROM stdin;
    public          postgres    false    210   �]       I          0    24915    dramas 
   TABLE DATA           M   COPY public.dramas (drama_id, drama_name, description, duration) FROM stdin;
    public          postgres    false    214   ic       S          0    24992    orders 
   TABLE DATA           O   COPY public.orders (order_id, user_id, ticket_id, seat_id, status) FROM stdin;
    public          postgres    false    224   �l       L          0    24941    performance_actors 
   TABLE DATA           L   COPY public.performance_actors (performance_id, role, actor_id) FROM stdin;
    public          postgres    false    217   �l       K          0    24925    performances 
   TABLE DATA           L   COPY public.performances (performance_id, drama_id, theater_id) FROM stdin;
    public          postgres    false    216   Pm       M          0    24954 	   schedules 
   TABLE DATA           U   COPY public.schedules (theater_id, performance_id, start_time, end_time) FROM stdin;
    public          postgres    false    218    n       U          0    25010    staff 
   TABLE DATA           =   COPY public.staff (work_id, work_name, password) FROM stdin;
    public          postgres    false    226   �o       G          0    24905    theaters 
   TABLE DATA           Y   COPY public.theaters (theater_id, theater_name, address, seats, contact_num) FROM stdin;
    public          postgres    false    212   �o       O          0    24971    tickets 
   TABLE DATA           X   COPY public.tickets (ticket_id, performance_id, price, left_tickets, class) FROM stdin;
    public          postgres    false    220   3s       Q          0    24985    users 
   TABLE DATA           X   COPY public.users (user_id, user_name, gender, birthday, country, password) FROM stdin;
    public          postgres    false    222   �u       e           0    0    actors_actor_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public.actors_actor_id_seq', 8, true);
          public          postgres    false    209            f           0    0    dramas_drama_id_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.dramas_drama_id_seq', 18, true);
          public          postgres    false    213            g           0    0    orders_order_id_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.orders_order_id_seq', 12, true);
          public          postgres    false    223            h           0    0    performances_performance_id_seq    SEQUENCE SET     O   SELECT pg_catalog.setval('public.performances_performance_id_seq', 43, false);
          public          postgres    false    215            i           0    0    staff_work_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.staff_work_id_seq', 1, false);
          public          postgres    false    225            j           0    0    theaters_theater_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.theaters_theater_id_seq', 21, true);
          public          postgres    false    211            k           0    0    tickets_ticket_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public.tickets_ticket_id_seq', 1, false);
          public          postgres    false    219            l           0    0    users_user_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.users_user_id_seq', 10032, true);
          public          postgres    false    221            �           2606    24903    actors actors_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.actors
    ADD CONSTRAINT actors_pkey PRIMARY KEY (actor_id);
 <   ALTER TABLE ONLY public.actors DROP CONSTRAINT actors_pkey;
       public            postgres    false    210            �           2606    24923    dramas dramas_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.dramas
    ADD CONSTRAINT dramas_pkey PRIMARY KEY (drama_id);
 <   ALTER TABLE ONLY public.dramas DROP CONSTRAINT dramas_pkey;
       public            postgres    false    214            �           2606    24998    orders orders_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (order_id);
 <   ALTER TABLE ONLY public.orders DROP CONSTRAINT orders_pkey;
       public            postgres    false    224            �           2606    24930    performances performances_pkey 
   CONSTRAINT     h   ALTER TABLE ONLY public.performances
    ADD CONSTRAINT performances_pkey PRIMARY KEY (performance_id);
 H   ALTER TABLE ONLY public.performances DROP CONSTRAINT performances_pkey;
       public            postgres    false    216            �           2606    24959    schedules schedules_pkey 
   CONSTRAINT     n   ALTER TABLE ONLY public.schedules
    ADD CONSTRAINT schedules_pkey PRIMARY KEY (theater_id, performance_id);
 B   ALTER TABLE ONLY public.schedules DROP CONSTRAINT schedules_pkey;
       public            postgres    false    218    218            �           2606    25015    staff staff_pkey 
   CONSTRAINT     S   ALTER TABLE ONLY public.staff
    ADD CONSTRAINT staff_pkey PRIMARY KEY (work_id);
 :   ALTER TABLE ONLY public.staff DROP CONSTRAINT staff_pkey;
       public            postgres    false    226            �           2606    24913    theaters theaters_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.theaters
    ADD CONSTRAINT theaters_pkey PRIMARY KEY (theater_id);
 @   ALTER TABLE ONLY public.theaters DROP CONSTRAINT theaters_pkey;
       public            postgres    false    212            �           2606    24978    tickets tickets_pkey 
   CONSTRAINT     Y   ALTER TABLE ONLY public.tickets
    ADD CONSTRAINT tickets_pkey PRIMARY KEY (ticket_id);
 >   ALTER TABLE ONLY public.tickets DROP CONSTRAINT tickets_pkey;
       public            postgres    false    220            �           2606    24990    users users_pkey 
   CONSTRAINT     S   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public            postgres    false    222            �           2606    25004    orders orders_ticket_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_ticket_id_fkey FOREIGN KEY (ticket_id) REFERENCES public.tickets(ticket_id);
 F   ALTER TABLE ONLY public.orders DROP CONSTRAINT orders_ticket_id_fkey;
       public          postgres    false    3241    220    224            �           2606    24999    orders orders_user_id_fkey    FK CONSTRAINT     ~   ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);
 D   ALTER TABLE ONLY public.orders DROP CONSTRAINT orders_user_id_fkey;
       public          postgres    false    222    3243    224            �           2606    24949 3   performance_actors performance_actors_actor_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.performance_actors
    ADD CONSTRAINT performance_actors_actor_id_fkey FOREIGN KEY (actor_id) REFERENCES public.actors(actor_id);
 ]   ALTER TABLE ONLY public.performance_actors DROP CONSTRAINT performance_actors_actor_id_fkey;
       public          postgres    false    217    3231    210            �           2606    24944 9   performance_actors performance_actors_performance_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.performance_actors
    ADD CONSTRAINT performance_actors_performance_id_fkey FOREIGN KEY (performance_id) REFERENCES public.performances(performance_id);
 c   ALTER TABLE ONLY public.performance_actors DROP CONSTRAINT performance_actors_performance_id_fkey;
       public          postgres    false    217    216    3237            �           2606    24931 '   performances performances_drama_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.performances
    ADD CONSTRAINT performances_drama_id_fkey FOREIGN KEY (drama_id) REFERENCES public.dramas(drama_id);
 Q   ALTER TABLE ONLY public.performances DROP CONSTRAINT performances_drama_id_fkey;
       public          postgres    false    214    3235    216            �           2606    24936 )   performances performances_theater_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.performances
    ADD CONSTRAINT performances_theater_id_fkey FOREIGN KEY (theater_id) REFERENCES public.theaters(theater_id);
 S   ALTER TABLE ONLY public.performances DROP CONSTRAINT performances_theater_id_fkey;
       public          postgres    false    216    3233    212            �           2606    24965 '   schedules schedules_performance_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.schedules
    ADD CONSTRAINT schedules_performance_id_fkey FOREIGN KEY (performance_id) REFERENCES public.performances(performance_id);
 Q   ALTER TABLE ONLY public.schedules DROP CONSTRAINT schedules_performance_id_fkey;
       public          postgres    false    216    218    3237            �           2606    24960 #   schedules schedules_theater_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.schedules
    ADD CONSTRAINT schedules_theater_id_fkey FOREIGN KEY (theater_id) REFERENCES public.theaters(theater_id);
 M   ALTER TABLE ONLY public.schedules DROP CONSTRAINT schedules_theater_id_fkey;
       public          postgres    false    218    3233    212            �           2606    24979 #   tickets tickets_performance_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tickets
    ADD CONSTRAINT tickets_performance_id_fkey FOREIGN KEY (performance_id) REFERENCES public.performances(performance_id);
 M   ALTER TABLE ONLY public.tickets DROP CONSTRAINT tickets_performance_id_fkey;
       public          postgres    false    220    3237    216            E   b  x�}V�r�6=�_�Ë�K��ĉ{��4Nbמʩ�3�@�J�8 hE߷ ))�ܓ ��}���-&�mG��6l�V{e5���������l2�\>4^�5��)�IEz�`x�,}���}�q{�ߧ%�q�{VQ�Œ�j�Ε��e�Y�f�.c�w�BT�sAڦ+�Q[�Ak�;;i�l����O�t�1=`�T��ڻ߸Uﰳ�;%(p��GJ|��Ni�P�n����a ����7^U�bc9���}�h˅@��>�J8��
^6�����}��Q�Le���&�9��o�Թ��и&�m�Բ�Xƍ�-����ۯW�����f �ms�r6��E3�n?' ���)m�Bv��J�"\���\�'�T>���F$|�z���d�,宪]���U�'}�(��P=U:jg��R��5l�P)�����j��H�O�������)o]�|P�0�_Frn
���P�6[l�ن����0��Q�doV<�������+�-}��vH�Hܿ&C$����*��翎i���w�<�J��7�v@�,Ԛ=ҕ���Dn'��z�~��!_�>VUgs|2ܠ!5�]C_�x�Ó������ U|:I�}�h)b��FHzz��Dϕ4�Ruڛٵ���%�ZWi����Q[p��,2���]i�|��m������Dc���s�������� 4�f@@/�Ҧ��p�4�M�Zv@�	)����:Ė�sFr�s�`���O9�A��ވ?m
�?��Y��s%2x��H|��X�O���6F�
\v�we����O�M�3�>i�a�HХ�J(�پC_�J\�8t�"\��uɖ�����}ۆs������/:�L.N�F�������E#\Ad+���W�ٓ�%��_w�'�n	�3yz�Nϳ����f���Wb�>�*7f(n��
R���Y��!������v���P�������U�$��c� �H�utP�[�B~�H�XU����`���C�c/��P��'������_x�CI�$�0�� ��5��A2!�H֩ct�q����I���k�}l��l�\�q��(�:"ۢ{�
�HZ�sF:��Uͮ
Ie�U�W0~����`��@0�ψ���!6�V.���H� ;l1��A&u)#��\���)͵/tW�쳤J`>�8��l	�S2�zgLk�Z�gL�Fm����+��m�P��Ů�'��TK�b�)�� ��dC��w���a��<F &	���=��+�\�r?���=���v6�ix�(Z��;���80�R�\�ǋ��@���f�n�ђs%OM�Zzë��"���P$Ia���y���������&�rV _Y%"ҬY7`�(��������_���5      I   C	  x��X�v۸����Mod�ٴv�����u��&�=��#� (�~�}�}�~���'ms٢���7-g��j��}itPmtIF�O���\��w��g��A��Tdc����̭T�{k��y�76�m��1)-�3{��4���f2�H�+��J�Z�o��<��j��)R�0Jj�z��s��<��B�E�4��ѓ��ew"[U9cȫBs�nk�ZO�tj�0[n�X��T̝�l(jgC�;�ձIm���;�_()`UQX|h���ޛy�5�߰��#���J׽�g�/EA�g�kV��l����q->��Պ}�'���Z�H��b@��[��uL^:��p-�+==�<�$EoI[3 ��q�[�;�#�)���N������z��3��,�o�شɹ���B��F<�"�ܓE�%Ba��� ����aKgD0t(oN����<Q���C]9��3�
8T���%����95@A�:v���.�1�O��lyv:?�� ��݆, l��I��)Ha@�H��b6כJYUCV�/��?��3UΣH�F�$srJ�2���7H��+Aq�p}��k�j+�$���̖��ϣ�n�7�T��F�ш�\��0�W��Rȅ?-o�e˂n���l8 2��
��+��8�!�$i�2\Fъ��%�C`��w��(��^���p��Ô䥞��ѣ?V�(���f���G4B�<��f[��,��C���V�|�>]]C[A�'ފ&��Cr�P�[`��
 ��].�:"�����q��ɗ �u�U���P<8[e���K����o� �0�<���Z:L����s �6l&����xə��$�EV���D��r]y�<�<s�@A=r�&����M�D>�E��E��p�+�g�^  �H2���0m��C��PuBkCM�jC�f����TB]I�W'����J@U��
l�q! ��#���ք�X
8��.{'bj�W2B��O3I��E�N�4��,ԉũ�Š.-Zl��*�����$B�u~�?�	 ���ި�I�ZV7D���2C�����I0� �j��$�˘�T�G�+2f�pg2τ%�jL�.�m�,���t�vvM(�?�Vc޿����.��㈀�������3(����[|~��Z����3Z�-�Pʍ3Bt �D�0C
�"x�ʜ�;�W�f�#�h�%� 0��'���&-َ�����dŘa�	���9x�v���{��<:HFک�!~��`y@T��	EV��}Vڴ��i^3ƁV�t[�b#��y�Ra���`���"��d֒��>;o���Z1���bC�̓� �hT�2���*0�D �~;�����+ׇE���`)�b�}��>�I�|�%N��u���
�ZG��9 ���8�V�2���O(D�&N^~�yR�!�v��ѱ�8?�E��ݗ�!�D�4��ܣ�����9�<F'u-��F)���|v������P�eC��c��'�����}�пE���l���9Y!�`E1${J��e�^�f���8C4��̡��q�I����} IW��]��!��n��GAXc\�2��8;����#�p���? z����7A�ﯮ.i�H�U�1$���1����Ơ1b(���+�b����F�E�%?-�BH5D��ȗ��ƎXg����^�<H&w��m��2���-c��~�NB���|y�������{�!����jc�tK�*��Y�6�p4 ^�-ݝ�m���[�A��Hv�����D}�!n�p_w�1cE[�J٠�֪�^H��oe��ږY���3ֵ���{e�\N��Ҟc�Q.� �ܖr�l�Η��7]��BZ���	lG��o����/��xx�܇�	���ƐU�WD��g,�3]C�G8��5��{pIE��{�F��;\%F��<w��^o�L06��Q���d�[��	�,\h�5���.&����q�����-Ɍ�!�g���
-f�qt[��|^�K!�����L՚e�� �yxa�����3���tb��F�����@r�:��&>�; t���J�s�=��cn�f&��Pi>IB�d�IR�q�<5r啛(c�=�Q��v����W{+ˣ�NQ5v����q7�E�_ː��?c���������������Z؀L�WG�t� ��J�L��v%��e�{����_! Tm3.Br���v:8��<ҷXgK�b�kGZ��%��X��~���Dw��"��ӷ�(����K�q�D���Є �fw�J_K3��y"�t1L�JcBN�-L����Uj�x\���y�n����RR�u2������      S   2   x���44  i�fd�Y����eh5�B���Ɔ�a�f�=... ʿq      L   B   x�32��H���)���4�22�t*-*�4�\s2�9����9]��2�S�8M����r1z\\\ i^       K   �   x�-��1CϨ����{I�uDbs����1�DZ+X���;��-'N��<��/8�9@�5�iM�BOBqv1A!iw!͢,eZ�b\�Û+�H��6������_����+:�6�@Ձ�Ɔ���/��LNO���[,�!����t��G�~ � �3+       M   �  x�m�ݑ� �����@v ��[��_�"*ݙ<}2���Q����b�Y�@<�E����l&	bt1���wƝ�t�/ˇ����a�+���E�bS�Xe�,ܐf�|qn�k�$�W!R���>_ZR+�he����MT9�F���(W�C��w�;�B�(�X����y�	(��ܝY��*��K�̤��I�y�Z�i�Fh6��覵�� Eki�Gg��m�����2��E3D�"�.�2OҒ�~h���N<���>�fr���t�?Ϟ���?��������6����f��M�����O �J�����q1�Z���PK�m��Tk�)��2��싇����d.~���U�{�!�+���k�$)@���&��I��\���(�ŕ�x縑����11yGu7�23��O�H~�      U   #   x�34 N�̼Ԣ��ļtNC#cS3�=... q��      G   C  x��T�r�8}����;��@<&��L7�vv���E���H.�������^��a�i��0���s�=�^�`�*�*`�mUj�w%T��k]�룱[8+�}�`���se����WY8��m�#�۬s��&f_�f]Ep���p��*`��@&@	$���$d���ʕ��R���Z�� &��"s��e��vu�����QH━$��qp$�kW<�������!7�����Qi�����9K ��yp��:䮆�;]*�t�y`��������+s����܋2�2΀I)C1�3���.1��BT��@4��f`���<�yV���`c(�y��]�I3�b˺@��Ny���U�}]=�hAEJA
� �3��[�����@S�nM�0^��ڿ�
o����I�i$C"*��s��sS����,H�2Q�·����޹����Ű)�C�(	nP�¯i�`���e��d�#(�l)a"�4�rv�l;bS�����+���˧v�=,���*���h�s�4O�*�$E�,@�p����c��_���V�����Wp��M�{�c̦��?xF{��q��q|i�9��	����+eu�6Vx��W~�t��ۖ�L<c@���{���+
7��g��]ԡ�X������>Z�1/
w�O���ť*>�p�)�lr�:���=��$8/1�����č1,��*G"}�J���(�8A��Y[3��d#<1�`HS/�Zj=�"����7`c�0��H����S=`���P2��x��l�xȬ�4v�����x}#�x=��t$�HCF<�"��tY��u"�K����i���'���+>� �RB��4��&�� �      O   �  x�e��1E��Ǡ؉�h�訨h5�/�wfB��9�����~��4���������ο������i-���¡�Β�%FێR�f��
6_���.A��X�f8�T����u�A���t�Ǆ���
׆��m�#DL�������d���#��z��,0_�sn����Nz�XV8�؄�K;�Eou�2�P��V�Lo�uj�[�]h�?�Gbj�խ	��n�|�9��d[A|u��3ϊ=v+���|��ڲ[vC�t�����M�[Ir<��.�:n}��b���2J-��7Le>�#C��031qj+f�3����Z�����C%ݨ�}���]>�T\/hq�����0O���P[/�`�g��Q(̻	g�4�x���Vbt��$,��3t(vwO�x��Kn�|k�6�#�������IZ��H�}"E��&/��~G����YY�%e���8m��<���"�ȋ����zi��s�D�N�Qzf�ӹf��ݑ��%�LG�V�����޸w����������gF����٤����=��rd�TG�Kg���`�w�P�t�n� �7�V|�@�m��`����Z	����5�Cu^�*�-L�OMEI�s~z��@��=�=R��/`�=UL��3X�����]�\ƭ 0�Oܺ�1�}�֒k�:�`M�S-A�i~X}�~~�|>� ����      Q   |   x�e��
�0����]Vf�$س�"} /F��|{�A{��a�2X}�|��^��v�⁠�*��RM���x9��mh�Q�����˾է��R|4�>(��z2���O�����O����0�     