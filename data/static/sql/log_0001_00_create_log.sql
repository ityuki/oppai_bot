create table if not exists log(
    id int not null,
    channel text not null,
    userid text not null,
    msg text not null,
    create_at int not null,
    PRIMARY KEY(id)
);
