import psycopg2

host = "localhost"
database = "postgresv2"
user = "postgres"
password = "postgres"
port = "5432"

connect = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
curs = connect.cursor()
curs.execute("ROLLBACK")

curs.execute('''create table user_person(
                    id_user serial primary key,
                    username varchar (255) not null UNIQUE,
                    email varchar (255) not null UNIQUE,                    
                    password varchar (255) not null,
                    status BOOLEAN DEFAULT false,
                    isadmin BOOLEAN DEFAULT false                    
                );
                create table hardware(
                    id_hardware serial primary key,
                    name varchar (255) not null,
                    type varchar (255) not null,
                    description varchar (255) not null
                );
                create table node(
                    id_node serial primary key,
                    id_user integer not null,                    
                    id_hardware_node integer not null, 
                    id_hardware_sensor integer[10], 
                    name varchar (255) not null, 
                    location varchar (255) not null, 
                    field_sensor text[10] not null DEFAULT {'','','','','','','','','',''}
                    is_public BOOLEAN default false,
                    foreign key (id_hardware_node) references hardware (id_hardware) on update cascade on delete cascade,
                    foreign key (id_user) references user_person (id_user) on update cascade on delete cascade
                ); 
                create table feed(
                    id_node integer not null,
                    time timestamp NOT NULL,
                    value float[10] NOT NULL,
                    foreign key (id_node) references node (id_node) on update cascade on delete cascade                    
                );''')
