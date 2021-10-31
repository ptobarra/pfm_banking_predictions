GET_ACCOUNT_TRANSACTIONS = "select tt.TRANSACTION_DATE as 'Fecha transacción', cast(aes_decrypt(unhex(ORIGINAL_CURRENCY_AMOUNT), unhex('440733dc90195af99b9b319fef77cb24')) as decimal(14,2)) as 'Importe', "\
"tc.id as 'ID Categoría', tc.name as 'Nombre de categoría', tc.level, tcp.ID, tcp.name, provider.PROVIDER_NAME as Proveedor, trademark.NAME as Trademark, sector.NAME as Sector, "\
"case "\
"	when tc.IS_FINANCIAL = 1 then 'True' "\
"	else 'False' "\
"end CATEGORY_IS_FINANCIAL, "\
"case "\
"	when tc.IS_TRANSFER = 1 then 'True' "\
"	else 'False' "\
"end CATEGORY_IS_TRANSFER "\
"from t_transactions tt "\
"left join t_categories tc on tt.CATEGORY_ID = tc.id "\
"left join t_categories tcp on tc.PARENT_ID = tcp.id "\
"left join t_providers provider on tt.PROVIDER_ID = provider.id "\
"left join t_trademarks trademark on tt.TRADEMARK_ID = trademark.id "\
"left join t_provider_activity_sectors sector on provider.PROVIDER_ACTIVITY_SECTOR_ID = sector.ID "\
"where tt.ACCOUNT_ID = #account_id# "\
"and tt.DELETED = 0 "\
"order by tt.TRANSACTION_DATE desc, tt.`TIMESTAMP` desc; "

GET_ACCOUNT_TRANSACTIONS_2 = "select tt.TRANSACTION_DATE as 'Fecha transacción', ORIGINAL_CURRENCY_AMOUNT as 'Importe', "\
"tc.id as 'ID Categoría', tc.name as 'Nombre de categoría', tc.level, tcp.ID, tcp.name, provider.PROVIDER_NAME as Proveedor, trademark.NAME as Trademark, sector.NAME as Sector, "\
"case "\
"	when tc.IS_FINANCIAL = 1 then 'True' "\
"	else 'False' "\
"end CATEGORY_IS_FINANCIAL, "\
"case "\
"	when tc.IS_TRANSFER = 1 then 'True' "\
"	else 'False' "\
"end CATEGORY_IS_TRANSFER "\
"from t_transactions tt "\
"left join t_categories tc on tt.CATEGORY_ID = tc.id "\
"left join t_categories tcp on tc.PARENT_ID = tcp.id "\
"left join t_providers provider on tt.PROVIDER_ID = provider.id "\
"left join t_trademarks trademark on tt.TRADEMARK_ID = trademark.id "\
"left join t_provider_activity_sectors sector on provider.PROVIDER_ACTIVITY_SECTOR_ID = sector.ID "\
"where tt.ACCOUNT_ID = #account_id# "\
"and tt.DELETED = 0 "\
"order by tt.TRANSACTION_DATE desc, tt.`TIMESTAMP` desc; "

GET_HOLDER_ACCOUNT_MOVEMENTS = "select tt.TRANSACTION_DATE as 'Fecha transacción', ORIGINAL_CURRENCY_AMOUNT as 'Importe', "\
"tc.id as 'ID Categoría', tc.name as 'Nombre de categoría', tc.level, tcp.ID, tcp.name, provider.PROVIDER_NAME as Proveedor, trademark.NAME as Trademark, sector.NAME as Sector, "\
"case "\
"	when tc.IS_FINANCIAL = 1 then 'True' "\
"	else 'False' "\
"end CATEGORY_IS_FINANCIAL, "\
"case "\
"	when tc.IS_TRANSFER = 1 then 'True' "\
"	else 'False' "\
"end CATEGORY_IS_TRANSFER "\
"from t_transactions tt "\
"left join t_accounts a on tt.ACCOUNT_ID = a.id "\
"left join t_categories tc on tt.CATEGORY_ID = tc.id "\
"left join t_categories tcp on tc.PARENT_ID = tcp.id "\
"left join t_providers provider on tt.PROVIDER_ID = provider.id "\
"left join t_trademarks trademark on tt.TRADEMARK_ID = trademark.id "\
"left join t_provider_activity_sectors sector on provider.PROVIDER_ACTIVITY_SECTOR_ID = sector.ID "\
"where tt.ACCOUNT_ID = a.id and a.HOLDER_ID = #login_id# "\
"and tt.DELETED = 0 "\
"order by tt.TRANSACTION_DATE desc, tt.`TIMESTAMP` desc; "

GET_CURRENT_BALANCE = "select balance as BALANCE, AGREGATOR_SYNC_DATE as BALANCE_DATE from t_accounts where id=#account_id#;"