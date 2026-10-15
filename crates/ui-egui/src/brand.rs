//! Approved PWDS artwork for the DesignStrike welcome screen and About panel.

use egui::{Color32, Rect, Sense, TextureHandle, TextureOptions, pos2, vec2};

static PWDS_MARK: &[u8] = include_bytes!("../../../assets/branding/PWDS-logo.png");

fn mark(ctx: &egui::Context) -> Option<TextureHandle> {
    let id = egui::Id::new("designstrike-pwds-mark");
    if let Some(texture) = ctx.data(|data| data.get_temp::<TextureHandle>(id)) {
        return Some(texture);
    }
    let bitmap = image::load_from_memory_with_format(PWDS_MARK, image::ImageFormat::Png).ok()?.to_rgba8();
    let pixels = egui::ColorImage::from_rgba_unmultiplied([bitmap.width() as usize, bitmap.height() as usize], bitmap.as_raw());
    let texture = ctx.load_texture("designstrike-pwds-mark", pixels, TextureOptions::LINEAR);
    ctx.data_mut(|data| data.insert_temp(id, texture.clone()));
    Some(texture)
}

pub fn logo(ui: &egui::Ui, plaque: Rect) {
    ui.painter().rect_filled(plaque, 10.0, Color32::WHITE);
    if let Some(texture) = mark(ui.ctx()) {
        let width = plaque.width() - 20.0;
        let image = Rect::from_center_size(plaque.center(), vec2(width, width * 129.0 / 300.0));
        ui.painter().image(texture.id(), image, Rect::from_min_max(pos2(0.0, 0.0), pos2(1.0, 1.0)), Color32::WHITE);
    }
}

pub fn about_header(ui: &mut egui::Ui, version: &str) {
    let (card, _) = ui.allocate_exact_size(vec2(ui.available_width(), 118.0), Sense::hover());
    ui.painter().rect_filled(card, 12.0, Color32::from_rgb(27, 36, 56));
    let plaque = Rect::from_min_size(card.min + vec2(16.0, 20.0), vec2(164.0, 78.0));
    logo(ui, plaque);
    ui.painter().text(card.min + vec2(198.0, 47.0), egui::Align2::LEFT_CENTER, "DesignStrike", egui::FontId::proportional(25.0), Color32::WHITE);
    ui.painter().text(
        card.min + vec2(198.0, 78.0),
        egui::Align2::LEFT_CENTER,
        format!("Version {version}  |  Page layout and publishing"),
        egui::FontId::proportional(12.0),
        Color32::from_rgb(190, 202, 222),
    );
}
