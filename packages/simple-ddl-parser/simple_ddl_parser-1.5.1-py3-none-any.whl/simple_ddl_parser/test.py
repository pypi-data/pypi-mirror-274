from simple_ddl_parser import DDLParser
import pprint

ddl = """CREATE TABLE IF NOT EXISTS public.generator_id (
hall_id int4 GENERATED ALWAYS AS IDENTITY(
INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1 NO CYCLE
) NOT NULL,
hall_name varchar(50) NOT NULL,
CONSTRAINT hall_pkey PRIMARY KEY (hall_id));
);"""

result = DDLParser(ddl).run()
pprint.pprint(result)


