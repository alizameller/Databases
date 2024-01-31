# Notes
Data Independence

Efficient Data Access

Data Integrity
- Make sure you are meeting the application requirements
- Security
  - Different tiers of access levels (for enterprise tools)
  - Concurrent access (locks)
- Crash recovery (need to write to disk, otherwise risk data loss)
  - Transaction logs 
  - Backup database
- Reducing fundamental application development time by using standard tools

ACID
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

Data Models
- Relational data models
- _______ data model (?)

Entity Relationship (ER) Diagrams
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

Diagram

    +---------+     +---------+    +---------+                                +------+    +-------+  +--------+
    |         |     |         |    |         |             +---------+        |      |    |       |  |        |
    |   ssn   |     |   name  |    |   dob   |             |  since  |        | name |    |  did  |  | budget |
    |   ---   |     |         |    |         |             +----+----+        |      |    |  ---  |  |        |
    +-----+---+     +----+----+    +-----+---+                  |             +----+-+    +--+----+  +-+------+
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
            |                  |                            |
    Supervisor|                  |Subordinate                 |
            |                  |                      +-----+-----+
            |                  |          +---------+ |           |   +----------+
            |        / \       |          | address +-+ LOCATIONS +---+ capacity |
            |       /   \      |          +---------+ |           |   +----------+
            +------/     \-----+                      +-----------+
                  /       \
                 / REPORTS \
                 \    TO   /
                  \       /
                   \     /
                    \   /
                     \ /


Bolded lines and Arrows


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

Weak entities (dependents) and partial keys

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

