from odoo import models, fields, api


class InventoryDashboardConfig(models.Model):
    _name = 'inventory.dashboard.config'
    _description = 'Configuration Tableau de bord Inventaire'

    name = fields.Char(default='Configuration Dashboard Inventaire', required=True)
    chart_days = fields.Integer(
        string='Jours graphique mouvements',
        default=7,
        help='Nombre de jours affichés dans le graphique des mouvements de stock',
    )
    recent_days = fields.Integer(
        string='Jours statistiques récentes',
        default=30,
        help='Période pour le calcul des statistiques récentes (transferts terminés)',
    )
    active_picking_limit = fields.Integer(
        string='Limite transferts actifs',
        default=50,
        help='Nombre maximum de transferts actifs affichés dans le tableau',
    )
    auto_refresh_interval = fields.Selection([
        ('0', 'Désactivé'),
        ('30', '30 secondes'),
        ('60', '1 minute'),
        ('120', '2 minutes'),
        ('300', '5 minutes'),
    ], string='Rafraîchissement auto', default='0')
    company_id = fields.Many2one(
        'res.company', string='Société',
        default=lambda self: self.env.company,
    )

    @api.model
    def get_config(self):
        """Retourne la config active ou les valeurs par défaut."""
        config = self.search([
            ('company_id', '=', self.env.company.id),
        ], limit=1)
        if config:
            return {
                'chart_days': config.chart_days,
                'recent_days': config.recent_days,
                'active_picking_limit': config.active_picking_limit,
                'auto_refresh_interval': int(config.auto_refresh_interval),
            }
        return {
            'chart_days': 7,
            'recent_days': 30,
            'active_picking_limit': 50,
            'auto_refresh_interval': 0,
        }
