//! Independent DesignStrike About panel with the inherited contributor credits.

use egui::{Rect, pos2, vec2};

use crate::DesignApp;
use crate::theme::Tokens;

/// The About window's tabs, in `UiState::about_tab` order.
pub const ABOUT_TABS: [&str; 3] = ["About", "Contributors", "Models"];

pub fn show(app: &mut DesignApp, ctx: &egui::Context) {
    if !app.ui.about {
        return;
    }
    let t = Tokens::get(ctx);
    let area = egui::Id::new("about");
    let instance = area.with("placement");
    let resp = crate::modal_drag::modal(ctx, area, instance).show(ctx, |ui| {
        ui.set_width(if app.ui.about_tab == 0 { 500.0 } else { 640.0 });
        let margin = egui::Frame::popup(ui.style()).inner_margin;
        let top = ui.cursor().top();
        let title_row = Rect::from_min_max(
            pos2(ui.max_rect().left() - margin.leftf(), top - margin.topf()),
            pos2(ui.max_rect().right() + margin.rightf(), top + ui.spacing().interact_size.y),
        );
        crate::modal_drag::title_drag(ui, instance, title_row);
        ui.horizontal(|ui| {
            for (i, label) in ABOUT_TABS.iter().enumerate() {
                let i = i as u8;
                if ui.selectable_label(app.ui.about_tab == i, crate::rtl::widget(ui, crate::i18n::tr(&app.ui.language, label))).clicked() {
                    app.ui.about_tab = i;
                }
            }
        });
        ui.separator();
        if app.ui.about_tab != 0 {
            let h = 400.0_f32.min(ctx.content_rect().height() * 0.7).max(160.0);
            ui.allocate_ui_with_layout(vec2(ui.available_width(), h), egui::Layout::top_down(egui::Align::Min), |ui| {
                ui.set_min_height(h);
                if app.ui.about_tab == 1 {
                    crate::credits::contributors_ui(ui);
                } else {
                    crate::credits::models_ui(ui);
                }
            });
        } else {
            ui.add_space(8.0);
            crate::brand::about_header(ui, env!("CARGO_PKG_VERSION"));
            ui.add_space(14.0);
            ui.label(egui::RichText::new("A page layout workspace for print and screen.").size(14.0).color(t.text_strong));
            ui.add_space(5.0);
            ui.label(
                egui::RichText::new("Built from the open-source DesignCraft application. Original contributors retain their credit and licences.")
                    .size(12.0)
                    .color(t.text_dim),
            );
            ui.add_space(12.0);
            ui.horizontal(|ui| {
                if ui.button("Project source").clicked() {
                    app.ui.pending_urls.push("https://github.com/Gerbzz/DesignStrike".into());
                }
                if ui.button("Report an issue").clicked() {
                    app.ui.pending_urls.push("https://github.com/Gerbzz/DesignStrike/issues".into());
                }
                if ui.button("Original project").clicked() {
                    app.ui.pending_urls.push("https://github.com/storytold/designcraft".into());
                }
            });
            ui.add_space(12.0);
            ui.label(egui::RichText::new("Software: MIT OR Apache-2.0  |  PWDS mark: separate owner terms").size(11.0).color(t.text_dim));
        }
        ui.add_space(10.0);
        ui.separator();
        ui.vertical_centered(|ui| {
            if ui.button(crate::rtl::widget(ui, crate::i18n::tr(&app.ui.language, "  Close  "))).clicked() {
                app.ui.about = false;
            }
        });
    });
    if resp.should_close() {
        app.ui.about = false;
    }
}
