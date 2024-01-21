use pyo3::prelude::*;
use std;
use std::collections::HashMap;
use std::option::Option;
/// CrossNumber board as a Rust struct for performance
#[pyclass]
struct RustedBoard {
    #[pyo3(get, set)]
    height: u8,
    #[pyo3(get, set)]
    width: u8,
    #[pyo3(get, set)]
    values: Vec<u8>,
}

#[pymethods]
impl RustedBoard {
    #[new]
    fn new(height: u8, width: u8) -> Self {
        RustedBoard {
            height,
            width,
            values: vec![255; (height * width) as usize],
        }
    }

    fn set_value(&mut self, row: u8, col: u8, horizontal: bool, value: u32) {
        if horizontal {
            for (idx, digit) in value
                .to_string()
                .chars()
                .map(|d| d.to_digit(10).unwrap())
                .enumerate()
            {
                self.values[(row * self.width + col + idx as u8) as usize] = digit as u8;
            }
        } else {
            for (idx, digit) in value
                .to_string()
                .chars()
                .map(|d| d.to_digit(10).unwrap())
                .enumerate()
            {
                self.values[((row + idx as u8) * self.width + col) as usize] = digit as u8;
            }
        }
    }

    fn get_value(&mut self, row: u8, col: u8, horizontal: bool, length: u8) -> u32 {
        if horizontal {
            self.values[(row * self.width + col as u8) as usize
                ..(row * self.width + col + length as u8) as usize]
                .iter()
                .enumerate()
                .map(|(idx, val)| *val as u32 * 10_u32.pow((length - idx as u8 - 1) as u32))
                .sum::<u32>()
        } else {
            self.values[(row * self.width + col as u8) as usize
                ..((row + length) * self.width + col as u8) as usize]
                .iter()
                .step_by(self.width as usize)
                .enumerate()
                .map(|(idx, val)| *val as u32 * 10_u32.pow((length - idx as u8 - 1) as u32))
                .sum::<u32>()
        }
    }

    fn clear(&mut self) {
        self.values = vec![255; (self.height * self.width) as usize];
    }
    fn safe_up_to_tier_one(
        &mut self,
        solution: Vec<i32>,
        position: usize,
        all_pos: Vec<(u8, u8, bool)>,
        pos_all_possible: HashMap<(u8, u8, bool), Vec<usize>>,
    ) -> bool {
        for s in 0..position as usize {
            self.set_value(
                all_pos[s].0,
                all_pos[s].1,
                all_pos[s].2,
                pos_all_possible.get(&all_pos[s]).unwrap()[solution[s] as usize] as u32,
            );
            if !self.is_possible(
                all_pos[s + 1].0,
                all_pos[s + 1].1,
                all_pos[s + 1].2,
                pos_all_possible.get(&all_pos[s + 1]).unwrap()[solution[s + 1] as usize] as u32,
            ) {
                return false;
            }
        }
        self.set_value(
            all_pos[position].0,
            all_pos[position].1,
            all_pos[position].2,
            pos_all_possible.get(&all_pos[position]).unwrap()[solution[position] as usize] as u32,
        );
        return true;
    }
    fn is_possible(&self, row: u8, col: u8, horizontal: bool, value: u32) -> bool {
        let length: u8 = value.ilog10() as u8 + 1;
        if horizontal {
            return std::iter::zip(
                value
                    .to_string()
                    .chars()
                    .map(|d| d.to_digit(10).unwrap() as u8),
                self.values[(row * self.width + col as u8) as usize
                    ..(row * self.width + col + length as u8) as usize]
                    .iter(),
            )
            .map(|(target, current)| target != *current && *current != 255)
            .all(|x| !x);
        } else {
            return std::iter::zip(
                value
                    .to_string()
                    .chars()
                    .map(|d| d.to_digit(10).unwrap() as u8),
                self.values[(row * self.width + col as u8) as usize
                    ..((row + length - 1) * self.width + col as u8 + 1) as usize]
                    .iter()
                    .step_by(self.width as usize),
            )
            .map(|(target, current)| target != *current && *current != 255)
            .all(|x: bool| !x);
        }
    }
    fn get_digit_count(&self) -> [u8; 10] {
        let mut count_arr: [u8; 10] = [0; 10];
        for x in 0..10 {
            count_arr[x as usize] = self.values.iter().filter(|&n| *n == x).count() as u8
        }
        count_arr
    }
    fn get_value_multiple(&mut self, positions: Vec<(u8, u8, bool, u8)>) -> Vec<u32> {
        let mut values: Vec<u32> = vec![];
        for idx in 0..positions.len() {
            values.push(self.get_value(
                positions.get(idx).unwrap().0,
                positions.get(idx).unwrap().1,
                positions.get(idx).unwrap().2,
                positions.get(idx).unwrap().3,
            ))
        }
        values
    }
    fn get_dsum_multiple(&mut self, positions: Vec<(u8, u8, bool, u8)>) -> Vec<u32> {
        let mut values: Vec<u32> = vec![];
        for idx in 0..positions.len() {
            values.push(
                self.get_value(
                    positions.get(idx).unwrap().0,
                    positions.get(idx).unwrap().1,
                    positions.get(idx).unwrap().2,
                    positions.get(idx).unwrap().3,
                )
                .to_string()
                .chars()
                .map(|c| c.to_digit(10).unwrap())
                .sum(),
            )
        }
        values
    }
    fn backtrace(
        &mut self,
        current_solution: Vec<i32>,
        all_pos: Vec<(u8, u8, bool)>,
        pos_all_possible: HashMap<(u8, u8, bool), Vec<usize>>,
        all_possible_count: HashMap<(u8, u8, bool), i32>,
    ) -> Option<Vec<i32>> {
        let number_all: usize = all_pos.len();
        let mut solution: Vec<i32>;
        let mut position: isize;
        if current_solution.len() == 0 {
            solution = vec![-1; number_all];
            solution[0] = 0;
            position = 0;
        } else {
            solution = current_solution;
            position = match solution.iter().position(|&x| x == -1) {
                Some(idx) => idx as isize,
                None => (solution.len() - 1) as isize,
            };
        }
        let mut max_position = 0;

        loop {
            if self.safe_up_to(&solution, position as usize, &all_pos, &pos_all_possible) {
                if position > max_position {
                    max_position = position
                }

                if position as usize == number_all - 1 {
                    return Some(solution);
                }
                position += 1;
                solution[position as usize] = 0;
            } else {
                while solution[position as usize]
                    == all_possible_count.get(&all_pos[position as usize]).unwrap() - 1
                {
                    solution[position as usize] -= 1;
                    position -= 1;
                }
                if position < 0 {
                    break;
                }
                solution[position as usize] += 1;
                self.clear();
            }
        }
        self.clear();
        return None;
    }
}
/// A Python module implemented in Rust.

impl RustedBoard {
    fn safe_up_to(
        &mut self,
        solution: &Vec<i32>,
        position: usize,
        all_pos: &Vec<(u8, u8, bool)>,
        pos_all_possible: &HashMap<(u8, u8, bool), Vec<usize>>,
    ) -> bool {
        for s in 0..position as usize {
            self.set_value(
                all_pos[s].0,
                all_pos[s].1,
                all_pos[s].2,
                pos_all_possible.get(&all_pos[s]).unwrap()[solution[s] as usize] as u32,
            );
            if !self.is_possible(
                all_pos[s + 1].0,
                all_pos[s + 1].1,
                all_pos[s + 1].2,
                pos_all_possible.get(&all_pos[s + 1]).unwrap()[solution[s + 1] as usize] as u32,
            ) {
                return false;
            }
        }
        self.set_value(
            all_pos[position].0,
            all_pos[position].1,
            all_pos[position].2,
            pos_all_possible.get(&all_pos[position]).unwrap()[solution[position] as usize] as u32,
        );
        return true;
    }
}
#[pymodule]
fn CrossNumber(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<RustedBoard>()?;
    Ok(())
}
