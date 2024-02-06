02/06/24
# Relational Algebra

### Relations
- An instance of a relation is a set of tuples (also called records), specifying the rows of the table
- Each row must be unique
- Degree, arity or cardinality = number of rows

DDL: Data Definition Language
- Used to define conceptual (logical) and external schemas
- CREATE TABLE

DML: Data Manipulation Language
- Used for creating, modifying or quering data
- INSERT or DELETE or UPDATE
- Need a WHERE key word in DELETE and UPDATE statements

Integrity Constraints (IC) - Things that will give you errors:
- Domain constraints: Data types
- Key constraint: a candidate key which is a minimal subset of fields of a relation that is a unique identifier of a tuple
  - Foreign key: you cannot access the data if you do not have a matching primary key of the referenced relation (can be explicitly used with keyword FOREIGN KEY or abstractly)

Values:
- SERIAL is an auto-incrementing integer
- NULL is an optional field
- CASCADE means that rows in the referencing relation should be deleted along with the row in the referenced relation
- SET DEFAULT can be used in place of CASCADE which would switch the foreign key to a default student (default is specified in creation of the table)
- Transaction 
  - Atomicity is key in databases, so transactions allow for multi-step operations to be carried out in full, not half way