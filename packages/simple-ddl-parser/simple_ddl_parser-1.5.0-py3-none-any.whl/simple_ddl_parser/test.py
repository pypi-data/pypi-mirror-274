from simple_ddl_parser import DDLParser
import pprint

ddl = """
CREATE TABLE `posts`(
    `integer_column__unique` INT NOT NULL AUTO_INCREMENT UNIQUE,   
    `integer_column__unique_key` INT NOT NULL AUTO_INCREMENT UNIQUE KEY,               
    `integer_column__index` INT NOT NULL AUTO_INCREMENT INDEX
);
"""

result = DDLParser(ddl).run()
pprint.pprint(result)


