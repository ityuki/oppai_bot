create table if not exists flag(
    id int not null,
    userid text not null,
    msg text not null,
    crate_at int not null,
    PRIMARY KEY(id)
);
