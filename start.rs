use std::fs::File;
use std::io::{Read, Result};

#[derive(Clone)]
pub struct Node {
    pub literal: i16, // the id of the literal
    pub value: bool, // the chosen value for the literal
    pub picked: bool, // Whether this node was picked, otherwise was chosen through simplification
}

#[derive(Clone, Default)]
pub struct Solver {
    pub clauses: Vec<Vec<(u16, bool)>>,
    pub n_falses: Vec<usize>,
    pub literals: Vec<Vec<u16>>,
    pub tree: Vec<Node>,
}

impl Solver {
    pub fn print(&self) {
        println!("Clauses:");
        for (i, (clause, n_false)) in self.clauses.iter().zip(self.n_falses.iter()).enumerate() {
            print!("{}: [", i);
            for (lit, sign) in clause {
                let sign = if !sign { "¬" } else { " " };
                print!("{}{} ", sign, lit);
            }
            println!("] #-{}",n_false);
        }

        println!("\n\nLiterals:");
        for (lit, clvec) in self.literals.iter().enumerate() {
            print!("{}: [", lit);
            for clause in clvec {
                print!("{} ", clause);
            }
            println!("]");
        }
    }

    pub fn add_sat_file(&mut self, fname: String) {
        let file_string = read_file(fname).unwrap();
        for line in file_string.lines() {
            if line.starts_with('p') || line.starts_with('c') { continue; }
            let mut clause: Vec<(u16, bool)> = Vec::new();
            self.n_falses.push(0);
            for c in line.split_whitespace() {
                let ilit: i16 = c.parse().unwrap();
                let lit = ilit.abs() as usize;
                if lit == 0 { // Finished this lines clause
                    self.clauses.push(clause);
                    break;
                }
                if self.literals.len() < lit + 1 {
                    self.literals.resize(lit + 1, vec![]);
                }
                self.literals[lit].push(self.clauses.len() as u16);
                clause.push((lit as u16, ilit > 0));
            }
        }
    }
}

fn rec_test(mut solver: Solver, i: u16) -> bool {
    solver.clauses.push(vec![(i, true), (i, true), (i, true)]);
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

    let mut solver: Solver = Default::default();
    let filename = String::from("test.sat");
    solver.add_sat_file(filename);
    solver.print();
    // rec_test(solver, 0);
    // println!("AYYYYYYY");
    // solver.print();
}
