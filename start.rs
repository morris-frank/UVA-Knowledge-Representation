use std::fs::File;
use std::io::{Read, Result};

#[derive(Clone)]
pub struct Node {
    pub literal: u16, // the id of the literal
    pub value: bool, // the chosen value for the literal
    pub picked: bool, // Whether this node was picked, otherwise was chosen through simplification
}

#[derive(Clone, Default)]
pub struct Solver {
    pub clauses: Vec<Vec<(u16, bool)>>,
    pub n_not_falses: Vec<usize>,
    pub literal_clauses: Vec<Vec<u16>>,
    pub literal_values: Vec<Option<bool>>,
    pub tree: Vec<Node>,
}

impl Solver {
    pub fn print(&self) {
        println!("Clauses:");
        for (i, (clause, n_not_false)) in self.clauses.iter().zip(self.n_not_falses.iter()).enumerate() {
            print!("{}: [", i);
            for (lit, sign) in clause {
                let sign = if !sign { "¬" } else { " " };
                print!("{}{} ", sign, lit);
            }
            println!("] #-{}",n_not_false);
        }

        println!("\n\nLiterals:");
        for (lit, clauses) in self.literal_clauses.iter().enumerate() {
            print!("{}: [", lit);
            for clause in clauses {
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
            for c in line.split_whitespace() {
                let ilit: i16 = c.parse().unwrap();
                let lit = ilit.abs() as usize;
                if lit == 0 { // Finished this lines clause
                    self.n_not_falses.push(clause.len());
                    self.clauses.push(clause);
                    break;
                }
                if self.literal_clauses.len() < lit + 1 {
                    self.literal_clauses.resize(lit + 1, vec![]);
                    self.literal_values.resize(lit + 1, None);
                }
                self.literal_clauses[lit].push(self.clauses.len() as u16);
                clause.push((lit as u16, ilit > 0));
            }
        }
    }

    pub fn add_node(&mut self, literal: u16, value: bool, picked: bool) {
        println!("⇒ {} ⇐", literal);
        self.tree.push(Node{literal, value, picked});
        self.literal_values[literal as usize] = Some(value);
    }

    pub fn literal_value(&self, literal: u16) -> Option<bool> {
        for node in &self.tree {
            if node.literal == literal {
                return Some(node.value.clone());
            }
        }
        return None;
    }

    pub fn simplify(&mut self) {
        for clauseid in self.n_not_falses.iter().position(|&x| x== 1) {
            println!("Clause with id {} is uni", clauseid);
        }
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
    let mut solver: Solver = Default::default();
    let filename = String::from("test.sat");
    solver.add_sat_file(filename);
    solver.print();
    solver.simplify();
}
