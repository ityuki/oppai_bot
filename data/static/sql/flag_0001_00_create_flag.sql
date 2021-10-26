create table if not exists flag(
    id int not null,
    userid text not null,
    msg text not null,
    is_deleted int not null,
    crate_at int not null,
    PRIMARY KEY(id)
);
