--Revert Close Production Order
select * from "bakeryAdmin_productionorder";
select * from "bakeryAdmin_product";
select * from "bakeryAdmin_productstock";

delete from "bakeryAdmin_productstock" where product_id = 4;
delete from "bakeryAdmin_product" where id = 4;
update "bakeryAdmin_productionorder" set "closedDate"=null where id=2;
