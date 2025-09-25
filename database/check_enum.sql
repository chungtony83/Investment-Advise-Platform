
-- Check for enum types in the database
SELECT n.nspname AS schema,
       t.typname AS enum_type
FROM pg_type t
JOIN pg_namespace n ON n.oid = t.typnamespace
WHERE t.typtype = 'e';

-- DELETE FROM pg_type WHERE typname = 'account_type_enum';
-- DELETE FROM pg_type WHERE typname = 'asset_type_enum';



-- Check for enum values
SELECT t.typname AS enum_type, e.enumlabel AS value
FROM pg_type t
JOIN pg_enum e ON t.oid = e.enumtypid
WHERE t.typtype = 'e'
ORDER BY t.typname, e.enumsortorder;