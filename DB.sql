PGDMP     -    /            
    {            Traffic_Light_Management    14.5    14.5     �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    16768    Traffic_Light_Management    DATABASE     |   CREATE DATABASE "Traffic_Light_Management" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'English_Philippines.1252';
 *   DROP DATABASE "Traffic_Light_Management";
                postgres    false                        2615    16793    TRiAL    SCHEMA        CREATE SCHEMA "TRiAL";
    DROP SCHEMA "TRiAL";
                postgres    false            �            1259    16787    users    TABLE     �   CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(50) NOT NULL,
    email character varying(50) NOT NULL,
    password character varying(200)
);
    DROP TABLE public.users;
       public         heap    postgres    false            �            1259    16786    users_id_seq    SEQUENCE     �   CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.users_id_seq;
       public          postgres    false    211            �           0    0    users_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;
          public          postgres    false    210            ]           2604    16790    users id    DEFAULT     d   ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);
 7   ALTER TABLE public.users ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    210    211    211            �          0    16787    users 
   TABLE DATA           >   COPY public.users (id, username, email, password) FROM stdin;
    public          postgres    false    211   T       �           0    0    users_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.users_id_seq', 8, true);
          public          postgres    false    210            _           2606    16792    users users_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public            postgres    false    211            �   H  x��S�n�1����5rb'q��G��Qi[��;q֮t�J�1���!q��e'��s�c�ɻ�n/.ײ���l֓��j�Ͽ-ć�<�����~���H��.Ș�:L$���h}�\�Y�U &��B攈"!7�(��6���e��G���1Lw ۳��嶅��*54JZB��YuF"�+�+����9�Q^anj2���v����)������يf�}H��o�^{.�} ��KƤ ���DU5wsj%PDc�4���v�蟂?ޜ�]�؜��p��f;�Ѱ9�\j��b�����B��H�r|ȴ�6��$Te�!��ꀻ��f�����|�iLY�
�J4{	(�9Oŧ�ԉR��5�&h���8S*E�q�'F~	��_�r����,����d������n}tX_�W#�r@	�O C�")g�l�Ռ1��$2z�T(�UV8i�ܭ����I0�9���|��G?�m`��;:�}�S��7�?Sd�䃒�Z�ٌ֞rAP���n����$���wzz2�g�߮�F��[2{+j.z����BB	�z{ ���M��:4m\������0?�,�     