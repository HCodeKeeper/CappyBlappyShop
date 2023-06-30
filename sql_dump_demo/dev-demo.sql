use cbshop;

insert into shop_category 
values (1, "Capybaras");

insert into shop_product 
values (1, "Gort", "images/products/cappyManufacturer/gort.jpeg", 0,
"A truly astonishing creature named of Gort! Though is still accused of hijacking and commiting several war crimes.",
"Cappy", "+380 50 - -. Our call center will get you bussin",
500.49, 200, 1),
(2, "Quandale Dingle", "images/products/cappyManufacturer/Quandale Dingle.png",
5, "Do I need to say something about this beautiful creature?",
"Cappy", "+380 50 - -. Our call center will get you bussin", 469.00, 10, 1);

insert into shop_deal
values (1, "30% off of Dale!", 30, 2);

insert into shop_addon values
(1, "Polishing", 9.99, 1);