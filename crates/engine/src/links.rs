//! Independent DesignStrike project and support links.
//!
//! Legacy keys remain in the command protocol for existing clients, but every
//! destination belongs to DesignStrike or the Gerbzz Strike suite.

use serde_json::{Value, json};

pub const APP: &str = "designstrike";
pub const GITHUB: &str = "https://github.com/Gerbzz/DesignStrike";
pub const ISSUES: &str = "https://github.com/Gerbzz/DesignStrike/issues";
pub const WEBSITE: &str = "https://github.com/Gerbzz/PWDS-Strike-Launcher";
pub const APP_PAGE: &str = GITHUB;
/// Compatibility alias for clients that request the old community key.
pub const DISCORD: &str = ISSUES;

pub fn all() -> Value {
    json!({
        "discord": DISCORD,
        "website": WEBSITE,
        "appPage": APP_PAGE,
        "github": GITHUB,
        "issues": ISSUES,
    })
}

pub fn get(key: &str) -> Option<&'static str> {
    Some(match key {
        "discord" => DISCORD,
        "website" => WEBSITE,
        "appPage" => APP_PAGE,
        "github" => GITHUB,
        "issues" => ISSUES,
        _ => return None,
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn project_links_are_owned_by_the_fork() {
        assert!(GITHUB.to_ascii_lowercase().ends_with(&format!("/gerbzz/{APP}")));
        assert!(ISSUES.starts_with(GITHUB));
        for key in ["discord", "website", "appPage", "github", "issues"] {
            assert!(get(key).is_some_and(|url| url.starts_with("https://github.com/Gerbzz/")), "{key}");
            assert_eq!(all()[key], get(key).unwrap());
        }
    }
}
