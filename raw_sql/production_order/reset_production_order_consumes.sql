select * from public."bakeryAdmin_productionorder";
select * from public."bakeryAdmin_supplierinvoicedetail";
select * from public."bakeryAdmin_productionorderconsume";

update public."bakeryAdmin_supplierinvoicedetail" set "quantityConsumed" = 0 where ingredient_id = 1
truncate table public."bakeryAdmin_productionorderconsume" cascade;