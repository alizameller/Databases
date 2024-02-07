02/06/24
# Ch. 4 Relational Algebra
```
Sailors(sid: int, snarne: string, rating: int, age: real) 
Boats(bid: int, bnarne: string, coloT: string)
Reserves(sid: int, bid: int, day: date)
```

σ is Selection
- example: σ<sub>ratings > 8</sub>(S)
  
∪ is OR

∩ is AND
- example: R ∩ S = R - (R - S)

\- is Set Difference

π is Projection
- example: π<sub>sname, age</sub>(S)

X is Cross Product
  
⨝ is Join operator (subscript is condition)
-  example: ⨝<sub>C</sub> S = σ<sub>C</sub> (R X S)

P is renaming
- example: P(GT8, σ<sub>ratings > 8</sub>(S)) 
  - P(GT8, 1 ▢ n, 2 ▢ a, π<sub>sname, age</sub>(S))

/ is Set Division
- example: A/B (where A, B have two fields x, y) =  π<sub>x</sub>(A) - π<sub>x</sub>(π<sub>x</sub>(A) X B - A)

### Examples:
1. Relactional Math translated into SQL
   
    π<sub>sname, age</sub> (σ<sub>ratings > 8</sub>(S))
    ```
    SELECT sname, age FROM Sailors 
        WHERE ratings > 8
    ```
2. Set Difference
    ``` 
    R       S       R-S
    1.0     1.0     2.0
    2.0     2.2     3.1
    3.1
    ```
3. Cross Product R X S
   ```
   R    S   
   1    4
   2    5
   3

   Cross Product returns 
   (1, 4), (1, 5), (2, 4), (2, 5), (3, 4), (3, 5)
   ```
4. S ⨝<sub>S, Sid</sub> = <sub>R, Sid</sub>R

5. Set Division: A/B = π<sub>x</sub>(A) - π<sub>x</sub>(π<sub>x</sub>(A) X B - A)
    ```
    A       B
    S, P    P
    ```

#### Question 1: Find the names of sailors who have reserved boat 103?
Answer: Can do this many ways
1. Join then Filter
   
   π<sub>sname</sub>(σ <sub>bid = 103</sub>(S ⨝ R))
2. Filter then Join
   
   π<sub>sname</sub>((σ <sub>bid = 103</sub> R) ⨝ S)
3. 
   π<sub>sname</sub>(S ⨝<sub>bid = 103</sub> R)

#### Question 2: Find the names of sailors who have reserved a red boat?
Answer:

1. π<sub>sname</sub>((σ <sub>color = red</sub>(B) ⨝ R) ⨝ S)
2. π<sub>sname</sub>(π<sub>sid</sub>((π<sub>bid</sub>(σ <sub>color = red</sub>(B))) ⨝ R) ⨝ S)

#### Question 3: Find the colors of boats reserved by 'Lubber'?
Answer:

1. π<sub>color</sub>(σ <sub>sname = 'lubber'</sub>(S) ⨝ R ⨝ B)

#### Question 4: Find the names of sailors who have reserved at least one boat?
Answer:

1. π<sub>sname</sub>(S ⨝ R)

#### Question 5: Find the names of sailors who have reserved a red or green  boat?
Answer:

1. π<sub>sname</sub>(σ <sub>color = red v color = green</sub>(B)) ⨝ S ⨝ R