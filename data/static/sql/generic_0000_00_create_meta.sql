create table if not exists meta(
    meta_key text not null,
    meta_val text not null,
    PRIMARY KEY(meta_key)
);
