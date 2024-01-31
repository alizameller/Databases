# Ch. 2 Introduction To Database Design
#### Data Independence
#### Efficient Data Access
#### Data Integrity
- Make sure you are meeting the application requirements
- Security
  - Different tiers of access levels (for enterprise tools)
  - Concurrent access (locks)
- Crash recovery (need to write to disk, otherwise risk data loss)
  - Transaction logs 
  - Backup database
- Reducing fundamental application development time by using standard tools

### ACID
- Atomicity
  - When you split something into a transaction, its all or nothing (database is exactly how you left it)
- Consistency
  - For a given query the same result will be returned when repeated, on disk same data
- Isolation
  - Things can safely happen in parallel
  - Locks (read locks and write locks)
    - Dirty read (in the middle you read a mixture of pre and post values)
- Durability 
  - Related to recovery stuff mentioned above

##### Data Models
- Relational data models
- _______ data model (?)

### Entity Relationship (ER) Diagrams
- Entry (CAPS)
  - Object 
- Attribute (lowercase)
  - Things that characterize the object (or belong to)
- Key (underline)
  - An identifier
- Relationship (diamond)

- Weak entity 
  - Dependents of an employee 
  - When employee leaves, their dependents and policy are destroyed

Diagram 1

    +---------+     +---------+    +---------+                                +------+    +-------+  +--------+
    |         |     |         |    |         |           +---------+          |      |    |       |  |        |
    |   ssn   |     |   name  |    |   dob   |           |  since  |          | name |    |  did  |  | budget |
    |   ---   |     |         |    |         |           +----+----+          |      |    |  ---  |  |        |
    +-----+---+     +----+----+    +-----+---+                |               +----+-+    +--+----+  +-+------+
        |              |               |                     / \                 |         |         |
        |              |               |                    /   \                |         |         |
    +---+--------------+---------------+----+              /     \             +-+---------+----+    |
    |                                       |             /       \            |                +----+
    |                                       |            /  WORKS  \-----------+                |
    |                                       +------------\         /           |     DEPT       |
    |                EMPLOYEE               |             \       /            |                |
    |                                       |              \     /             |                |
    |                                       |               \   /              +----------------+
    |                                       |                \ /
    +---------+------------------+----------+                 |
            |                  |                              |
    Supervisor|                |Subordinate                   |
            |                  |                        +-----+-----+
            |                  |            +---------+ |           |   +----------+
            |        / \       |            | address +-+ LOCATIONS +---+ capacity |
            |       /   \      |            +---------+ |           |   +----------+
            +------/     \-----+                        +-----------+
                  /       \
                 / REPORTS \
                 \    TO   /
                  \       /
                   \     /
                    \   /
                     \ /


#### Bolded lines (double lines) and Arrows

Arrows mean that given a DEPARTMENTS entity, we can uniquely determine the MANAGES relationship because each MANAGES relationship has exactly one DEPARTMENTS entity

Bolded lines (double lines) indicate that the participation of an entity set in a relationship set is total


    +---------+     +---------+    +---------+                                +------+    +-------+  +--------+
    |         |     |         |    |         |           +---------+          |      |    |       |  |        |
    |   ssn   |     |   name  |    |   dob   |           |  since  |          | name |    |  d_id |  | budget |
    |   ---   |     |         |    |         |           +----+----+          |      |    |  ---  |  |        |
    +-----+---+     +----+----+    +-----+---+                |               +----+-+    +--+----+  +-+------+
        |              |               |                     / \                 |         |         |
        |              |               |                    /   \                |         |         |
    +---+--------------+---------------+----+              /     \             +-+---------+----+    |
    |                                       |             /       \            |                +----+
    |                                       |            / MANAGES \           |                |
    |                                       +--------++--\         /<+---------+      DEPT      |
    |                EMPLOYEE               |        ||   \       /  +-++------+                |
    |                                       |        ||    \     /     ||      |                |
    |                                       |        ||     \   /      ||      +----------------+
    |                                       |        ||      \ /       ||
    +---------+------------------+----------+        ||                ||
            |                  |                     ||                ||
    Supervisor                 |Subordinate          ||      / \       ||
            |                  |                     ||     /   \      ||
            |                  |                     ||    /     \     ||
            |        / \       |                     ||   /       \    ||
            |       /   \      |                     |+-+/  WORKS  \+--+|
            +------/     \-----+                     +--+\         /+---+
                  /       \                               \       /
                 / REPORTS \                               \     /
                 \    TO   /                                \   /
                  \       /                                  \ /
                   \     /
                    \   /
                     \ /

#### Weak entities (dependents) and partial keys
Dependents are weak entities and each weak entity must have total participation in the indentifying relationship set. Each weak entity therefore has an identifying owner (depicted with bold lines (double))

Partial keys are keys that are identifying given another attribute. In this case, Dependents are identied uniquely with the pname of the Dependent AND the key of the owning Employees entity. 

        +---------+
        |         |
        |  cost   |
        |         |
        +----+----+
             |
           // \\
          //   \\
         //     \\-------- EMPLOYEE
        //       \\
       //  POLICY \\
       \\         //
        \\       //
         \\     //
          \\   //
           \\ //
    +----------------+
    |+--------------+|
    ||              ||
    ||  DEPENDENTS  ||
    ||              ||
    |+--------------+|
    +--+----------+--+
       |          |
    +------+--+   +---+-----+
    |         |   |         |
    | p_name  |   |   age   |
    | - - - - |   |         |
    +---------+   +---------+

More examples in the textbook

### Class Hierarchy

ISA (pronounced "is a")
  - Hourly employees and contract employees inherit from EMPLOYEES 
  - Think of this as subclasses
#### Constraints 
- Overlap contraints determine whether two subclasses can contain the same entity
  - Ex: Senior employee and contract employee (overlap allowed) vs. contract employee and hourly employee (overlap not allowed)
- Covering constraints determine whether the entities in the subclasses exhaust all entities in the superclass
  - Ex: does every EMPLOYEEs entity belong to one of the subclasses? (no, so there is no covering constraint)

#### Aggregation

### Binary vs. Ternary Relationships
#### Requirements
1. A policy can only be owned by at most 1 employee
2. Every policy must be owned by at least 1 employee
3. Policy is linked to dependents (each dependent is uniquely identified with pname (weak identifier) AND policy_id of policy)

Re: Figure 2.18 Policy Revisited
Employee purchases a policy and the policy covers the dependents

Getting rid of the ternery relationship made this diagram clearer

### Docker Containers and Postgres
Note for running postgres in Docker container - use the following command instead of `postgres`:

`docker exec -ti databases-course psql -U postgres`

To create table:
```
postgres=# CREATE TABLE accounts ( 
    user_id SERIAL PRIMARY KEY, 
    username VARCHAR (50) UNIQUE NOT NULL, 
    password VARCHAR (50) NOT NULL, 
    email VARCHAR (255) UNIQUE NOT NULL, 
    created_at TIMESTAMP NOT NULL, 
    last_login TIMESTAMP);
```
To insert accounts:
```
postgres=# insert into accounts (username, password, email, created_at) VALUES ('testusername', 'password', 'hello@world.com', NOW());
``````
To get number of accounts:
```
postgres=# select COUNT(*) from accounts
```
To get accounts with condition:
```
postgres=# select * from accounts where user_id > 4
```