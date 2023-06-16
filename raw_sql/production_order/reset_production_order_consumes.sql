select * from "bakeryAdmin_productionorder";

select * from "bakeryAdmin_supplierinvoicedetail";
select * from "bakeryAdmin_productionorderconsume";

select * from "bakeryAdmin_productstock";
select * from "bakeryAdmin_productionorderconsumeproduct";


update "bakeryAdmin_productionorder" set "startedDate"=null, "canceledDate"=null where id=2;
update "bakeryAdmin_supplierinvoicedetail" set "quantityConsumed" = 0 where ingredient_Id = 1;
update "bakeryAdmin_productstock" set "quantityConsumed" = 0 where product_id = 2;
truncate table "bakeryAdmin_productionorderconsume";
truncate table "bakeryAdmin_productionorderconsumeproduct";


select * from "bakeryAdmin_ingredient"

select * from "bakeryAdmin_recipedetail"

select * from "bakeryAdmin_productstock";
truncate table "bakeryAdmin_productstock" cascade
