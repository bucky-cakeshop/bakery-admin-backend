select * from public."bakeryAdmin_productionorder";
select * from public."bakeryAdmin_supplierinvoicedetail";
select * from public."bakeryAdmin_productionorderconsume";

update public."bakeryAdmin_supplierinvoicedetail" set "quantityConsumed" = 0 where ingredient_id = 1
truncate table public."bakeryAdmin_productionorderconsume" cascade;

select * from public."bakeryAdmin_productionorder" where id = 2;
update public."bakeryAdmin_productionorder" set "startedDate" = null, "canceledDate"=null,"closedDate"=null where id =1

select * from public."bakeryAdmin_productionorder" where id = 1;
select * from public."bakeryAdmin_productionorderconsume" where "productionOrder_id" = 1;
select * from public."bakeryAdmin_supplierinvoicedetail";
update public."bakeryAdmin_productionorder" set "canceledDate"=null where id =1