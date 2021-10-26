create table if not exists word(
    id int not null,
    userid text not null,
    msg text not null,
    crate_at int not null,
    PRIMARY KEY(id)
);
