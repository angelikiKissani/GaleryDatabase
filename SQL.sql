DROP TABLE IF EXISTS visitor
DROP TABLE IF EXISTS Ticket
DROP TABLE IF EXISTS Ticket_Temp
DROP TABLE IF EXISTS Ticket_general
DROP TABLE IF EXISTS Ticket_perm
DROP TABLE IF EXISTS Temp_exhibition
DROP TABLE IF EXISTS EXHIBITION
DROP TABLE IF EXISTS PERM_EXHIBITION
DROP TABLE IF EXISTS PRESENTS
DROP TABLE IF EXISTS COLLECTION
DROP TABLE IF EXISTS PAINTING
DROP TABLE IF EXISTS COPY
DROP TABLE IF EXISTS CATEGORY
DROP TABLE IF EXISTS ARTIST
DROP TABLE IF EXISTS PURCHASE
DROP TABLE IF EXISTS CUSTOMER

CREATE TABLE "Artist" (
	"First_Last_name"	TEXT NOT NULL,
	"nationality"	TEXT NOT NULL,
	"active_period"	TEXT NOT NULL,
	PRIMARY KEY("First_Last_name")
);

CREATE TABLE "Copy" (
	"id_painting"	INTEGER NOT NULL,
	"price"	TEXT NOT NULL,
	"title_of_painting"	TEXT NOT NULL,
	"number_of_copies"	INTEGER NOT NULL,
	PRIMARY KEY("id_painting"),
	FOREIGN KEY("title_of_painting") REFERENCES "Painting"("title"),
	FOREIGN KEY("id_painting") REFERENCES "Painting"("id_painting")
);

CREATE TABLE "Exhibition" (
	"id_exhibition"	INTEGER NOT NULL,
	"name_of_exhibition"	TEXT NOT NULL,
	PRIMARY KEY("id_exhibition")
);

CREATE TABLE "Painting" (
	"id_painting"	INTEGER NOT NULL,
	"title"	TEXT NOT NULL,
	"dimensions"	TEXT NOT NULL,
	"artist"	TEXT NOT NULL,
	"movement"	TEXT NOT NULL,
	"year"	TEXT NOT NULL,
	"process_of_painting"	TEXT NOT NULL,
	"price"	TEXT NOT NULL,
	PRIMARY KEY("id_painting"),
	FOREIGN KEY("artist") REFERENCES "Artist"("First_Last_name")
);

CREATE TABLE "Perm_exhibition" (
	"id_perm_exhibition"	INTEGER NOT NULL,
	PRIMARY KEY("id_perm_exhibition"),
	FOREIGN KEY("id_perm_exhibition") REFERENCES "Exhibition"("id_exhibition")
);

CREATE TABLE "Purchase" (
	"receipt"	INTEGER NOT NULL,
	"title_of_painting"	INTEGER NOT NULL,
	"date_of_purchase"	NUMERIC NOT NULL,
	"total_price"	TEXT NOT NULL,
	PRIMARY KEY("receipt"),
	FOREIGN KEY("total_price") REFERENCES "Copy"("price"),
	FOREIGN KEY("title_of_painting") REFERENCES "Copy"("title_of_painting")
);

CREATE TABLE "Temp_exhibition" (
	"id_temp_exhibition"	INTEGER NOT NULL,
	"start_date"	TEXT NOT NULL,
	"closing_date"	TEXT NOT NULL,
	PRIMARY KEY("id_temp_exhibition"),
	FOREIGN KEY("id_temp_exhibition") REFERENCES "Exhibition"("id_exhibition")
);

CREATE TABLE "Ticket" (
	"id_ticket"	INTEGER NOT NULL,
	"duration"	TEXT NOT NULL,
	"price"	TEXT NOT NULL,
	"date_of_print"	TEXT NOT NULL,
	PRIMARY KEY("id_ticket")
);

CREATE TABLE "Ticket_Perm" (
	"id_ticket_perm"	INTEGER NOT NULL,
	"id_exhibition"	INTEGER NOT NULL,
	PRIMARY KEY("id_ticket_perm"),
	FOREIGN KEY("id_exhibition") REFERENCES "Perm_exhibition"("id_perm_exhibition"),
	FOREIGN KEY("id_ticket_perm") REFERENCES "Ticket"("id_ticket")
);

CREATE TABLE "Ticket_Temp" (
	"id_ticket_temp"	INTEGER NOT NULL,
	"id_exhibition"	INTEGER NOT NULL,
	PRIMARY KEY("id_ticket_temp")
);

CREATE TABLE "presents" (
	"id_exhibition"	INTEGER NOT NULL,
	"id_painting"	INTEGER NOT NULL,
	FOREIGN KEY("id_exhibition") REFERENCES "Exhibition"("id_exhibition"),
	FOREIGN KEY("id_painting") REFERENCES "Painting"("id_painting")
);