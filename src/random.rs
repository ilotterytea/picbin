use rand::{Rng, rng};

pub const CHARACTER_POOL: &[u8] = b"ABCDEF123456";

pub fn generate_random_sequence(size: u8, char_pool: &[u8]) -> String {
    let mut rng = rng();
    let mut output = String::new();

    for _ in 0..size {
        let index = rng.random_range(0..char_pool.len());
        output.push(char_pool[index] as char);
    }

    output
}
