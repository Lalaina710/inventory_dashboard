/** @odoo-module **/

import { Component, useState, onWillStart, onMounted, onWillUnmount } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { rpc } from "@web/core/network/rpc";

class InventoryDashboard extends Component {
    static template = "inventory_dashboard.InventoryDashboard";
    static props = ["*"];

    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.state = useState({
            loading: true,
            data: {},
            // Filtres dynamiques
            filters: {
                chart_days: 7,
                recent_days: 30,
                active_picking_limit: 50,
                date_from: '',
                date_to: '',
                picking_type_id: 0,
                partner_id: 0,
            },
            // Données des listes déroulantes
            pickingTypes: [],
            partners: [],
            // Panneau filtres visible/masqué
            showFilters: false,
            // Auto-refresh
            autoRefreshInterval: 0,
            // Dernière mise à jour
            lastUpdate: '',
        });
        this._refreshTimer = null;

        onWillStart(async () => {
            await this.loadFiltersData();
            await this.loadConfig();
            await this.loadData();
        });

        onMounted(() => {
            this._startAutoRefresh();
        });

        onWillUnmount(() => {
            this._stopAutoRefresh();
        });
    }

    async loadConfig() {
        try {
            const config = await this.orm.call(
                'inventory.dashboard.config', 'get_config', []
            );
            this.state.filters.chart_days = config.chart_days;
            this.state.filters.recent_days = config.recent_days;
            this.state.filters.active_picking_limit = config.active_picking_limit;
            this.state.autoRefreshInterval = config.auto_refresh_interval;
        } catch (e) {
            console.warn("Config non disponible, valeurs par défaut utilisées");
        }
    }

    async loadFiltersData() {
        try {
            const data = await rpc("/inventory_dashboard/filters_data", {});
            this.state.pickingTypes = data.picking_types || [];
            this.state.partners = data.partners || [];
        } catch (e) {
            console.warn("Impossible de charger les filtres:", e);
        }
    }

    async loadData() {
        this.state.loading = true;
        try {
            const filters = { ...this.state.filters };
            // Nettoyer les filtres vides
            if (!filters.picking_type_id) delete filters.picking_type_id;
            if (!filters.partner_id) delete filters.partner_id;
            if (!filters.date_from) delete filters.date_from;
            if (!filters.date_to) delete filters.date_to;

            this.state.data = await rpc("/inventory_dashboard/data", { filters });
            this.state.lastUpdate = new Date().toLocaleTimeString("fr-FR");
        } catch (e) {
            console.error("Inventory Dashboard error:", e);
            this.state.data = {
                state_counts: {},
                late_count: 0,
                low_stock_count: 0,
                moves_today_count: 0,
                operation_type_stats: [],
                daily_moves: [],
                done_pickings_total: 0,
                done_moves_total: 0,
                active_pickings: [],
                top_products: [],
            };
        }
        this.state.loading = false;
    }

    // --- Gestion des filtres ---

    toggleFilters() {
        this.state.showFilters = !this.state.showFilters;
    }

    onFilterChange(field, ev) {
        const value = ev.target.value;
        if (['chart_days', 'recent_days', 'active_picking_limit',
             'picking_type_id', 'partner_id'].includes(field)) {
            this.state.filters[field] = parseInt(value) || 0;
        } else {
            this.state.filters[field] = value;
        }
    }

    applyFilters() {
        this.loadData();
    }

    resetFilters() {
        this.state.filters = {
            chart_days: 7,
            recent_days: 30,
            active_picking_limit: 50,
            date_from: '',
            date_to: '',
            picking_type_id: 0,
            partner_id: 0,
        };
        this.loadData();
    }

    // --- Auto-refresh ---

    onRefreshIntervalChange(ev) {
        this.state.autoRefreshInterval = parseInt(ev.target.value) || 0;
        this._startAutoRefresh();
    }

    _startAutoRefresh() {
        this._stopAutoRefresh();
        const interval = this.state.autoRefreshInterval;
        if (interval > 0) {
            this._refreshTimer = setInterval(() => this.loadData(), interval * 1000);
        }
    }

    _stopAutoRefresh() {
        if (this._refreshTimer) {
            clearInterval(this._refreshTimer);
            this._refreshTimer = null;
        }
    }

    // --- Formatage et helpers ---

    formatQty(qty) {
        if (!qty) return "0";
        return Math.round(qty).toLocaleString("fr-FR");
    }

    getBarHeight(count) {
        const maxCount = Math.max(
            ...this.state.data.daily_moves.map((d) => d.count),
            1
        );
        return Math.max((count / maxCount) * 150, 4);
    }

    getStateLabel(state) {
        const labels = {
            draft: "Brouillon",
            waiting: "En attente",
            confirmed: "En attente",
            assigned: "Prêt",
            done: "Terminé",
            cancel: "Annulé",
        };
        return labels[state] || state;
    }

    getStateBadgeClass(state) {
        const classes = {
            draft: "draft",
            waiting: "waiting",
            confirmed: "waiting",
            assigned: "assigned",
            done: "done",
            cancel: "cancel",
        };
        return classes[state] || "draft";
    }

    getOpTypeColorClass(code) {
        if (code === 'incoming') return 'op-incoming';
        if (code === 'outgoing') return 'op-outgoing';
        if (code === 'internal') return 'op-internal';
        return 'op-other';
    }

    hasActiveFilters() {
        const f = this.state.filters;
        return f.date_from || f.date_to || f.picking_type_id || f.partner_id
            || f.chart_days !== 7 || f.recent_days !== 30;
    }

    formatDate(dateStr) {
        if (!dateStr) return '-';
        try {
            const d = new Date(dateStr);
            return d.toLocaleDateString("fr-FR", {
                day: '2-digit', month: '2-digit', year: 'numeric',
                hour: '2-digit', minute: '2-digit',
            });
        } catch (e) {
            return dateStr;
        }
    }

    // --- Actions de navigation ---

    openPickings(state) {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: `Transferts - ${this.getStateLabel(state)}`,
            res_model: "stock.picking",
            views: [
                [false, "list"],
                [false, "form"],
            ],
            domain: [["state", "=", state]],
            target: "current",
        });
    }

    openLatePickings() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Transferts en retard",
            res_model: "stock.picking",
            views: [
                [false, "list"],
                [false, "form"],
            ],
            domain: [
                ["state", "in", ["assigned", "waiting", "confirmed"]],
                ["scheduled_date", "<", new Date().toISOString()],
            ],
            target: "current",
        });
    }

    openLowStock() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Règles de réapprovisionnement",
            res_model: "stock.warehouse.orderpoint",
            views: [
                [false, "list"],
                [false, "form"],
            ],
            domain: [],
            target: "current",
        });
    }

    openMovesToday() {
        const today = new Date().toISOString().slice(0, 10);
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Mouvements aujourd'hui",
            res_model: "stock.move",
            views: [
                [false, "list"],
                [false, "form"],
            ],
            domain: [
                ["state", "=", "done"],
                ["date", ">=", today + " 00:00:00"],
                ["date", "<=", today + " 23:59:59"],
            ],
            target: "current",
        });
    }

    openPicking(pickingId) {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "stock.picking",
            res_id: pickingId,
            views: [[false, "form"]],
            target: "current",
        });
    }

    openPickingsByType(typeId) {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Transferts",
            res_model: "stock.picking",
            views: [
                [false, "list"],
                [false, "form"],
            ],
            domain: [
                ["picking_type_id", "=", typeId],
                ["state", "not in", ["done", "cancel"]],
            ],
            target: "current",
        });
    }
}

registry.category("actions").add("inventory_dashboard.InventoryDashboard", InventoryDashboard);
