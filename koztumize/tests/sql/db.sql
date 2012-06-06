BEGIN;

CREATE TABLE rights (
    document_id character varying NOT NULL,
    owner character varying
);


CREATE TABLE user_rights (
    document_id character varying NOT NULL,
    user_id character varying NOT NULL,
    read boolean,
    write boolean
);


CREATE TABLE users (
    "uidNumber" integer NOT NULL,
    "givenName" character varying,
    sn character varying,
    uid character varying,
    "employeeNumber" character varying,
    cn character varying
);


ALTER TABLE ONLY rights
    ADD CONSTRAINT rights_pkey PRIMARY KEY (document_id);

ALTER TABLE ONLY user_rights
    ADD CONSTRAINT pk_user_rights PRIMARY KEY (document_id, user_id);

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY ("uidNumber");


COMMIT;
