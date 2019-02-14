use std::fs::File;
use std::io::{Read, Result};

#[derive(Clone)]
pub struct Node {
    pub literal: i16, // the id of the literal
    pub value: bool, // the chosen value for the literal
    pub picked: bool, // Whether this node was picked, otherwise was chosen through simplification
}

#[derive(Clone)]
pub struct Solver {
    pub clauses: Vec<Vec<i16>>,
    pub tree: Vec<Node>,
}

impl Solver {
    pub fn print(&self) {
        for (i, clause) in self.clauses.iter().enumerate() {
            print!("{}: [ ", i);
            for lit in clause {
                print!("{} ", lit);
            }
            println!("]");
        }
    }

    pub fn add_sat_file(&mut self, fname: String) {
        let file_string = read_file(fname).unwrap();
        for line in file_string.lines() {
            if line.starts_with('p') || line.starts_with('c') { continue; }
            let mut clause: Vec<i16> = Vec::new();
            for c in line.split_whitespace() {
                let lit: i16 = c.parse().unwrap();
                // Finished this lines clause
                if lit == 0 {
                    self.clauses.push(clause);
                    break;
                }
                clause.push(lit);
            }
        }
    }
}

fn rec_test(mut solver: Solver, i: i16) -> bool {
    solver.clauses.push(vec![i, i, i]);
    println!("{}", i);
    solver.print();
    if i == 4 {
        return true;
    }
    let retval = rec_test(solver.clone(), i + 1);
    if i != 0 {
        return retval;
    } else {
        println!("weeeeeee");
        solver.print();
        return true;
    }
}

fn read_file(fname: String) -> Result<String> {
    let mut file = File::open(fname)?;
    let mut s = String::new();
    file.read_to_string(&mut s)?;
    Ok(s)
}

fn read_sudoku_file(fname: String) {
    let file_string = read_file(fname).unwrap();
    for line in file_string.lines() {
        for (i, c) in line.chars().enumerate() {
            if c != '.' {
                let column = i % 9 + 1;
                let row = i / 9 + 1;
                let new_rule = format!("{}{}{} 0", column, row, c);
                println!("{}", new_rule);
            }
        }
    }
}

fn main() {
    // let filename = String::from("damnhard.sdk.txt");
    // read_sudoku_file(filename);

    let mut solver = Solver{ clauses:  vec![], tree: vec![]};
    let filename = String::from("test.sat");
    solver.add_sat_file(filename);
    solver.print();
    rec_test(solver, 0);
    println!("AYYYYYYY");
    // solver.print();
}
